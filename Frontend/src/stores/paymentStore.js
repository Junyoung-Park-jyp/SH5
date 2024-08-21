import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    payments: [],
    cost: null,
    category: null,
    
  }),

  getters: {
    tripPayments(state) {
      return state.payments
    }
  },

  actions: {
  },
});