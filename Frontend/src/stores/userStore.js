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
        const response = await axiosInstance.post('/accounts/signup/', {
          username: userData.username,
          email: userData.email,
        });
        console.log(response.data)

        // await this.signIn({
        //   email,
        // });

      } catch (error) {
        console.error('회원가입 실패:', error);
      }
    },

    async signIn(userData) {
      try {
        const response = await axiosInstance.post('/accounts/login/', {
          email: userData.email,

        });
        if (response.message) {
          this.email = userData.email;
          this.isLogin = true;
        }
        

      } catch (error) {
        console.error('로그인 실패:', error);
      }
    },

    async getUser(email) {
      try {
        const response = await axiosInstance.get('/users', {
          email: email
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