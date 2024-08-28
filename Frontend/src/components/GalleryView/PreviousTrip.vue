<template>
  <div class="main-container">
    <!-- 국가 -->
    <div class="my-10 trip country">
      {{ destination }}
    </div>

    <!-- 날짜 -->
    <div class="trip date">
      <div class="title d-flex justify-space-between">
        날짜<v-spacer></v-spacer>
        <div class="subtitle">{{ duration }}</div>
      </div>
      <div class="content">
        <p>시작일 &nbsp; | &nbsp; {{ formatDay(startDate) }}</p>
        <p>종료일 &nbsp; | &nbsp; {{ formatDay(endDate) }}</p>
      </div>
    </div>

    <!-- 멤버 -->
    <div class="trip member">
      <div class="title">
        멤버<v-spacer></v-spacer>
        <div class="subtitle">{{ tripMembers.length }}명</div>
      </div>
      <div class="background-member content">
        <div
          v-for="(member, index) in tripMembers"
          :key="index"
          class="member-list"
          :style="{ backgroundImage: `url(${getImagePath(index)})`, paddingRight: calculatePadding(index) }"
        >
          <div
            class="member-symbol d-flex justify-center align-center"
            :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }"
          >
            <div class="member-familyname">{{ member.name.slice(0, 3) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 지출 내역 -->
    <div class="trip money">
      <div class="title">나의 지출</div>
      <div class="content">
        <PieChart />
      </div>
    </div>

    <!-- 여행 스케치 -->
    <div class="trip sketch">
      <div class="title">여행 스케치</div>
      <div class="content">
        <DrawPicture />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useTripStore } from "@/stores/tripStore";
import { useRoute } from "vue-router";
import { format } from "date-fns";
import { useMemberColors } from "@/stores/colorStore";
import {
  exchangeArray,
  formatToTwoDecimal,
  formatWithComma,
  convertCurrency,
  currencyIcons,
  currencyText,
  fetchExchangeRates,
} from "@/stores/currencyStore";

import DrawPicture from "./DrawPicture.vue";
import PieChart from './PieChart.vue';

// const route = useRoute()
// const tripStore = useTripStore()
// const tripId = route.params.tripId
// const tripData = computed(() => {
//   return tripStore.getTrip(tripId)
// })

// 여행 목적지
const country = "대한민국";
const city = "부산";

// 대한민국 여행일 경우 목적지는 도시로 설정
const destination = ref(country);
if (country === "대한민국") {
  destination.value = city;
}

// 오늘 날짜
const today = new Date();
today.setHours(0, 0, 0, 0);

// 여행 날짜
const startDate = new Date(2024, 7, 10); // 2024년 8월 10일
const endDate = new Date(2024, 7, 27); // 2024년 8월 27일

// 몇 박 몇 일 계산
const durationInDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
const nights = durationInDays - 1;
const days = durationInDays;

// 몇 박 몇 일 포맷팅
const formatDuration = (nights, days) => {
  return `${nights}박 ${days}일`;
};

const duration = formatDuration(nights, days);

const formatDay = (date) => {
  return format(date, "yyyy년 MM월 dd일");
};

// 여행 멤버와 계좌번호
const tripMembers = [
  { name: "박준영", account: "신한 0276524561730773" },
  { name: "이선재", account: "신한 000-000-000" },
  { name: "임광영", account: "국민 000-000-000" },
  { name: "정태완", account: "우리 000-000-000" },
  { name: "최한진", account: "계좌 미등록" },
  { name: "이뭉크", account: "신한 000-000-000" },
];

const { memberColors, rgbaColor } = useMemberColors(tripMembers);

import member1 from '@/assets/img/member1.png';
import member2 from '@/assets/img/member2.png';
import member3 from '@/assets/img/member3.png';
import member4 from '@/assets/img/member4.png';

const images = [member1, member2, member3, member4];

const getImagePath = (index) => {
  return images[index % images.length];
};

const calculatePadding = (index) => {
  // Example padding values based on index, customize as needed
  const paddingValues = [0, 15, 40, 40]; // These values are in pixels
  return `${paddingValues[index % paddingValues.length]}px`;
};
</script>

<style scoped>
.main-container {
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 20px;
  background-color: #f4f6fa;
}

/* 구획 나누기 */
.trip {
  margin: 20px auto;
  /* border: 2px solid blue; */
}

.title {
  font-size: x-large;
  font-weight: bolder;
  padding: 5px 20px;
}

.subtitle {
  font-size: medium;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.content {
  background-color: #ffffff;
  padding: 10px 20px;
}

.content * {
  font-size: 1rem;
}

/* 국가 */
.country {
  display: flex;
  justify-content: center; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 100px;
  font-size: 40px;
  font-weight: bolder;
}

/* 날짜 */
.date {
  margin-top: -10px;
}

.date > .content {
  padding-left: 35px;
}

.dday {
  font-size: large;
  margin: auto;
}

/* 멤버 */
.member * {
  margin: 0px auto;
}

.member > .title {
  display: flex;
}

.background-member {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 200px;
  max-width: 400px; /* 한 화면에 4명씩 (4 * 100px) */
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.member-list {
  display: flex;
  align-items: center;
  justify-content: flex;
  width: 100px; /* 각 사진의 너비 */
  height: 100%; 
  background-size: cover;
  background-position: center;
  scroll-snap-align: start; /* Snap alignment */
  flex-shrink: 0; /* Prevent shrinking */
  /* border: 1px solid black; */
  padding-bottom: 55px;
  padding-left: 10px;
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.member-familyname {
  font-weight: 500;
}

/* 지출내역 */
.money {
  width: 100%;
  padding: 10px 0;
  margin: 0 auto;
  padding: 20px 0 50px 0;
}

/* 스케치 */
.sketch {
  width: 100%;
  overflow-x: hidden;
  margin: 0 auto;
}

.sketch .content {
  padding: 30px 20px;
}
</style>
