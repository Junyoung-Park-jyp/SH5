import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
    apiKey: '',
    userKey: '',
    bank: null,
    accountNum: null,
    isLogin: false,
  }),

  getters: {
    userName(state) {
      return state.name;
    },
    userEmail(state) {
      return state.email;
    },
    apiKey(state) {
      return state.apiKey
    },
    isLogin(state) {
      return state.isLogin;
    },
    userBank(state) {
      return state.bank
    },
    userAccountNum(state) {
      return state.accountNum
    }
  },

  actions: {
    setUser(userData) {
      this.name = userData.userName;     
      this.email = userData.email;
      this.isLogin = true;
      this.apiKey = userData.apiKey;
      this.userKey = userData.userKey;
    },


    clearUser() {
      this.name = '';
      this.email = '';
      this.isLogin = false;
      this.apiKey = '';
      this.userKey = '';
    },
  },
});