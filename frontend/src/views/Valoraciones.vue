<template>
  <v-container fluid>
    <v-row wrap>
      <v-col>
        <div>
          <v-card dark>
            <v-card-title>
              Selecciona en base a qué quieres ordenar las películas que has
              valorado
            </v-card-title>
            <v-select
              :items="criterios"
              v-model="criterio"
              dark
              outlined
              dense
              @input="ordenar"
            ></v-select>
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
  name: "Valoraciones",
  components: {
    Pelicula,
  },
  data: () => ({
    criterios: [
      "Mejor valoradas primero",
      "Peor valoradas primero",
      "Más nuevas primero",
      "Más antiguas primero",
      "Orden alfabético(A-Z)",
      "Orden alfabético(Z-A)"
    ],
    criterio: "Mejor valoradas primero",
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
    ordenar() {
      if (this.criterio == "Mejor valoradas primero") {
        this.ordenar_mejor_valoradas();
      } else if (this.criterio == "Peor valoradas primero") {
        this.ordenar_mejor_valoradas();
        this.peliculas.reverse();
      }
      else if(this.criterio == "Más nuevas primero"){
        this.ordenar_mas_nuevas()
      }
      else if(this.criterio == "Más antiguas primero"){
        this.ordenar_mas_antiguas()
      }
      else if(this.criterio == "Orden alfabético(A-Z)"){
        this.ordenar_alfabetico_a()
      }
      else if(this.criterio == "Orden alfabético(Z-A)"){
        this.ordenar_alfabetico_z()
      }
    },
    ordenar_mejor_valoradas() {
      this.peliculas.sort(function (a, b) {
        var rate_a = a.rating;
        var rate_b = b.rating;
        return rate_a > rate_b ? -1 : rate_a < rate_b ? 1 : 0;
      });
    },
    ordenar_peor_valoradas() {
      this.ordenar_mejor_valoradas();
      this.peliculas.reverse();
    },
    ordenar_mas_nuevas() {
      this.peliculas.sort(function (a, b) {
        var year_a = a.year;
        var year_b = b.year;
        return year_a > year_b ? -1 : year_a < year_b ? 1 : 0;
      });
    },
    ordenar_mas_antiguas(){
      this.ordenar_mas_nuevas()
      this.peliculas.reverse()
    },
    ordenar_alfabetico_a(){
      this.peliculas.sort(function (a, b) {
        var year_a = a.title;
        var year_b = b.title;
        return year_a < year_b ? -1 : year_a > year_b ? 1 : 0;
      });
    },
    ordenar_alfabetico_z(){
      this.ordenar_alfabetico_a()
      this.peliculas.reverse()
    },
    addReview(rating, id) {
      for (var i = 0; i < this.peliculas.length; i++) {
        if (this.peliculas[i].id == id) {
          this.peliculas[i].rating = rating;
        }
      }
    },
  },
  computed: {
    ...mapState(["IP"]),
  },
};
</script>