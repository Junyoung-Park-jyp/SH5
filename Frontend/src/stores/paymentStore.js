import { defineStore } from 'pinia';
import axiosInstance from '@/axios';

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
      {
        name: "에어프랑스",
        cost: 1806200,
        members: ["최한진", "박준영"],
        pay_date: "2024-05-10",
        pay_time: "16:21:00",
        checked: false,
      },
      {
        name: "대한한공",
        cost: 2420000,
        members: ["임광영", "정태완"],
        pay_date: "2024-05-17",
        pay_time: "17:24:00",
        checked: false,
      },
      {
        name: "Hotel Le Relais Du Louvre",
        cost: 910000,
        members: ["최한진", "박준영", "임광영", "정태완"],
        pay_date: "2024-06-30",
        pay_time: "09:19:00",
        checked: false,
      },
      {
        name: "Hertz Rental Car",
        cost: 450000,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-07-15",
        pay_time: "22:24:00",
        checked: false,
      },

      // 8월 10일
      {
        name: "아침 커피",
        cost: 4500,
        members: ["최한진", "박준영"],
        pay_date: "2024-08-10",
        pay_time: "08:15:00",
        checked: false,
      },
      {
        name: "점심 도시락",
        cost: 12000,
        members: ["임광영", "정태완"],
        pay_date: "2024-08-10",
        pay_time: "12:30:00",
        checked: false,
      },
      // 8월 11일
      {
        name: "아침 산책 후 주스",
        cost: 6000,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-08-11",
        pay_time: "09:00:00",
        checked: false,
      },
      {
        name: "저녁 식사",
        cost: 25000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-11",
        pay_time: "19:00:00",
        checked: false,
      },
      // 8월 12일
      {
        name: "점심 파스타",
        cost: 18000,
        members: ["임광영", "정태완", "최한진"],
        pay_date: "2024-08-12",
        pay_time: "13:00:00",
        checked: false,
      },
      {
        name: "저녁 맥주",
        cost: 8000,
        members: ["박준영"],
        pay_date: "2024-08-12",
        pay_time: "20:30:00",
        checked: false,
      },
      // 8월 13일
      {
        name: "박물관 입장료",
        cost: 15000,
        members: ["최한진", "임광영"],
        pay_date: "2024-08-13",
        pay_time: "10:00:00",
        checked: false,
      },
      {
        name: "저녁 라면",
        cost: 7000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-13",
        pay_time: "19:30:00",
        checked: false,
      },
      // 8월 14일
      {
        name: "아침 샌드위치",
        cost: 5000,
        members: ["최한진", "임광영", "박준영"],
        pay_date: "2024-08-14",
        pay_time: "08:30:00",
        checked: false,
      },
      {
        name: "점심 피자",
        cost: 22000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-14",
        pay_time: "13:00:00",
        checked: false,
      },
      // 8월 15일
      {
        name: "아침 커피",
        cost: 4500,
        members: ["최한진", "임광영"],
        pay_date: "2024-08-15",
        pay_time: "08:15:00",
        checked: false,
      },
      {
        name: "저녁 스테이크",
        cost: 30000,
        members: ["정태완", "박준영", "최한진"],
        pay_date: "2024-08-15",
        pay_time: "20:00:00",
        checked: false,
      },
      // 8월 16일
      {
        name: "점심 샐러드",
        cost: 12000,
        members: ["임광영", "박준영"],
        pay_date: "2024-08-16",
        pay_time: "12:00:00",
        checked: false,
      },
      {
        name: "디저트 아이스크림",
        cost: 5000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-16",
        pay_time: "15:00:00",
        checked: false,
      },
      // 8월 17일
      {
        name: "조식 뷔페",
        cost: 25000,
        members: ["최한진", "임광영"],
        pay_date: "2024-08-17",
        pay_time: "08:00:00",
        checked: false,
      },
      {
        name: "저녁 바비큐",
        cost: 35000,
        members: ["정태완", "박준영", "최한진"],
        pay_date: "2024-08-17",
        pay_time: "19:00:00",
        checked: false,
      },
      // 8월 18일
      {
        name: "브런치 팬케이크",
        cost: 18000,
        members: ["임광영", "박준영"],
        pay_date: "2024-08-18",
        pay_time: "10:30:00",
        checked: false,
      },
      {
        name: "저녁 타코",
        cost: 22000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-18",
        pay_time: "20:00:00",
        checked: false,
      },
      // 8월 19일
      {
        name: "점심 김밥",
        cost: 8000,
        members: ["최한진", "박준영"],
        pay_date: "2024-08-19",
        pay_time: "13:00:00",
        checked: false,
      },
      {
        name: "디저트 케이크",
        cost: 9000,
        members: ["임광영", "정태완"],
        pay_date: "2024-08-19",
        pay_time: "16:00:00",
        checked: false,
      },
      // 8월 20일
      {
        name: "아침 오믈렛",
        cost: 12000,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-08-20",
        pay_time: "09:00:00",
        checked: false,
      },
      {
        name: "저녁 파스타",
        cost: 20000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-20",
        pay_time: "19:30:00",
        checked: false,
      },
      // 8월 21일
      {
        name: "점심 햄버거",
        cost: 15000,
        members: ["최한진", "임광영"],
        pay_date: "2024-08-21",
        pay_time: "12:30:00",
        checked: false,
      },
      {
        name: "저녁 초밥",
        cost: 28000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-21",
        pay_time: "19:00:00",
        checked: false,
      },
      // 8월 22일
      {
        name: "아침 베이글",
        cost: 5000,
        members: ["최한진", "박준영"],
        pay_date: "2024-08-22",
        pay_time: "08:00:00",
        checked: false,
      },
      {
        name: "저녁 스파게티",
        cost: 22000,
        members: ["임광영", "정태완"],
        pay_date: "2024-08-22",
        pay_time: "19:30:00",
        checked: false,
      },
      // 8월 23일
      {
        name: "점심 파스타",
        cost: 18000,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-08-23",
        pay_time: "12:30:00",
        checked: false,
      },
      {
        name: "저녁 피자",
        cost: 24000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-23",
        pay_time: "19:30:00",
        checked: false,
      },
      // 8월 24일
      {
        name: "조식 뷔페",
        cost: 20000,
        members: ["최한진", "임광영"],
        pay_date: "2024-08-24",
        pay_time: "08:00:00",
        checked: false,
      },
      {
        name: "저녁 해물탕",
        cost: 35000,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-24",
        pay_time: "20:00:00",
        checked: false,
      },
      // 8월 25일
      {
        name: "점심 Viana",
        cost: 86200,
        members: ["정태완", "박준영"],
        pay_date: "2024-08-25",
        pay_time: "17:21:00",
        checked: false,
      },
      {
        name: "Monoprix",
        cost: 56789,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-08-25",
        pay_time: "22:24:00",
        checked: false,
      },
      // 8월 26일
      {
        name: "사그라다 파밀리아 입장료",
        cost: 20000,
        members: ["임광영", "정태완"],
        pay_date: "2024-08-26",
        pay_time: "09:33:00",
        checked: false,
      },
      {
        name: "저녁 스테이크",
        cost: 40000,
        members: ["최한진", "박준영", "임광영"],
        pay_date: "2024-08-26",
        pay_time: "20:00:00",
        checked: false,
      },
      // 8월 27일
      {
        name: "선크림",
        cost: 15000,
        members: ["최한진", "박준영", "임광영", "정태완"],
        pay_date: "2024-08-27",
        pay_time: "09:19:00",
        checked: false,
      },
      {
        name: "저녁 바베큐",
        cost: 30000,
        members: ["최한진", "박준영"],
        pay_date: "2024-08-27",
        pay_time: "19:30:00",
        checked: false,
      },
    ],
  }),
  getters: {
    getPaymentsByDate: (state) => (date) => {
      return state.payments.filter((payment) => payment.pay_date === date);
    },
  },
});