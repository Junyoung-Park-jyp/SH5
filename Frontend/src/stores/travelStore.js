import { defineStore } from 'pinia';

export const useTravelStore = defineStore('travel', {
  state: () => ({
    country: '',
    exchangeRate: null,
    members: [],
  }),

  getters: {
    travelCountry(state) {
      return state.country;
    },
    travelExchangeRate(state) {
      return state.exchangeRate;
    },
    travelMembers(state) {
      return state.members
    }
  },

  actions: {
    setTravel(travelData) {
      this.country = travelData.country;
      this.exchangeRate = travelData.exchangeRate;
      this.members = travelData.members;
    },

    clearTravel() {
      this.country = '';
      this.exchangeRate = null;
      this.members = [];
    },
  },
});