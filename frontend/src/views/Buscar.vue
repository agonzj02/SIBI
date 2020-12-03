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
              @keydown.native.enter="buscar"
            ></v-text-field>
          </v-card>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col sm="4" md="3" lg="2" v-for="item in peliculas" :key="item.id">
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

    <v-row>
      <v-dialog v-model="dialog" hide-overlay :persistent="true" width="300">
        <v-card color="red darken-4" dark>
          <v-card-text class="text-center">
            Espere mientras cargan las películas...
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-progress-circular
              indeterminate
              color="white"
              class="mb-0"
            ></v-progress-circular>
          </v-card-actions>
        </v-card>
      </v-dialog>
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
    dialog: false,
  }),
  mounted: function () {
    this.obtenerPeliculas();
  },
  methods: {
    obtenerPeliculas() {
      const data = {
        user: this.nombreUsuario,
      };
      this.dialog = true
      this.peliculas = [];
      axios.post(this.IP + "/top", data).then((response) => {
        this.peliculas = response.data;
        this.dialog = false
      });
    },
    buscar() {
      const data = {
        pattern: this.pattern,
        user: this.nombreUsuario,
      };
            this.dialog = true
      axios.post(this.IP + "/search", data).then((response) => {
        this.peliculas = [];
        this.peliculas = response.data;
        this.dialog = false
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