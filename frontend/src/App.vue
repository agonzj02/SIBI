<template>
  <v-app
    :style=color_fondo>
    <v-app-bar app v-if="logged" clipped-left src="./assets/banner.jpg">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" color="white"></v-app-bar-nav-icon>
      <v-toolbar-title class="display-1 font-weight-bold white--text" >iRate</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <v-btn fab small ml-10 color="white" @click="cerrarSesionDialog"> 
        <v-icon >mdi-logout-variant</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer
      app
      clipped
      v-if="drawer"
      dark
      src="./assets/banner.jpg"
      v-model="drawer"
    >
      <v-list-item two-line class=" 'px-0'">
        <v-list-item-avatar>
          <img src="./assets/icono.png" />
        </v-list-item-avatar>
      
       <v-list-item-content>
          <v-list-item-title>Bienvenido, {{nombreUsuario}}</v-list-item-title>
        </v-list-item-content>
        </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item @click="acciones(item)" v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title >{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-card-text class="title">¿Esta seguro que desa cerrar sesion?</v-card-text>
                </v-col>
              </v-row>

          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red" text @click="dialog = false">Cancelar</v-btn>
            <v-btn color="green" text @click="confirmarCierreSesion()">Confirmar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <v-main fluid>
      <router-view />
    </v-main>
    
  </v-app>
</template>

<script>
import { mapState, mapMutations} from 'vuex'
export default {
  name: "App",

  data() {
    return {
      drawer: null,
      dialog:false,
      items: [
        { title: "Recomendaciones", icon: "mdi-home-variant" },
        { title: "Buscar películas", icon: "mdi-movie" },
        { title: "Mis valoraciones", icon: "mdi-star-circle" },
      ]
    };
  },
  methods: {
    acciones(item){
      if(item.title == "Mis valoraciones"){
        this.$router.push('/valoraciones')
      }
      else if(item.title == "Buscar películas"){
        this.$router.push('/buscar')
      }
      else if(item.title == "Recomendaciones"){
        this.$router.push("/home")
      }
    },
    cerrarSesionDialog(){
      this.dialog=true

    },
    confirmarCierreSesion(){
      this.deslogearse()
      this.drawer=false
      this.dialog=false
      this.$router.push('/login')
      
    },
    ...mapMutations(['deslogearse'])
  },
  computed: {

    color_fondo(){
      if(!this.logged){
        return "background: rgb(136,22,42);background: linear-gradient(90deg, rgba(136,22,42,1) 0%, rgba(253,29,29,1) 40%, rgba(214,125,125,1) 94%);"
      }
      else{
        return "background-color: #000;"
      }
    },
    ...mapState(['logged','nombreUsuario'])
  }
};
</script>