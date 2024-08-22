import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

export const useTripStore = defineStore('trip', {
  state: () => ({
    tripId: null,
    country: [],
    city: [],
    exchangeRate: null,
    members: [],
    startDate: null,
    endDate: null,
    adjustTime: null,

    // 다녔던 여행들 더미 데이터
    experiences: [
      {country: '대한민국', city: '제주도', cost: 963500},
      {country: '프랑스', city: '파리', cost: 3572600},
      {country: '일본', city: '오키나와', cost: 1572600},
      {country: '대한민국', city: '부산', cost: 678830},
    ],

    stage: 0,
    progressStage: 0,
  }),

  getters: {
    tripCountry(state) {
      return state.country;
    },
    tripExchangeRate(state) {
      return state.exchangeRate;
    },
    tripMembers(state) {
      return state.members.map(member => member.userName);
    },
    tripExperiences(state) {
      return state.experiences;
    },
    tripFormStage(state) {
      return state.stage
    },
    tripProgressStage(state) {
      return state.progressStage
    }
  },

  actions: {
    clearTrip() {
      this.country = [];
      this.city = [];
      this.exchangeRate = null;
      this.members = [];
      this.startDate = null;
      this.endDate = null;
      this.adjustTime = null;
    },

    setTrip(tripData) {
      this.country = tripData.country;
      this.members = tripData.members;
      this.startDate = tripData.startDate;
      this.endDate = tripData.endDate;
      this.adjustTime = tripData.adjustTime;
    },

    async makeTrip(tripData) {
      try {
        const response = await axiosInstance.post('/trips/', {
          tripData
        });
        if (response.data.REC) {
          const tripId  = response.data;
          this.tripId = tripId;
          this.setTrip(travelData)
          console.log('여행 생성 성공')
        } else {
          console.error('여행 데이터 전송 실패')
        }
      } catch(error) {
        console.error('여행 생성 실패:', error);
      }
    },

    async deleteTrip(tripId) {
      try {
        const response = await axiosInstance.delete(`/trips/`)

        if (response.data.REC) {
          this.clearTrip()
          console.log('여행 삭제 성공')
        }
      } catch(error) {
        console.error('여행 삭제 실패:', error)
      }
    },

    async editTrip(tripId, tripData) {
      try {
        const response = await axiosInstance.put(`/trips/`, tripData)
  
        if (response.data.REC) {
          this.setTrip(tripData)
        }
      } catch(error) {
        console.error('여행 정보 수정 실패:', error)
      }
    },
  },
});
