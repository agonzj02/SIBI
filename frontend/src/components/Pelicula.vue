<template>
  <v-card class="mx-auto" max-width="344">
    <v-img :src="picture" height="275px"></v-img>

    <v-card-title>
      {{ title }}
    </v-card-title>

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

        <v-card-text >
          <div>Director : {{ director }}</div>
          <div class="mt-2">País : {{ country }}</div>
          <div class="mt-2">Año : {{ year }}</div>
          <div class="mt-2">
            <v-btn class="ma-2" outlined color="indigo" :href=link target="_blank">
              Link IMDB
            </v-btn>
          </div>
        </v-card-text>
      </div>
    </v-expand-transition>
    <v-divider dark></v-divider>
    <v-card-actions class="pa-4">
      Puntúa la película
      <v-spacer></v-spacer>
      <span class="grey--text text--lighten-2 caption mr-2">
        ({{ rating }})
      </span>
      <v-rating
        v-model="rating"
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
export default {
  name: "Pelicula",
  props: ['title','imdbID','picture','country','director','actors','genre','id','year'],
  data: () => ({
    show: false,
    rating: null,
  }),
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
    link() {
      return "https://www.imdb.com/title/tt" + this.imdbID + "/";
    },
  },
};
</script>