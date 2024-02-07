import { createRouter, createWebHistory } from "vue-router";
import Games from "../components/Games.vue";
import Login from "../components/Login.vue";

const routes = [
  {
    path: "/games",
    name: "Games",
    component: Games,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
