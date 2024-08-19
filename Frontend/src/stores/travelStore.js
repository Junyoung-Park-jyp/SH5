import { defineStore } from 'pinia';

export const useTravelStore = defineStore('travel', {
  state: () => ({
    country: '',
    exchangeRate: null,
    members: [],
    startDate: null,
    endDate: null,
    adjustTime: null,
  }),

  getters: {
    country(state) {
      return state.country;
    },
    exchangeRate(state) {
      return state.exchangeRate;
    },
    members(state) {
      return state.members
    },
    
  },

  actions: {
    setTravel(travelData) {
      this.country = travelData.country;
      this.exchangeRate = travelData.exchangeRate;
      this.members = travelData.members;
      this.startDate = travelData.startDate;
      this.endDate = travelData.endDate;
      this.adjustTime = travelData.adjustTime;
    },

    clearTravel() {
      this.country = '';
      this.exchangeRate = null;
      this.members = [];
      this.startDate = null;
      this.endDate = null;
      this.adjustTime = null;
    },
  },
});