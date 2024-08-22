import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import BridgeView from "@/views/BridgeView.vue";
import TripView from "@/views/TripView.vue";
import TripCreateView from "@/views/TripCreateView.vue";
import TripMainView from "@/views/TripMainView.vue";
import TripDetailView from "@/views/TripDetailView.vue";

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
      path: "/trip/create",
      name: "createTrip",
      component: TripCreateView,
    },
    {
      path: "/trip",
      name: "trip",
      component: TripView,
    },
    {
      // path: "/trip/:tripId",
      path: "/trip/main",
      name: "tripMain",
      component: TripMainView,
    },
    {
      // path: "/trip/:tripId",
      path: "/trip/detail",
      name: "tripDetail",
      component: TripDetailView,
    },
  ]
});

export default router;
