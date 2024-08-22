import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import BridgeView from "@/views/BridgeView.vue";
import TripView from "@/views/TripView.vue";
import TripCreateView from "@/views/TripCreateView.vue";
import TripProgressView from "@/views/TripProgressView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: TripView
    },
    {
      path: "/bridge",
      name: "bridge",
      component: BridgeView,
    },
    {
      path: "/create",
      name: "createTrip",
      component: TripCreateView,
    },
    {
      // path: "/trip/:tripId",
      path: "/trip/progress",
      name: "progresstrip",
      component: TripProgressView,
    },
  ]
});

export default router;
