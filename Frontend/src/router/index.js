import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import BridgeView from "../views/BridgeView.vue";
import TripView from "../views/TripView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/bridge",
      name: "bridge",
      component: BridgeView,
    },
    {
      path: "/trip",
      name: 'trip',
      component: TripView,
    },
  ],
});

export default router;
