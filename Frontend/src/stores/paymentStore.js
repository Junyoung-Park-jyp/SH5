import { defineStore } from 'pinia';
import axiosInstance from '@/axios';
import { useTripStore } from '@/stores/tripStore'
export const usePaymentStore = defineStore('paymentStore', {
  state: () => ({
    payments: [
    ],
    bills: [
    ]
  }),
  getters: {
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
      const tripStore = useTripStore();

      try {
        const response = await axiosInstance.get('/payments/list/', {
          params: {
            trip_id: tripId,
          }
        });
    
        if (response) {
          console.log("정산 내역", response.data);
          console.log("여행 멤버", tripStore.members)
          // response.data.data 배열을 순회하며 각 payment에 members 필드를 추가
          this.payments = response.data.data.map(payment => {
            return {
              ...payment,
              members: [{member: payment.username}] // 기본값으로 username을 members에 할당
            };
          });
    
          console.log(this.payments);
        } else {
          console.error('정산 내역 조회 실패');
        }
      } catch (error) {
        console.error('결제내역 조회 실패', error);
      }
    },

    async makeAdjustment() {
      const tripStore = useTripStore()
      try {
        const response = await axiosInstance.post('/payments/adjustment/', { 
          trip_id: tripStore.tripId,
          payment_id: this.paymentId,
          bills: this.bills
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
    // 특정 날짜 이후의 결제 내역 필터링
    filterPaymentsAfterDate(startDate) {
      return this.payments.filter(payment => new Date(payment.pay_date) >= new Date(startDate));
    },

    // 특정 날짜 이전의 결제 내역 필터링 (예: 사전 예약)
    filterPaymentsBeforeDate(startDate) {
      return this.payments.filter(payment => new Date(payment.pay_date) < new Date(startDate));
    },

    // 특정 날짜의 결제 내역 필터링
    filterPaymentsByDate(selectedDate) {
      return this.payments.filter(payment =>
        new Date(payment.pay_date).toDateString() === new Date(selectedDate).toDateString()
      );
    },

    // 모든 결제 내역 반환
    getAllPayments() {
      return this.payments;
    },

    // 결제 항목 체크 상태 토글
    togglePaymentCheck(paymentIndex, type, startDate) {
      const paymentList =
        type === 'booking'
          ? this.filterPaymentsBeforeDate(startDate)
          : this.filterPaymentsAfterDate(startDate);

      paymentList[paymentIndex].checked = !paymentList[paymentIndex].checked;
    },

    // 정산 대상 토글
    toggleMemberInPayment(paymentIndex, memberName, type, startDate) {
      const paymentList =
        type === 'booking'
          ? this.filterPaymentsBeforeDate(startDate)
          : this.filterPaymentsAfterDate(startDate);

      const payment = paymentList[paymentIndex];

      if (payment.members.includes(memberName)) {
        payment.members = payment.members.filter(name => name !== memberName);
      } else {
        payment.members.push(memberName);
      }
    },

    addBills(payment, members) {
      
    }
  },
});