import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

export const useStateStore = defineStore('states', {
  state: () => ({
    travel: false,
    
  }),

  getters: {
    isTraveling(state) {
      return state.travel
    }
  },

  actions: {
    toggleTrip() {
      this.travel = !this.travel;
      return this.travel
    }
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'stateStore',
        storage: sessionStorage,
      },
    ],
  },  
});