import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useErrorStore = defineStore('error', {
  state: () => ({
    isError: false,
    errorMessage: '',
  }),
  getters: {
    hasError: (state) => !!state.errorMessage,
  },
  actions: {
    // 에러 메시지 설정 및 다이얼로그 표시
    showError(message) {
      this.errorMessage = message;
      this.isError = true;
    },
    // 에러 상태 초기화 및 다이얼로그 숨김
    clearError() {
      this.isError = false;
      this.errorMessage = '';
    },
  },
});
