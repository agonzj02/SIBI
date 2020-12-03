<template>
  <v-container>
    <v-row>
      <v-col>
        <div>
          <p class="font-weight-black text-center white--text text-h4">
            {{ nombreUsuario }}, valora al menos 5 películas que hayas visto.
          </p>
          <p class="text-center white--text text-h6">
            Así podremos encontrar películas que te gusten
          </p>
          <div class="text-center">
            <v-btn x-large color="success" dark @click="continuar">
              Continuar
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col sm="4" md="3" lg="2" v-for="item in peliculas" :key="item.id">
        <Pelicula
          :title="item.title"
          :id="item.id"
          imdbID=""
          :picture="item.picture"
          year=""
          country=""
          director=""
          actors=""
          :genre="item.genre"
          :inicial="false"
          :width="300"
          :height="400"
          :rating="null"
          @addReview="addReview"
        ></Pelicula>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Pelicula from "@/components/Pelicula.vue";
import Alerta from "@/components/Alerta.vue";
import { mapState, mapMutations } from "vuex";
const axios = require("axios");

export default {
  name: "Inicial",
  components: {
    Pelicula,
    Alerta,
  },
  data: () => ({
    peliculas: [],
    reviewed: 0,

    cambiar: false,
  }),
  mounted: function () {
    this.obtenerPeliculas();
  },
  computed: {
    ...mapState(["logged", "nombreUsuario", "IP"]),
  },
  methods: {
    continuar() {
      if (this.reviewed >= 5) {
        this.$router.push("/buscar");
      }
    },
    addReview(rating, id) {
      this.reviewed++;
      for (var i = 0; i < this.peliculas.length; i++) {
        if (this.peliculas[i].id == id) {
          this.peliculas[i].rating = rating;
        }
      }
    },
    obtenerPeliculas() {
      this.peliculas = [];
      axios.get(this.IP + "/top").then((response) => {
        this.peliculas = response.data;
      });
    },
  },
};
</script>