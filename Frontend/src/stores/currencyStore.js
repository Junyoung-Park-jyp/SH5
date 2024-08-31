import { ref, onMounted } from "vue";
import axios from "axios";
import axiosInstance from "@/axios";
import { useUserStore } from "./userStore";

// 환율 데이터를 저장하는 상태
export const exchangeArray = ref([]);

// 통화 아이콘 맵핑
export const currencyIcons = {
  CAD: "mdi-currency-usd",
  CHF: "mdi-currency-fra",
  CNY: "mdi-currency-cny",
  EUR: "mdi-currency-eur",
  GBP: "mdi-currency-gbp",
  JPY: "mdi-currency-jpy",
  USD: "mdi-currency-usd",
};

// 통화 기호 맵핑
export const currencyText = {
  CAD: "$",
  CHF: "₣",
  CNY: "¥",
  EUR: "€",
  GBP: "£",
  JPY: "¥",
  USD: "$",
};

// 환율 데이터를 가져오는 함수
export function fetchExchangeRates() {
  const userStore = useUserStore()
  axios({
    url: 'https://5illjjang.click/api/exchange_rates/',
    headers: {Authorization: `Token ${userStore.token}`}
  })
    .then(res => {
      exchangeArray.value = res.data.data
      exchangeArray.value = res.data.data.filter(element => element.currency === 'EUR' || element.currency === 'JPY' || element.currency === 'USD');
      console.log(exchangeArray.value)
    })
    .catch(err => console.log(err))
}

// Dummy exchange rates (환율 데이터를 저장)
// 환율 데이터를 가져오는 함수
// export function fetchExchangeRates() {
  // 임의의 dummy 데이터를 사용하도록 설정
  // exchangeArray.value = [
    // {
    //   id: 5399,
    //   currency: "CAD",
    //   exchangeRate: "980.82",
    //   exchangeMin: "140",
    //   created: "2024-08-22 16:31:47",
    // },
    // {
    //   id: 5400,
    //   currency: "CHF",
    //   exchangeRate: "1,566.15",
    //   exchangeMin: "100",
    //   created: "2024-08-22 16:31:47",
    // },
    // {
    //   id: 5401,
    //   currency: "CNY",
    //   exchangeRate: "186.91",
    //   exchangeMin: "800",
    //   created: "2024-08-22 16:31:47",
    // },
    // {
    //   id: 5402,
    //   currency: "EUR",
    //   exchangeRate: "1,486.49",
    //   exchangeMin: "100",
    //   created: "2024-08-22 16:31:47",
    // },
    // {
    //   id: 5403,
    //   currency: "GBP",
    //   exchangeRate: "1,744.64",
    //   exchangeMin: "80",
    //   created: "2024-08-22 16:31:47",
    // },
//     {
//       id: 5404,
//       currency: "JPY",
//       exchangeRate: "919.63",
//       exchangeMin: "100",
//       created: "2024-08-22 16:31:47",
//     },
//     {
//       id: 5406,
//       currency: "USD",
//       exchangeRate: "1,332.4",
//       exchangeMin: "100",
//       created: "2024-08-22 16:31:47",
//     },
//   ];
// }

// 금액을 소수점 둘째 자리까지 포맷하는 함수
export function formatToTwoDecimal(value) {
  if (typeof value !== "number") {
    value = parseFloat(value);
  }
  return value.toFixed(2);
}

// 세 자리마다 콤마를 찍어주는 함수
export function formatWithComma(value) {
  if (typeof value !== "number") {
    value = parseFloat(value);
  }
  return value.toLocaleString("en-US");
}

// 외화와 원화 간의 환율을 적용해 변환하는 함수
export function convertCurrency(value, rate, toForeignCurrency) {
  if (toForeignCurrency) {
    return value / rate; // 외화 -> 원화
  } else {
    return value * rate; // 원화 -> 외화
  }
}
