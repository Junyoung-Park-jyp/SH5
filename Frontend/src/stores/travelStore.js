import { defineStore } from 'pinia';

export const useTravelStore = defineStore('travel', {
  state: () => ({
    travelId: null,
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
    async makeTravel(travelData) {
      try {
        const response = await axiosInstance.post('/travel', {
          country: travelData.country,
          members: travelData.members,
          apiKey: this.apiKey,
          startDate: travelData.startDate,
          endDate: travelData.endDate,
          adjustTime: travelData.adjustTime,
        });

        const travelId  = response.data;

        this.travelId = travelId;
        this.members = travelData.members; 
        this.startDate = travelData.startDate;
        this.endDate = travelData.endDate,
        this.adjustTime = travelData.adjustTime,

      } catch (error) {
        console.error('로그인 실패:', error);
      }
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