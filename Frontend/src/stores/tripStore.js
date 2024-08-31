import { defineStore } from "pinia";
import axiosInstance from "@/axios";

export const useTripStore = defineStore("trip", {
  state: () => ({
    pastTrips: [],
    futureTrips: [],
    tripId: null,
    tripName: null,
    country: [],
    city: [],
    locations: [],
    exchangeRate: null,
    members: [],
    startDate: null,
    endDate: null,
    adjustTime: null,
    payments: [],
    stage: 0,
    progressStage: 0,
    imageUrl: null
  }),

  getters: {
    getTripName(state) {
      return state.tripName;
    },
    tripCountry(state) {
      return state.country;
    },
    tripExchangeRate(state) {
      return state.exchangeRate;
    },
    tripMembers(state) {
      return state.members.map((member) => member.userName);
    },
    tripExperiences(state) {
      return state.experiences;
    },
    tripFormStage(state) {
      return state.stage;
    },
    tripProgressStage(state) {
      return state.progressStage;
    },
  },

  actions: {
    clearTrip() {
      this.tripName = null;
      this.country = [];
      this.city = [];
      this.locations = [];
      this.exchangeRate = null;
      this.members = [];
      this.startDate = null;
      this.endDate = null;
      this.adjustTime = null;
      this.imageUrl = null;
    },

    setTrip(tripData) {
      this.locations = tripData.locations;
      this.members = tripData.members;
      this.startDate = tripData.start_date;
      this.endDate = tripData.end_date;
      this.adjustTime = tripData.adjustTime;
      this.imageUrl = tripData.image_url
    },

    async makeTrip(tripData) {
      try {
        const response = await axiosInstance.post("/trips/", tripData);
        if (response) {
          console.log(response.data);
          const tripId = response.data.data.id;
          this.tripId = tripId;
          this.setTrip(tripData);
          console.log("여행 생성 성공");
        } else {
          console.error("여행 데이터 전송 실패");
        }
      } catch (error) {
        console.error("여행 생성 실패:", error);
      }
    },

    async deleteTrip(tripId) {
      try {
        const response = await axiosInstance.delete(`/trips/`);

        if (response) {
          this.clearTrip();
          console.log("여행 삭제 성공");
        }
      } catch (error) {
        console.error("여행 삭제 실패:", error);
      }
    },

    async editTrip(tripId, tripData) {
      try {
        const response = await axiosInstance.put(`/trips/`, tripData);

        if (response) {
          this.setTrip(tripData);
        }
      } catch (error) {
        console.error("여행 정보 수정 실패:", error);
      }
    },

    async getTrip(tripId) {
      console.log("tripId:", tripId);
      try {
        const response = await axiosInstance.get(`/trips/main/`, {
          params: { trip_id: tripId },
        });

        if (response) {
          console.log(response.data.data);
          this.setTrip(response.data.data);
          return response.data.data;
        }
      } catch (error) {
        console.error("여행 정보 조회 실패:", error);
      }
    },

    async getPastTrips() {
      try {
        const response = await axiosInstance.get("/trips/finish/");

        if (response) {
          console.log(response.data);

          this.pastTrips = response.data.data;
        }
      } catch (error) {
        console.error("과거 여행 조회 실패", error);
      }
    },

    async getFutureTrips() {
      try {
        const response = await axiosInstance.get("/trips/ongoing/");

        if (response) {
          console.log(response.data);

          this.futureTrips = response.data.data;
        }
      } catch (error) {
        console.error("미래 여행 조회 실패", error);
      }
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "tripStore",
        storage: sessionStorage,
      },
    ],
  },
});
