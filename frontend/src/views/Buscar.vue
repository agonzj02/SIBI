<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <div>
          <v-card dark dense height="70px">
            <v-text-field
              label="Buscar"
              v-model="pattern"
              placeholder="Títulos, géneros"
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
  name: "Buscar",
  components: {
    Pelicula,
  },
  data: () => ({
    peliculas: [],
    pattern: "",
  }),
  mounted: function () {
    this.obtenerPeliculas();
  },
  methods: {
    obtenerPeliculas() {
      const data = {
        pattern: "Accion",
        user: this.nombreUsuario,
      };
      this.peliculas = [];
      axios.post(this.IP + "/search", data).then((response) => {
        console.log(response.data);
        this.peliculas = response.data;
      });
    },
    buscar() {
      const data = {
        pattern: this.pattern,
        user: this.nombreUsuario,
      };
      axios.post(this.IP + "/search", data).then((response) => {
        this.peliculas = [];
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