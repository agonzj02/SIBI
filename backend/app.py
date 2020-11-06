import pandas as pd
import numpy as np
import os
import ast
import base64

from dotenv import load_dotenv, find_dotenv

from flask import Flask, request, abort, request_started, g
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_json import FlaskJSON, JsonError, json_response, as_json

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)
FlaskJSON(app)

api = Api(app)

def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
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

def serialize_movie(movie, genres, actors, directors, country, my_rating=None):
    return {
        'id': movie['id'],
        'imdbID': movie['imdbID'],
        'title': movie['title'],
        'picture': movie['picture'],
        'year' : 1980,
        'genres' : genres,
        'actors' : actors,
        'directors': directors,
        'country': country,
        'rating' : my_rating
    }

def serialize_user(user, num_rated=None):
    return{
        'id': user['id'],
        'nombre': user['nombre'],
        'apellidos': user['apellidos'],
        'username': user['username'],
        'num_rated': num_rated
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
        password = inp['password']
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
                OPTIONAL MATCH (m)-[r:RATED]->(m:Movie) RETURN user, count(r) as cnt
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


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)



