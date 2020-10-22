<template>
  <v-container>
    <v-row>
      <v-col>
        <div>
          <p class="font-weight-black text-center text-h4">
            Prueba, valora al menos 3 películas que te gustan.
          </p>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="2" v-for="item in peliculas" :key="item.id">
        <Pelicula
          :title="item.title"
          :id="item.id"
          :imdbID="item.imdbID"
          :picture="item.picture"
          :year="item.year"
          :country="item.country"
          :director="item.director"
          :actors="item.actors"
          :genre="item.genre"
          :inicial="false"
          :width="180"
          :height="268"
          @addReview="reviewed++"
        ></Pelicula>
      </v-col>
    </v-row>
    <div v-if="cambiar">
      <Alerta />
    </div>
  </v-container>
</template>

<script>
import Pelicula from "@/components/Pelicula.vue";
import Alerta from "@/components/Alerta.vue";

export default {
  name: "Inicial",
  components: {
    Pelicula,
    Alerta,
  },
  watch: {
    reviewed: function () {
      if (this.reviewed == 5) {
        this.cambiar = true;
      }
    },
  },
  data: () => ({
    peliculas: [
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
      {
        id: 11,
        title: "Jumanji",
        imdbID: "0113497",
        picture: "http://content8.flixster.com/movie/56/79/73/5679734_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2010,
      },
      {
        id: 804,
        title: "Ella es unica",
        imdbID: "0117628",
        picture: "http://content9.flixster.com/movie/27/16/271699_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 2000,
      },
      {
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
      },
    ],
    reviewed: 0,

    cambiar: false,
  }),
};
</script>

<style lang="css" scoped>
.p {
  font-size: 0.8em;
  font-weight: 100;
}
</style>