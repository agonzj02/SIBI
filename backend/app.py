import pandas as pd
import numpy as np
import os
import ast
import base64
import random
import time

from dotenv import load_dotenv, find_dotenv

from flask import Flask, request, abort, request_started, g
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_json import FlaskJSON, JsonError, json_response, as_json

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from scipy.stats import pearsonr

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)
FlaskJSON(app)

api = Api(app)

def env(key, default=None, required=True):
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)

DATABASE_USERNAME = env('MOVIE_DATABASE_USERNAME')
DATABASE_PASSWORD = env('MOVIE_DATABASE_PASSWORD')
DATABASE_URL = env('MOVIE_DATABASE_URL')

driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

def serialize_movie(movie, genres, actors, directors, country, my_rating=None, directors_name = None):
    return {
        'id': movie['id'],
        'imdbID': movie['imdbID'],
        'title': movie['title'],
        'picture': movie['picture'],
        'year' : movie['year'],
        'genres' : genres,
        'actors' : actors,
        'directors': directors,
        'country': country,
        'rating' : my_rating,
        'directors_name' : directors_name
    }

def serialize_movie_pandas(row):
    return {
            'id': row['id'],
            'imdbID': row['imdbID'],
            'title': row['title'],
            'picture': row['picture'],
            'year' : row['year'],
            'genres' : row['genres'],
            'actors' : row['actors'],
            'directors': row['directors_name'],
            'country': row['country'],
            'rating' : None
        }

def serialize_user(user, num_rated=None):
    return{
        'id': user['id'],
        'nombre': user['nombre'],
        'apellidos': user['apellidos'],
        'username': user['username'],
        'num_rated': num_rated
    }

def serialize_top_movie(genre, movies):
    normalized = []
    for movie in movies:
        normalized.append({
            'id': movie['id'],
            'title': movie['title'],
            'picture': movie['picture'],
            'genre' : genre
        })
    return normalized

def serialize_rating(user, movie, rating):
    return {
        'id' : movie,
        'username': user,
        'rating': rating
    }

class Register(Resource):
    def post(self):
        def get_user_by_username(tx, username):
            return tx.run(
                '''
                MATCH (user:User {username: $username}) RETURN user
                ''', {'username': username}
            ).single()

        def get_next_id(tx):
            return tx.run(
                '''
                match(u:User) return max(u.id)+1 as max
                '''
            ).single()

        def create_user(tx, id, nombre, apellidos, username, password):
            return tx.run(
                '''
                CREATE (user:User {id: $id, nombre: $nombre, apellidos: $apellidos, username: $username, password: $password}) RETURN user
                ''',
                {
                    'id': id,
                    'nombre': nombre,
                    'apellidos': apellidos,
                    'username': username,
                    'password': str(password)
                }
            ).single()

        inp = request.get_json()
        nombre = inp['nombre']
        apellidos = inp['apellidos']
        username = inp['user']
        password = inp['pass']
        password = password.encode("utf-8")
        password = base64.b64encode(password)

        db = get_db()
        result = db.read_transaction(get_user_by_username, username)
        if result and result.get('user'):
            return {'error': 'username already in use'}, 400
        else:
            id = db.read_transaction(get_next_id)['max']
        result = db.write_transaction(create_user, int(id), nombre, apellidos, username, password)
        user = result['user']
        return serialize_user(user), 201

class Login(Resource):
    def post(self):
        def get_user_by_username(tx, username):
            return tx.run(
                '''
                MATCH (user:User {username: $username})
                OPTIONAL MATCH (user)-[r:RATED]->(m:Movie) RETURN user, count(r) as cnt
                ''', {'username': username}
            ).single()

        inp = request.get_json()
        username = inp['user']
        password = inp['pass']
        password = password.encode("utf-8")
        password = base64.b64encode(password)

        db = get_db()
        result = db.read_transaction(get_user_by_username, username)

        if result and result.get('user'):
            user = result['user']
            pas = user['password']
            cnt = result['cnt']
            if str(pas) == str(password):
                return serialize_user(user, cnt), 200
            else:
                return {'error': "Contraseña incorrecta"}, 400
        else:
            return {'error': "El usuario no existe"}, 400

class TopMoviesByGenre(Resource):
    def get(self):
        def get_top_movies(tx):
            return list(tx.run(
                '''
                match(u:User)-[j:RATED]->(m:Movie)-[r:OF_GENRE]->(g:Genre)
                with m, g, count(j) as nr
                order by nr desc
                return g.class as genre, collect(m)[0..4] as movies
                '''
            ))

        db = get_db()
        result = db.read_transaction(get_top_movies)

        serialized = [serialize_top_movie(record['genre'], record['movies'])  for record in result]
        final = []
        def search_movie(lista, movie):
            for i in lista:
                if i['id'] == movie['id']:
                    return False
            return True

        for serie in serialized:
            for elem in serie:
                if search_movie(final, elem):
                    final.append(elem)

        random.shuffle(final)
        return final, 200

class RateMovie(Resource):
    def post(self):
        def rate_movie(tx, id, username, rating):
            return tx.run(
                '''
                MATCH (u:User), (m:Movie)
                WHERE u.username = $username AND m.id = $id
                MERGE (u)-[r:RATED]->(m)
                SET r.score = toFloat($rating)
                return u.username as username, r.score as rating, m.id as id
                ''',
                {
                'id': int(id),
                'username': username,
                'rating': rating
                }
            ).single()

        inp = request.get_json()
        username = inp['user']
        id = inp['id']
        rating = inp['rating']

        db = get_db()
        result = db.write_transaction(rate_movie, id, username, rating)
        return serialize_rating(result['username'], result['id'], result['rating']), 200

class RatedMovies(Resource):
    def post(self):
        def get_rated_movies(tx, username):
            return list(tx.run(
                '''
                match (m:Movie)-[:OF_GENRE]->(g:Genre), (m)<-[:ACTED_IN]-(a:Actor), (m)<-[:DIRECTED]-(d:Director),
                (m)-[:OF_COUNTRY]-(c:Country), (u:User)-[r:RATED]->(m)
                where u.username = $username
                return m as movie ,collect(distinct g.class) as genres,collect( distinct a.name) as actors,
                collect(distinct d.name) as directors, c.name as country, r.score as rating
                ''',
                {
                'username': username
                }
            ))

        inp = request.get_json()
        username = inp['user']

        db = get_db()
        result = db.read_transaction(get_rated_movies, username)
        return [serialize_movie(record['movie'], record['genres'], record['actors'], record['directors'], record['country'], my_rating =record['rating']) for record in result]

class Search(Resource):
    def post(self):
        def search(tx, pattern, username):
            return list(tx.run(
                '''
                match (m:Movie)-[:OF_GENRE]->(g:Genre), (m)<-[r:RATED]-(u:User)
                where toLower(m.title) contains $p or toLower(g.class) contains $p
                with m , count(r) as cnt
                order by cnt desc limit 50
                match (m)-[:OF_GENRE]->(g:Genre), (m)<-[:ACTED_IN]-(a:Actor), (m)<-[:DIRECTED]-(d:Director), (m)-[:OF_COUNTRY]-(c:Country)
                OPTIONAL MATCH (u1:User {username:$username})-[k:RATED]->(m:Movie)
                return distinct m as movie ,collect(distinct g.class) as genres,collect( distinct a.name) as actors,
                collect(distinct d.name) as directors, c.name as country, k.score as rating
                ''',
                {
                    'p': pattern.lower(),
                    'username': username
                }
            ))

        inp = request.get_json()
        pattern = inp['pattern']
        username = inp['user']

        db = get_db()
        result = db.read_transaction(search, pattern, username)
        return [serialize_movie(record['movie'], record['genres'], record['actors'], record['directors'], record['country'], record['rating']) for record in result]

class Recommend(Resource):
    def post(self):
        def get_rated_movies(tx, username):
            return list(tx.run(
                '''
                match (m:Movie)-[:OF_GENRE]->(g:Genre), (m)<-[:ACTED_IN]-(a:Actor), (m)<-[:DIRECTED]-(d:Director),
                (m)-[:OF_COUNTRY]-(c:Country), (u:User)-[r:RATED]->(m)
                where u.username = $username
                return m as movie ,collect(distinct g.class) as genres,collect( distinct a.id) as actors,
                collect(distinct d.id) as directors, c.name as country, r.score as rating
                ''',
                {
                'username': username
                }
            ))

        def get_all_movies(tx):
            return list(tx.run(
                '''
                match (m:Movie)-[:OF_GENRE]->(g:Genre), (m)<-[:DIRECTED]-(d:Director),
                (m)-[:OF_COUNTRY]-(c:Country), (m)<-[:ACTED_IN]-(a:Actor)
                return m as movie ,collect(distinct g.class) as genres,
                collect(distinct d.id) as directors, c.name as country, collect( distinct a.id) as actors, collect(distinct d.name) as directors_name
                '''
            ))

        def get_rated_movies_cf(tx, username):
            return list(tx.run(
                '''
                match (u:User)-[r:RATED]->(m:Movie)
                where u.username = $username
                return collect({id: m.id, score: r.score}) as ratings, u.id as id
                ''',
                {
                'username': username
                }
            ))

        def get_similar_users(tx, username):
            return list(tx.run(
                '''
                match(u:User)-[r:RATED]->(m:Movie)
                where u.username = $username
                with r,m, collect(m.title) as titles,u
                match(u1:User)-[r2:RATED]->(m2:Movie)
                where m2.title in titles and u1<>u
                with u1, count(r2) as cnt
                with u1,cnt
                order by cnt desc limit 100
                match(u1)-[rr:RATED]->(j:Movie)
                return u1.id as id, collect({id : j.id, score: rr.score}) as ratings
                ''',
                {
                    'username': username
                }
            ))


        def recommend_content_based(db, username, number):
            def create_profile(rated_df):
                profile = dict()

                def create_dict_profile(x, profile):
                    genres = x['genres']
                    directors = x['directors']
                    country = x['country']
                    for genre in genres:
                        if genre not in profile:
                            profile[genre] = [x['rating'], 1]
                        else:
                            rating, count = profile[genre]
                            profile[genre] = [rating + x['rating'], count + 1]

                    for director in directors:
                        if director not in profile:
                            profile[director] = [x['rating'], 1]
                        else:
                            rating, score = profile[director]
                            profile[director] = [rating + x['rating'], score + 1]

                    if country not in profile:
                        profile[country] = [x['rating'],1]
                    else:
                        rating, score = profile[country]
                        profile[country] = [rating + x['rating'], score + 1]

                def normalize_profile(profile):
                    for key, value in profile.items():
                        profile[key] = round(value[0]/(value[1]*5),3)

                rated_df.apply(create_dict_profile, profile = profile,axis=1)
                normalize_profile(profile)
                return profile

            def generate_movies_matrix(movies_df):
                def create_mix(x):
                    return ' '.join(x['genres']) + ' ' + x['country'] + ' ' + ' '.join(x['directors'])

                movies_df['mix'] = movies_df.apply(create_mix, axis=1)

                count = CountVectorizer()
                count_matrix = count.fit_transform(movies_df['mix'])
                return count_matrix.toarray(), count



            result = db.read_transaction(get_rated_movies, username)
            rated_movies = [serialize_movie(record['movie'], record['genres'], record['actors'], record['directors'],
            record['country'], record['rating']) for record in result]
            rated_df = pd.DataFrame(rated_movies)
            rated_df.drop(['imdbID', 'picture', 'year', 'actors'], axis = 1, inplace = True)

            profile = create_profile(rated_df)

            result = db.read_transaction(get_all_movies)
            all_movies = [serialize_movie(record['movie'], record['genres'], record['actors'], record['directors'], record['country'], directors_name=record['directors_name']) for record in result]
            all_df = pd.DataFrame(all_movies)
            count_matrix, count = generate_movies_matrix(all_df)


            feat_dict=count.get_feature_names()

            vector_perfil = dict(zip(feat_dict, [0 for elem in feat_dict]))

            for key, value in profile.items():
                vector_perfil[key.lower()] = value

            cosine_sim2 = cosine_similarity([list(vector_perfil.values())], count_matrix)

            all_df['score'] = cosine_sim2[0]

            cond = rated_df['id']
            all_df = all_df[~all_df['id'].isin(cond)]
            return all_df

        def recommend_collaborative_filtering(db, username):
            def serialize_rated(id, ratings, lista):
                for rating in ratings:
                    lista.append([id, rating['id'], rating['score']])

            result = db.read_transaction(get_rated_movies_cf, username)
            lista_usuario = []
            id_usuario = result[0]['id']
            [serialize_rated(record['id'], record['ratings'], lista_usuario) for record in result]

            result = db.read_transaction(get_similar_users, username)
            [serialize_rated(record['id'], record['ratings'], lista_usuario) for record in result]

            movies_df = pd.DataFrame(lista_usuario, columns =['user_id', 'movie_id', 'rating'])

            ratings_matrix = pd.pivot_table(movies_df, values='rating', index='user_id', columns='movie_id')

            user = ratings_matrix.loc[id_usuario]
            user_valid = user.notna()
            valid_indexes = user_valid[user_valid==True].index

            ratings_matrix.drop([id_usuario], inplace = True)

            def app(x, user, valid_indexes):
                comparison = x
                comparison_valid = comparison.notna()
                val = comparison_valid[comparison_valid == True].index

                intersection = valid_indexes.intersection(val)

                prs,_ = pearsonr(user[intersection], comparison[intersection])
                return prs

            ratings_matrix['pearson'] = ratings_matrix.apply(app, user = user, valid_indexes = valid_indexes, axis = 1)

            k = 10

            top_k = ratings_matrix.nlargest(k, 'pearson')
            pearson_mean = pd.DataFrame(top_k['pearson'])
            top_k.drop('pearson', axis = 1, inplace = True)

            top_k['mean'] = top_k.mean(axis=1)
            pearson_mean = pearson_mean.join(top_k['mean'])
            top_k.drop('mean', axis = 1, inplace = True)

            top_k.drop(valid_indexes, axis = 1, inplace = True)
            print(pearson_mean.head())
            print(top_k.head())






        inp = request.get_json()
        username = inp['user']
        method = inp['method']
        number = inp['number']

        db = get_db()

        if method == "Basado en gustos propios":
            recommended_df = recommend_content_based(db, username, number)
            top_movies = recommended_df.nlargest(number, 'score')
            return [serialize_movie_pandas(row) for index,row in top_movies.iterrows()]
        elif method == "Basado en perfiles parecidos":
            recommended_df = recommend_collaborative_filtering(db,username)





api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(TopMoviesByGenre, "/top")
api.add_resource(RateMovie, "/rate")
api.add_resource(RatedMovies, "/rated_movies")
api.add_resource(Search, "/search")
api.add_resource(Recommend, "/recommend")

if __name__ == "__main__":
    app.run(debug=True)



