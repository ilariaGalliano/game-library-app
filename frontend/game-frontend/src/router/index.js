import { createRouter, createWebHistory } from "vue-router";
import Games from "../components/Games.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import HomePage from "../components/HomePage.vue";
import NewGame from "../components/NewGame.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/games",
    name: "Games",
    component: Games,
    meta: { requiresAuth: true },
  },
  {
    path: "/new-games",
    name: "NewGame",
    component: NewGame,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
