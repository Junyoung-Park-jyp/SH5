import { defineStore } from 'pinia';
import { useUserStore } from '@/stores/userStore.js'
import axiosInstance from '@/axios';
import { useTripStore } from './tripStore';

export const useBalanceStore = defineStore('balance', {
  state: () => ({
    accounts: [],
    bank: null,
    balance: null,
    accountNum: null,
    withdrawal: null, // 출금
    deposit: null, // 입금
    payments: [], // 결제 내역
  }),
  getters: {
    userAccounts(state) {
      return state.accounts
    },
    userBalance(state) {
      return state.balance
    },
    userWithdrawal(state) {
      return state.withdrawal
    },
    userDeposit(state) {
      return state.deposit
    }
  },

  actions: {
    // 사용자가 계좌 변경시, 계좌 초기화
    clearAccount() {
      this.bank = null
      this.balance = null
      this.accountNum = null
    },

    // 계좌 리스트 조회 데이터 처리
    // 계좌 잔액 갱신
    async refreshBalance(accountNum) {
      try {
        const response = await axiosInstance.post('/edu/demandDeposit/inquireDemandDepositAccountBalance')
        if (response.data.REC) {
          this.balance = response.REC.accountBalance
        } else {
          console.error('계좌가 없습니다')
        }
        
      } catch(error) { console.error('계좌 잔액 조회 실패:', error)}

    },

    // 계좌 리스트 조회
    async getAccounts(userEmail) {
      try {
      
        const response = await axiosInstance.get('/bank_accounts/', { email: userEmail });

        if (response.data) {
          this.accounts = response.data.data
          console.log("계좌 정보", this.accounts)
        } else {
          console.error('올바르지 않은 응답 구조:', response.data);
        }
      } catch (error) {
        console.error('계좌 리스트 조회 실패:', error);
      }
    },

    // 계좌 출금
    async withdrawAccount(accountData) {
      try {
        const response = await axiosInstance.post('edu/demandDeposit/inquireDemandDepositAccountWithdrawal',
          {
            accountNo: this.accountNum,
            transactionBalance: accountData.transactionBalance,
            transactionSummary: "(수시입출금): 출금"
          }
        );

        if (response.data && response.data.REC) {
          this.refreshBalance(this.accountNum)
        } else {
          console.error('올바르지 않은 응답 구조:', response.data);
        }
      } catch (error) {
        console.error('계좌 리스트 조회 실패:', error);
      }
    },

    // 계좌 입금
    async depositAccount(accountData) {
      try { 
        const response = await axiosInstance.post('/edu/demandDeposit/updateDemandDepositAccountDeposit',
          {
            accountNo: this.accountNum,
            transactionBalance: accountData.transactionBalance,
            transactionSummary: "(수시입출금): 입금"
          }
        );

        if (response.data && response.data.REC) {
          this.refreshBalance(this.accountNum)
        } else {
          console.error('올바르지 않은 응답 구조:', response.data);
        }
      } catch (error) {
        console.error('계좌 리스트 조회 실패:', error);
      }
    },

  },
});