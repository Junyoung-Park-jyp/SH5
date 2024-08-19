import { defineStore } from 'pinia';

export const useBalanceStore = defineStore('balance', {
  state: () => ({
    accounts: [],
    bank: null,
    balance: null,
    accountNum: null,
    sendPayment: null,
    getPayment: null,
  }),

  getters: {
    
  },

  actions: {
    setAccounts(accountsData) {
      this.accounts = accountsData
      .filter(account => account.accountTypeCode === "1")
      .map(account => ({
        bankName: account.bankName,
        userName: account.userName,
        accountNo: account.accountNo,
        accountBalance: account.accountBalance
      }));
    },
  },
});