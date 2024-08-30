import { defineStore } from 'pinia';
import axiosInstance from '@/axios';
import { useTripStore } from '@/stores/tripStore'
import { useBalanceStore } from '@/stores/balanceStore'
import { useUserStore } from './userStore';
export const usePaymentStore = defineStore('paymentStore', {
  state: () => ({
    payments: [
    ],
    bills: [
    ],
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
      const userStore = useUserStore();
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
              members: [{member: payment.username, bank_account: userStore.accountNum}] // 기본값으로 username을 members에 할당
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

    async makeAdjustment(tripId, selectedPayments) {
      console.log('makeAdjustment 가 받은 데이터', selectedPayments)
      // 각 payment 객체를 적절한 형식으로 변환
      const adjustments = selectedPayments.map(payment => {
        const memberCount = payment.members.length;
        const dividedCost = payment.amount / memberCount;
        return {
          payment_id: payment.id,
          bills: payment.members.map(member => {
            return {
              cost: dividedCost, // or use any logic to distribute the amount among members
              bank_account: payment.bank_account, // 기본적으로 payment의 계좌를 사용
            };
          }),
        };
      });
    
      try {
        const response = await axiosInstance.post('/payments/adjustment/', { 
          trip_id: tripId,
          payments: adjustments,
        });
    
        if (response) {
          this.payments = []; // 정산 후 payments 초기화
          console.log('정산에 성공했습니다');
        } else {
          console.error("요청이 거부되었습니다.");
        }
      } catch(error) {
        console.error('정산 실패', error);
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