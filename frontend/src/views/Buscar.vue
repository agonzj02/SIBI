<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <div>
          <v-card dark dense height="70px">
            <v-text-field
              label="Buscar"
              placeholder="Títulos, personas, géneros"
              append-outer-icon="mdi-send"
              @click:append-outer="buscar"
            ></v-text-field>
          </v-card>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="3" v-for="item in peliculas" :key="item.id">
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
          :inicial="true"
          :width="300"
          :height="400"
          :rating="item.rating"
          @addReview="addReview"
        ></Pelicula>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Pelicula from "@/components/Pelicula.vue";
import { mapState, mapMutations } from "vuex";

export default {
  name: "Buscar",
  components: {
    Pelicula,
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
        rating: 3.5,
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
        rating: 2.5,
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
        rating: 5.0,
      },
    ],
  }),
  methods: {
    buscar(){
      this.peliculas.push({
        id: 3239,
        title: "Ella es unica",
        imdbID: "0141399",
        picture: "http://content7.flixster.com/movie/28/13/281397_det.jpg",
        country: "USA",
        director: "Joe Johnston",
        actors: ["Robin Williams", "James Handy", "Bebe Neuwirth"],
        genre: ["Adventure", "Fantasy", "Children"],
        year: 1980,
        rating: 5.0
      }
      )
    },
    addReview(rating, id) {
      for (var i = 0; i < this.peliculas.length; i++) {
        if (this.peliculas[i].id == id) {
          this.peliculas[i].rating = rating;
        }
      }
    },
  },
  computed:{
    ...mapState(["IP"]),
  }
};
</script>