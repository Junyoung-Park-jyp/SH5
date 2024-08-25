<template>
  <div class="main-container">
    <!-- 프로필 -->
    <div class="my-10 profile">
      <img class="profile-img" src="../assets/img/profile.png" alt="프로필" />
      <span
        >최한진 님은
        <span class="profile-destination">{{ destination }}</span> 여행
        {{ tripState }} 중</span
      >
    </div>

    <div class="pick-container">
      <!-- ALL -->
      <div class="all">
        <div class="upper">&nbsp;</div>
        <div class="middle">A</div>
        <div class="bottom">ALL</div>
      </div>
      <!-- 준비 -->
      <div class="prepare">
        <div class="upper">&nbsp;</div>
        <div class="middle">P</div>
        <div class="bottom">준비</div>
      </div>

      <!-- 구분선 -->
      <div class="line">|</div>

      <!-- 날짜 스크롤 -->
      <!-- <div v-for="(date, index) in weeks" :key="index"> -->
      <div class="day-scroll">
        <div v-for="(day, i) in date" :key="i" class="day-container">
          <div class="upper">{{ format(day, "EEE") }}</div>
          <div class="middle" :class="{ 'today-circle': isToday(day) }">
            {{ format(day, "d") }}
          </div>
          <div class="bottom">{{ format(day, "M") }}월</div>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="arrow">></div>

      <!-- 날짜 캐러셀 by 광영 -->
      <!-- <v-row>
        <v-col class="carousel-container" cols="9">

          <v-btn
            variant="text"
            icon="mdi-chevron-left"
            @click="prevWeek"
            :disabled="currentWeekIndex === 0"
          ></v-btn>

          <div class="carousel">
            <div class="carousel-track" :style="trackStyle">
              <div
                v-for="(date, index) in weeks"
                :key="index"
                class="carousel-item"
              >
                <div v-for="(day, i) in date" :key="i" class="day-container">
                  <div class="upper">{{ format(day, "EEE") }}</div>
                  <div :class="{ 'today-circle': isToday(day) }" class="middle">
                    {{ format(day, "dd") }}
                  </div>
                  <div class="bottom">{{ format(day, "M") }}월</div>
                </div>
              </div>
            </div>
          </div>

          <v-btn
            variant="text"
            icon="mdi-chevron-right"
            @click="nextWeek"
            :disabled="currentWeekIndex === weeks.length - 1"
          ></v-btn>
        </v-col> -->
      <!-- </v-row> -->
    </div>

    <DetailReady v-if="tripState === '준비'" />
    <DetailProgress v-else />

    <v-btn @click="goFinish">정산하기</v-btn>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { eachDayOfInterval, format } from "date-fns";

import DetailReady from "@/components/TripDetailView/DetailReady.vue";
import DetailProgress from "@/components/TripDetailView/DetailProgress.vue";

const router = useRouter();

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

// 오늘 날짜인지를 판별
const isToday = (day) => {
  if (
    day.getFullYear() === today.getFullYear() &&
    day.getMonth() === today.getMonth() &&
    day.getDate() === today.getDate()
  ) {
    return true;
  } else {
    return false;
  }
};

// 여행 날짜
const startDate = new Date(2024, 7, 10); // 2024년 8월 10일
const endDate = new Date(2024, 8, 23); // 2024년 8월 27일

// 여행 날짜의 범위
const date = eachDayOfInterval({
  start: startDate,
  end: endDate,
});

// 오늘 날짜의 인덱스 찾기
const todayIndex = date.findIndex((day) => isToday(day));

// 컴포넌트가 마운트된 후 스크롤을 이동
onMounted(() => {
  const dayScrollContainer = document.querySelector(".day-scroll");
  const todayElement = dayScrollContainer.children[todayIndex];

  // 오늘 날짜를 왼쪽에 맞추기
  if (todayElement) {
    dayScrollContainer.scrollLeft = todayElement.offsetLeft;
  }

  // 스크롤 가능 여부에 따라 화살표 표시
  const arrowElement = document.querySelector(".arrow");
  if (dayScrollContainer.scrollWidth > dayScrollContainer.clientWidth) {
    arrowElement.style.display = "block";
  } else {
    arrowElement.style.display = "none";
  }
});

// const tripRange = eachDayOfInterval({
//   start: startDate,
//   end: endDate,
// });

// 여행 상태
const tripState = ref("준비");

// 현재 날짜의 주차 인덱스
const currentWeekIndex = ref(0);

// 여행 날짜의 범위를 6일 단위로 구분
// const weeks = [];
// for (let i = 0; i < tripRange.length; i += 5) {
//   const tmp = tripRange.slice(i, i + 5);
//   weeks.push(tmp);
//   if (tmp[0] <= today && today <= tmp[tmp.length - 1]) {
//     currentWeekIndex.value = i / 5;
//     tripState.value = "";
//   }
// }

const prevWeek = () => {
  if (currentWeekIndex.value > 0) {
    currentWeekIndex.value--;
  }
};

const nextWeek = () => {
  if (currentWeekIndex.value < weeks.length - 1) {
    currentWeekIndex.value++;
  }
};

const trackStyle = computed(() => ({
  transform: `translateX(-${currentWeekIndex.value * 100}%)`,
}));

const goFinish = () => {
  return router.push({ name: "tripFinish" });
};
</script>

<style scoped>
.main-container {
  height: 92vh;
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 20px;
  background-color: #f4f6fa;
}

/* 프로필 */
.profile {
  display: flex;
  justify-content: left; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 100px;
}

.profile-img {
  height: 75px;
  margin-left: 30px;
  margin-right: 20px;
}

.profile > span {
  font-weight: bold;
  font-size: 1.25rem;
}

.profile-destination {
  font-weight: bolder;
  font-size: x-large;
  padding: 0 4px;
  text-decoration-line: underline;
  text-decoration-style: wavy;
  text-decoration-thickness: 2px;
  text-underline-offset: 4px; /* 글자-밑줄 간격 */
  text-decoration-skip-ink: none;
}

/* 구획 나누기 */
.pick-container {
  width: 95%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  height: 100px;
  margin: -40px auto 20px auto;
}

.all,
.prepare {
  width: 30px;
  margin: 0px 5px;
  padding: 0;
  flex-shrink: 0;
}

.line {
  margin: auto 0px;
}

.day-scroll {
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: row;
  white-space: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px 10px;
}

.arrow {
  margin: 0px 5px;
  display: none;
}

.upper,
.middle,
.bottom {
  height: 30%;
  margin: 0 auto;
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.upper,
.bottom {
  font-size: xx-small;
  color: rgb(109, 109, 109);
}

.middle {
  font-weight: 600;
  margin: 5px 0px;
}

/* 날짜 */
.day-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  padding: 0 10px;
  width: 100%;
}

/* 날짜 */
.day-scroll::-webkit-scrollbar {
  display: none; /* 웹킷 브라우저에서 스크롤바 숨김 */
}

.today-circle {
  background-color: #4b72e1;
  color: white;
  font-size: 0.8rem;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  font-weight: 600;
}

/* .carousel-container {
  display: flex;
  align-items: center;
}

.carousel {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-item {
  display: flex;
  flex: 0 0 100%;
  justify-content: center;
} */

.v-btn {
  cursor: pointer;
}

.v-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
