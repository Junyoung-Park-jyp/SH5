import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import BridgeView from "@/views/BridgeView.vue";
import TripView from "@/views/TripView.vue";
import TripCreateView from "@/views/TripCreateView.vue";
import TripMainView from "@/views/TripMainView.vue";
import TripDetailView from "@/views/TripDetailView.vue";
import TripFinishView from "@/views/TripFinishView.vue";
import LoadingMessage from '@/components/TripCreateView/LoadingMessage.vue';
import InsuranceView from '@/views/InsuranceView.vue';
import GalleryView from "@/views/GalleryView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: TripView,
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
    {
      // path: "/trip/:tripId",
      path: "/trip/finish",
      name: "tripFinish",
      component: TripFinishView,
    },
    {
      path: '/loading-message/:message/:status',
      name: 'loadingMessage',
      component: LoadingMessage,
      props: true,
    },
    {
      path: '/insurance',
      name: 'insurance',
      component: InsuranceView,
    },
    {
      path: '/gallery',
      name: 'gallery',
      component: GalleryView,
      props: true,
    },
    // {
    //   path: '/gallery/:id',
    //   name: 'gallery',
    //   component: GalleryView,
    //   props: true,
    // }
  ]
});

export default router;
