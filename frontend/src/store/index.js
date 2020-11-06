import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    logged: false,
    nombreUsuario: 'Alvaro',
    IP: 'http://127.0.0.1:5000',
  },
  mutations: {
    logearse(state) {
      state.logged = true
    },
    deslogearse(state) {
      state.logged = false
      state.nombreUsuario = ''
    },
    setNombreUsuario(state, msg) {
      state.nombreUsuario = msg
    },
  },
  actions: {
  },
  modules: {
  }
})
