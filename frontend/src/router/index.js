import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue'),
    meta: {
      hideForAuth: true
    }
  },
  {
    path: '/registro',
    name: 'Registo',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue'),
    meta: {
      hideForAuth: true
    }
  },
  {
    path: '/inicial',
    name: 'Inicial',
    component: () => import(/* webpackChunkName: "about" */ '../views/Inicial.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/valoraciones',
    name: 'Valoraciones',
    component: () => import(/* webpackChunkName: "about" */ '../views/Valoraciones.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/buscar',
    name: 'Buscar',
    component: () => import(/* webpackChunkName: "about" */ '../views/Buscar.vue'),
    meta: {
      requiresAuth: true
    }
  },
  { path: '/', redirect: '/login' },
  { path: '*', redirect: '/login' },
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.logged) {
      next({ path: '/login' });
    } else {
      next();
    }

  } else {
    next();
  }

  if (to.matched.some(record => record.meta.hideForAuth)) {
    if (store.state.logged) {
      next({ path: '/home' });
    } else {
      next();
    }
  } else {
    next();
  }
})

export default router
