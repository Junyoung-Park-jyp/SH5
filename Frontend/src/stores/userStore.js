import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

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
    async signUp(userData) {
      try {
        // 회원가입 API 호출
        const response = await axiosInstance.post('/member', {
          apiKey: this.apiKey,
          userId: userData.userId,
          password: userData.password
        });

        const { userId, username, institutionCode, userKey } = response.data;

        await this.signIn({
          userId,
          apiKey: this.apiKey,
          password: userData.password,
        });

      } catch (error) {
        console.error('회원가입 실패:', error);
      }
    },

    async signIn(userData) {
      try {
        const response = await axiosInstance.post('/member/search', {
          userId: userData.userId,
          apiKey: this.apiKey,
          password: userData.password, 
        });

        const { userId, userName, institutionCode, userKey } = response.data;

        this.name = userName;
        this.userKey = userKey;
        this.isLogin = true;

      } catch (error) {
        console.error('로그인 실패:', error);
      }
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