<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img :src="require('../assets/logo.png')" class="my-3" contain height="200" />
      </v-col>

      

      <v-col cols="12">
        <v-row justify="center" mb-5>
          <p class="font-weight-bold font-italic white--text">*Todos los campos son obligatorios.</p>
        </v-row>
        <v-row justify="center">
          <form>
            <v-row>
              <v-text-field
                name="nombre"
                v-model="nombre"
                label="Nombre"
                id="nombre"
                type="nombre"
                required
                dark
                prepend-icon="mdi-account-circle"
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                name="apellidos"
                v-model="apellidos"
                label="Apellidos"
                id="apellidos"
                type="apellidos"
                required
                dark
                prepend-icon="mdi-account-circle"
              ></v-text-field>
            </v-row>
            <v-row xs12 sm6>
              <v-text-field
                v-model="user"
                name="email-sin"
                label="Nombre de usuario"
                id="email-sin"
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
                required
                dark
                prepend-icon="mdi-fingerprint"
              ></v-text-field>
            </v-row>
            <v-row xs12 sm6>
              <v-text-field
                v-model="password1"
                :rules="[v => !!v || 'La contraseña es necesaria.',
                v => v==this.password || 'Tiene que ser iguales']"
                name="password1"
                label="Repetir Contraseña"
                id="password-sin2"
                type="password"
                required
                dark
                prepend-icon="mdi-fingerprint"
              ></v-text-field>
            </v-row>
            <v-alert :value="visibleAlerta" justify-center type="error" height="40" dense>Ese usuario ya ha sido registrado.</v-alert>
            <v-row>
              <v-col xs12 sm6>
                <v-btn @click="confirmaRegistro" type="submit"  color="white" light>Confirmar</v-btn>
              </v-col>
              <v-col xs12 sm6>
                <router-link to="/Login" tag="button">
                  <v-btn color="white" light>¿Ya tienes cuenta? Inicia sesión</v-btn>
                </router-link>
              </v-col>
            </v-row>
          </form>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
const axios = require("axios");
import { mapState } from "vuex";
export default {
  name: "Register",

  data: () => ({
    nombre: "",
    apellidos: "",
    user: "",
    visibleAlerta: false,
    password: "",
    password1: "",
  }),
  computed: {
    ...mapState(['IP'])
  },
  methods: {
    confirmaRegistro() {
      if (this.nombre != "" && this.apellidos != "" && this.user != "" && this.password != "" && this.password1 != "" && this.password.localeCompare(this.password1)==0) {
        const userData = {
          nombre: this.nombre,
          apellidos: this.apellidos,
          user: this.user,
          pass: this.password
        };

        axios.post(this.IP + "/register", userData).then(
          response => {
            if (Object.prototype.hasOwnProperty.call(response.data, "error")) {
              this.visibleAlerta = true;
            } else {
              this.$router.push('Login')
            }
          }
        ).catch(error => {
          this.visibleAlerta = true;
        })
          ;
      }
    }
  }
};
</script>