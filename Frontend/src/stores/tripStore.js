import { defineStore } from 'pinia';
import { watch } from 'vue';
import axiosInstance from '@/axios';

export const useTripStore = defineStore('trip', {
  state: () => ({
    travelId: null,
    country: null,
    exchangeRate: null,
    members: [],
    startDate: null,
    endDate: null,
    adjustTime: null,

    // 다녔던 여행들 더미 데이터
    travelExperiences: [
      {country: '제주도', cost: 963500},
      {country: '파리', cost: 3572600},
      {country: '오키나와', cost: 1572600},
      {country: '부산', cost: 678830},
    ],
    stage: 0,
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
    tripFormStage(state) {
      return state.stage
    }
  },

  actions: {
    clearTravel() {
      this.country = '';
      this.exchangeRate = null;
      this.members = [];
      this.startDate = null;
      this.endDate = null;
      this.adjustTime = null;
    },

    setTravel(travelData) {
      this.country = travelData.country;
      this.members = travelData.members;
      this.startDate = travelData.startDate;
      this.endDate = travelData.endDate;
      this.adjustTime = travelData.adjustTime;
    },

    async makeTravel(travelData) {
      try {
        const response = await axiosInstance.post('/trips/', {
          travelData
        });
        if (response.data.REC) {
          const travelId  = response.data;
          this.travelId = travelId;
          this.setTravel(travelData)
          console.log('여행 생성 성공')
        } else {
          console.error('여행 데이터 전송 실패')
        }
      } catch(error) {
        console.error('여행 생성 실패:', error);
      }
    },

    async deleteTravel(travelId) {
      try {
        const response = await axiosInstance.delete(`/trips/`)

        if (response.data.REC) {
          this.clearTravel()
          console.log('여행 삭제 성공')
        }
      } catch(error) {
        console.error('여행 삭제 실패:', error)
      }
    },

    async editTravel(travelId, travelData) {
      try {
        const response = await axiosInstance.put(`/trips/`, travelData)
  
        if (response.data.REC) {
          this.setTravel(travelData)
        }
      } catch(error) {
        console.error('여행 정보 수정 실패:', error)
      }
    },
  },
});
