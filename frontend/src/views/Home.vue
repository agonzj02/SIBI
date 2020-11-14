<template>
  <v-container fluid>
    <v-row align="start" align-start>
      <v-col cols="12">
        <v-card elevation="24" class="mx-auto" dark>
          <v-carousel height="300" width="7500">
            <v-carousel-item
              v-for="(item, i) in items"
              :key="i"
              :src="item.src"
              reverse-transition="fade-transition"
              transition="fade-transition"
            ></v-carousel-item>
          </v-carousel>
          <v-divider></v-divider>
          <v-row>
            <v-col cols="6" class="ml-4 mr-5">
              <v-select
                v-model="algoritmo"
                :items="algoritmos"
                label="Selecciona un algoritmo de recomendacion"
              >
              </v-select>
            </v-col>
            <v-col cols="2"></v-col>
            <v-col cols="3" class="d-flex ml-5 mr-n7">
              <v-select
                v-model="numero"
                :items="numeros"
                label="Selecciona nº recomendaciones"
              >
              </v-select>
            </v-col>
          </v-row>
        </v-card>
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
          :director="item.directors"
          :actors="item.actors"
          :genre="item.genres"
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
const axios = require("axios");

export default {
  name: "Home",
  components: {
    Pelicula,
  },
  data: () => ({
    algoritmo: "Basado en gustos propios",
    algoritmos: ["Basado en gustos propios", "Basado en perfiles parecidos", "Híbrido"],
    numero: 5,
    numeros: [1, 5, 10, 15, 20],
    items: [
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
      },
    ],
    peliculas: [ ],
  }),
  mounted: function () {
    this.recomendar();
  },
  watch: {
    numero: function () {
      this.recomendar()
    },
    algoritmo: function () {
      this.recomendar()
    }
  },
  methods: {
    recomendar(){
      const data = {
        method: this.algoritmo,
        user: this.nombreUsuario,
        number: this.numero
      };
      this.peliculas = [];
      axios.post(this.IP + "/recommend", data).then((response) => {
        this.peliculas = response.data;
      });
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
    ...mapState(["IP", "nombreUsuario"]),
  },
};
</script>
