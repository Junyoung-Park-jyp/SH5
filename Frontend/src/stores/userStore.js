import { defineStore } from 'pinia';
import axiosInstance from '@/axios';
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    name: '',
    email: '',
    userKey: '',
    bank: null,
    accountNum: null,
    balance: 0,
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
    },
    userAccountNumMasked(state) {
      if (!state.accountNum) return '';
      if (state.accountNum.length <= 5) return '*'.repeat(state.accountNum.length);
      const visiblePart = state.accountNum.slice(0, -5);
      const maskedPart = '*'.repeat(5);
      return visiblePart + maskedPart;
    },
    userBalance(state) {
      return state.balance
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
        if (response) {
          this.email = userData.email;
          this.isLogin = true;
          this.name = response.data.data.username
          this.token = response.data.token

          // 신한 은행의 계좌 정보
          const searchResponse = response.data.data.account_list.filter(element => element.bank_name === '신한은행')[0]

          this.bank = searchResponse.bank_name
          this.accountNum = searchResponse.bank_account
          this.balance = Number(searchResponse.balance)
          console.log('data', response.data)
          console.log("로그인 여부", this.isLogin, this.name)
        }
        

      } catch (error) {
        console.error('로그인 실패:', error);
      }
    },

    async getUser(email) {
      try {
        if (email == this.email) {
          alert('자기 자신을 초대할 수 없습니다.')
        }
        else if (this.isLogin) {
          const response = await axiosInstance.get('/trips/member/', { params: { email: email } })
          console.log(response.data)
          if (response.data) {
            return response.data;
          } else {
            console.error('사용자가 존재하지 않습니다');
            return null
          }
        }

        
      } catch(error) {
        console.error('사용자 검색 실패:', error);
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
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'userStore',
        storage: localStorage,
      },
    ],
  },  
});