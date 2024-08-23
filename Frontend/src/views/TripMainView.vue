<template>
  <div>
    <h1>최한진 님은 {{ destination }} 여행 {{ tripState }} 중</h1>

    <!-- 날짜 -->
    <div>
      <div class="d-flex justify-space-between">
        <h2>날짜</h2>
        <div @click="modifyTrip">수정</div>
        <div v-if="tripState === '준비'">D-{{ Math.ceil((startDate - today) / (1000 * 60 * 60 * 24)) }}</div>
      </div>
      <div>
        <p>시작일 | {{ formatDay(startDate) }}</p>
        <p>종료일 | {{ formatDay(endDate) }}</p>
      </div>
    </div>

    <!-- 멤버 -->
    <div>
      <h2>멤버</h2>
      <div v-for="member in tripMembers" class="d-flex align-center">
        <div class="name-symbol d-flex justify-center align-center">
          <div>{{ member[0].slice(0, 1) }}</div>
        </div>
        <div>{{ member[0] }}</div>
        <div>{{ member[1] }}</div>
      </div>
    </div>

    <v-btn @click="goDetail">지출내역</v-btn>

    <!-- 환율 -->
    <div>
      <h2>환율 계산기</h2>
      <div class="d-flex">
        <v-select v-model="selectCurrency" :items=currencies></v-select>
        <v-text-field v-model="foreignCurrency"></v-text-field>
        <v-icon :icon="currencyIcons[selectCurrency]"></v-icon>
        <v-icon icon="mdi-arrow-left-right"></v-icon>
        <v-text-field v-model="koreaCurrency"></v-text-field>
        <v-icon icon="mdi-currency-krw"></v-icon>
      </div>
      <div>현재 환율은 {{ foreignCurrency }}{{ currencyText[selectCurrency] }} = {{ koreaCurrency }}₩ 입니다.</div>
    </div>

    <!-- 여행자 보험 -->
    <div>
      <h2>여행자 보험</h2>
      <div>
        친구와 함께 가족과 함께<br>
        2인 가입 시 5% 할인<br>
        3인 이상 가입 시 총 10% 할인
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { format } from 'date-fns';
import axios from 'axios'

const router = useRouter()

// 여행 목적지
const country = '대한민국'
const city = '부산'

// 대한민국 여행일 경우 목적지는 도시로 설정
const destination = ref(country)
if (country === '대한민국') {
  destination.value = city
}

// 오늘 날짜
const today = new Date();

// 여행 날짜
const startDate = new Date(2024, 7, 26);  // 2024년 8월 10일
const endDate = new Date(2024, 7, 27);  // 2024년 8월 27일

// 여행 상태
const tripState = ref('준비')
if (startDate <= today && today <= endDate) {
  tripState.value = ''
}

const formatDay = (date) => {
  return format(date, 'yyyy년 MM월 dd일')
}

// 여행 멤버와 계좌번호
const tripMembers = [
  ['박준영', '000-000-000'],
  ['임광영', '000-000-000'],
  ['정태완', '000-000-000'],
  ['최한진', '000-000-000'],
]

// 선택한 통화
const selectCurrency = ref('USD')

// 지원하는 통화 배열
const currencies = ['USD', 'EUR', 'JPY', 'CNY', 'GBP', 'CHF', 'CAD']

// 환율 GET 요청
const exchangeArray = ref([])
// onMounted(() => {
//   axios({
//     url: 'http://52.79.246.151:8000/exchange_rate/',
//     method: 'get'
//   })
//     .then(res => {
//       exchangeArray.value = res.data
//       console.log(res)
//     })
//     .catch(err => console.log(err))
// })
exchangeArray.value = [
  {
    "id": 5399,
    "currency": "CAD",
    "exchangeRate": "980.82",
    "exchangeMin": "140",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5400,
    "currency": "CHF",
    "exchangeRate": "1,566.15",
    "exchangeMin": "100",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5401,
    "currency": "CNY",
    "exchangeRate": "186.91",
    "exchangeMin": "800",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5402,
    "currency": "EUR",
    "exchangeRate": "1,486.49",
    "exchangeMin": "100",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5403,
    "currency": "GBP",
    "exchangeRate": "1,744.64",
    "exchangeMin": "80",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5404,
    "currency": "JPY",
    "exchangeRate": "919.63",
    "exchangeMin": "100",
    "created": "2024-08-22 16:31:47"
  },
  {
    "id": 5406,
    "currency": "USD",
    "exchangeRate": "1,332.4",
    "exchangeMin": "100",
    "created": "2024-08-22 16:31:47"
  }
]

// 환율 계산
const foreignCurrency = ref(1)
const koreaCurrency = computed(() => {
  const selectedExchange = exchangeArray.value.find(
    item => item.currency === selectCurrency.value
  )
  return parseFloat(selectedExchange.exchangeRate.replace(/,/g, '')) * foreignCurrency.value
})

// 통화에 따른 버튼 아이콘
const currencyIcons = {
  'CAD': 'mdi-currency-usd',
  'CHF': 'mdi-currency-fra',
  'CNY': 'mdi-currency-cny',
  'EUR': 'mdi-currency-eur',
  'GBP': 'mdi-currency-gbp',
  'JPY': 'mdi-currency-jpy',
  'USD': 'mdi-currency-usd',
}

// 통화에 따른 텍스트
const currencyText = {
  'CAD': '$',
  'CHF': '₣',
  'CNY': '¥',
  'EUR': '€',
  'GBP': '£',
  'JPY': '¥',
  'USD': '$',
}

const modifyTrip = () => {
  return router.push({ name: 'createTrip' })
}

const goDetail = () => {
  return router.push({ name: 'tripDetail' })
}
</script>

<style scoped>
.name-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 30px;
  height: 30px;
}
</style>