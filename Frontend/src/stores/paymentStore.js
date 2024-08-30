import { defineStore } from 'pinia';
import axiosInstance from '@/axios';
import { useTripStore } from '@/stores/tripStore'
export const usePaymentStore = defineStore('paymentStore', {
  // state: () => ({
  //   payments: [],
  //   cost: null,
  //   category: null,
    
  // }),

  // getters: {
  //   tripPayments(state) {
  //     return state.payments
  //   }
  // },

  // actions: {
  // },

  state: () => ({
    payments: [
    ],
  }),
  getters: {
    getAllPayments(state) {
      return state.payments; // 모든 결제 내역을 반환
    },
    getPaymentsByDate: (state) => (date) => {
      return state.payments.filter(payment => payment.pay_date === date);
    }
  },

  actions: {
    
    // 결제
    async makePayment(paymentData) {
      try {
        const response = await axiosInstance.post('/payments/', { paymentData })

        if (response.data) {
          this.payments.push(response.data)
        } else {
          console.error('데이터가 잘못 전송되었습니다.')
        }

      } catch(error) {
        console.error("결제 실패: ", error)
      }
    },

    async getPayments(tripId) {
      try {
        const response = await axiosInstance.get('/payments/list/', { params: {
          trip_id: tripId,
          } 
        })

        if (response) {
          console.log("정산 내역", response.data)
          this.payments=response.data.data
        } else {
          console.error('정산 내역 조회 실패')
        }

      } catch(error) {
        console.error('결제내역 조회 실패', error)
      }
    },

    async makeAdjustment() {
      const tripStore = useTripStore()
      try {
        const response = await axiosInstance.post('/payments/adjustment/', { 
          trip_id: tripStore.tripId,
          payment_id: this.paymentId,
          bills: this.payments
        }
      )
      if (response) {
        this.payments = []
        console.log('정산에 성공했습니다')
      } else {
        "요청이 거부되었습니다."
      }
      } catch(error) {
        console.error('정산 실패', error)
      }
    },

  }
});