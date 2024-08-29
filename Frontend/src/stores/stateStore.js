import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

export const useStateStore = defineStore('states', {
  state: () => ({
    travel: false,
    apiKey: null,
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
    },

    async getAILABapi() {
      try {
        const response = await axiosInstance.get('/keys/')

        if (response) {
          this.apiKey = response.data.data.key
          console.log(this.apiKey)
        }
      } catch (error) {
        console.error('apikey 호출 실패', error)
      }
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