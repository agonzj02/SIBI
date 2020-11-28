<template>
  <v-card class="mx-auto" :max-width="width">
    <v-img :src="picture" :width="width" :height="height"></v-img>
    <v-card-title>
      {{ title }}
    </v-card-title>
    <div v-if="inicial">
      <v-card-subtitle> {{ generos }} </v-card-subtitle>

      <v-card-actions>
        <v-btn color="orange lighten-2" text @click="show = !show">
          Explorar
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn icon @click="show = !show">
          <v-icon>{{ show ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
        </v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="show">
          <v-divider></v-divider>

          <v-card-text>
            <div>Director : {{ directores }}</div>
            <div class="mt-2">País : {{ country }}</div>
            <div class="mt-2">Año : {{ year }}</div>
            <div class="mt-2">
              <v-btn
                class="ma-2"
                outlined
                color="red"
                :href="link"
                target="_blank"
              >
                Link IMDB
              </v-btn>
            </div>
          </v-card-text>
        </div>
      </v-expand-transition>
      <v-divider dark></v-divider>
    </div>
    <v-card-actions class="pa-4">
      <span class="grey--text text--lighten-2 caption mr-2">
        ({{ rating_aux }})
      </span>
      <v-rating
        v-model="rating_aux"
        background-color="black"
        color="yellow accent-4"
        dense
        half-increments
        hover
        size="18"
      ></v-rating>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from "vuex";
const axios = require("axios");

export default {
  name: "Pelicula",
  props: [
    "title",
    "imdbID",
    "picture",
    "country",
    "director",
    "actors",
    "genre",
    "id",
    "year",
    "inicial",
    "width",
    "height",
    "rating",
  ],
  data: () => ({
    clicked: false,
    show: false,
    rating_aux: null,
  }),
  mounted: function () {
    this.iniciar_rating_aux();
  },
  watch: {
    // whenever question changes, this function will run
    rating_aux: function () {
      if (!this.clicked) {
        this.clicked = true;
      }
      const data = {
        user: this.nombreUsuario,
        id: this.id,
        rating: this.rating_aux
      }
      axios.post(this.IP + "/rate", data)

      this.addReview()
    },
  },
  methods: {
    addReview() {
      if (!this.clicked) {
        this.clicked = true;
      }
      this.$emit("addReview", this.rating_aux, this.id);
    },
    iniciar_rating_aux() {
      this.rating_aux = this.rating;
    },
  },
  computed: {
    generos() {
      var string = "";
      for (var i = 0; i < this.genre.length; i++) {
        string += this.genre[i];
        if (i != this.genre.length - 1) {
          string += ", ";
        }
      }
      return string;
    },
    actores() {
      var string = "";
      for (var i = 0; i < this.actors.length; i++) {
        string += this.actors[i];
        if (i != this.actors.length - 1) {
          string += ", ";
        }
      }
      return string;
    },
    directores() {
      var string = "";
      for (var i = 0; i < this.director.length; i++) {
        string += this.director[i];
        if (i != this.director.length - 1) {
          string += ", ";
        }
      }
      return string;
    },
    link() {
      return "https://www.imdb.com/title/tt" + this.imdbID + "/";
    },
    ...mapState(["IP", "nombreUsuario"]),
  },
};
</script>