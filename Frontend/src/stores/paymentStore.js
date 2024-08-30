import { defineStore } from 'pinia';
import axiosInstance from '@/axios';
import { useTripStore } from '@/stores/tripStore'
import { useBalanceStore } from '@/stores/balanceStore'
import { useUserStore } from './userStore';
export const usePaymentStore = defineStore('paymentStore', {
  state: () => ({
    payments: [
    ],
    budgets: [
    ],
    adjustmentResult:null
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

    async deletePayment(paymentId) {
      try {
        const response = await axiosInstance.post('/payments/delete/', {
          payment_id: paymentId
        })
        if (response) {
          console.log(response.data)
        } else {
          console.error('결제 내역 삭제 오류')
        }
      } catch(error) {
        console.error("결제 내역 삭제 실패", error)
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
          this.budgets = response.data.budget
          // response.data.data 배열을 순회하며 각 payment에 members 필드를 추가
          this.payments = response.data.data.map(payment => {
            const paymentMembers = tripStore.members.map(member => ({
              member: member.member,  // member 객체에서 필요한 필드를 사용
              bank_account: member.bank_account // 기본적으로 동일한 계좌 사용
            }));
          
            return {
              ...payment,
              members: paymentMembers // tripStore.members를 기반으로 새로 생성한 members 배열을 할당
            };
          });
    
          console.log("멤버가 추가된 정산 내역" , this.payments);
        } else {
          console.error('정산 내역 조회 실패');
        }
      } catch (error) {
        console.error('결제내역 조회 실패', error);
      }
    },

    async makeAdjustment(tripId, adjustments) {
      console.log('makeAdjustment 가 받은 데이터', adjustments)
      // 각 payment 객체를 적절한 형식으로 변환      
      try {
        const response = await axiosInstance.post('/payments/adjustment/', { 
          trip_id: tripId,
          payments: adjustments,
        });
    
        if (response) {
          this.adjustmentResult = response.data
          // 정산 성공 시, selectedPayments의 id와 this.payments의 id를 비교하여 is_completed를 1로 설정
          this.payments = this.payments.map(payment => {
            const isCompleted = selectedPayments.some(selected => selected.id === payment.id);
            if (isCompleted) {
              return {
                ...payment,
                is_completed: 1, // is_completed 값을 1로 변경
              };
            }
            return payment;
          });
          
          
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