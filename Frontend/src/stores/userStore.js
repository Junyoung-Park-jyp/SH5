import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
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
    userIsLogin(state) {
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
          userId: userData.userId,
        });

        const { userId, username, institutionCode, userKey } = response.data;

        await this.signIn({
          userId,
        });

      } catch (error) {
        console.error('회원가입 실패:', error);
      }
    },

    async signIn(userData) {
      try {
        const response = await axiosInstance.post('/member/search', {
          userId: userData.userId,
        });

        const { userId, userName, institutionCode, userKey } = response.data;

        this.name = userName;
        this.userKey = userKey;
        this.isLogin = true;

      } catch (error) {
        console.error('로그인 실패:', error);
      }
    },

    async getUser(userName, email) {
      try {
        const response = await axiosInstance.get('/users', {
          userName: userName,
          userEmail: email
        })

        if (response.data) {
          return response.data
        } else {
          console.error('사용자가 존재하지 않습니다')
          return null
        }
      } catch(error) {
        console.error('사용자 검색 실패:', error)
        return null
      }
    },

    clearUser() {
      this.name = '';
      this.email = '';
      this.isLogin = false;
      this.userKey = '';
    },


  },
});