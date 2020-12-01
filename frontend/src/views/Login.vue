<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/movie.png')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3 white--text">
          Bienvenido a iRate
        </h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-row justify="center">
          <v-alert dismissible type="error" v-if="alerta">
            <v-row>
              <v-col>
                <span class="font-weight-black"
                  >La contraseña/usuario no son correctos.</span
                >
              </v-col>
            </v-row>
          </v-alert>
        </v-row>
        <v-row justify="center" wrap>
          <v-form>
            <v-row xs12 sm6>
              <v-text-field
                v-model="user"
                name="email-sin"
                label="Nombre de usuario"
                id="email-sin"
                type="email"
                required
                dark
                prepend-icon="mdi-account-circle"
              ></v-text-field>
            </v-row>
            <v-row xs12 sm6>
              <v-text-field
                v-model="password"
                name="password"
                label="Contraseña"
                id="password-sin"
                type="password"
                dark
                required
                prepend-icon="mdi-fingerprint"
                @keydown.native.enter="iniciar"
              ></v-text-field>
            </v-row>
            <v-row>
              <v-col xs12 sm6>
                <v-btn @click="iniciar" color="white" light
                  >Iniciar Sesión</v-btn
                >
              </v-col>
              <v-col xs12 sm6>
                <router-link to="/Registro" tag="button"
                  ><v-btn color="white" light
                    >¿No tienes cuenta? Regístrate</v-btn
                  ></router-link
                >
              </v-col>
            </v-row>
          </v-form>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
const axios = require("axios");
import { mapState, mapMutations } from "vuex";
export default {
  name: "Login",
  data: () => ({
    password: "",
    user: "",
    alerta: false,
  }),
  computed: {
    ...mapState(["logged", "nombreUsuario", "IP"]),
  },
  methods: {
    iniciar() {
      if (this.user != "" && this.password != "") {
        const userData = {
          user: this.user,
          pass: this.password,
        };
        axios
          .post(this.IP + "/login", userData)
          .then((response) => {
            let user = response.data;
            this.setNombreUsuario(user["username"]);
            if (user["num_rated"] != 0) {
              this.logearse();
              this.$router.push("/home");
            } else {
              this.logearse();
              this.$router.push("/inicial");
            }
          })
          .catch((error) => {
            console.log(error)
            this.password = "";
            this.user = "";
            this.visibleAlerta = true;
          });
      }
    },
    ...mapMutations(["logearse", "setNombreUsuario"]),
  },
};
</script>