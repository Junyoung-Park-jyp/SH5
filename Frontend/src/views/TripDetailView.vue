<template>
  <div>
    <h1>
      최한진 님은 스페인 여행 {{ tripState }} 중
    </h1>

    <v-container>
      <v-row>
        <!-- ALL -->
        <v-col cols="1">
          <div>A</div>
          <div>ALL</div>
        </v-col>
        <!-- 준비 -->
        <v-col cols="1">
          <div>P</div>
          <div>준비</div>
        </v-col>
        <!-- 날짜 캐러셀 -->
        <v-col class="carousel-container" cols="9">
          <!-- 왼쪽 버튼 -->
          <v-btn density="compact" icon="mdi-chevron-left" @click="prevWeek" :disabled="currentWeekIndex === 0"></v-btn>
          <!-- 날짜 -->
          <div class="carousel">
            <div class="carousel-track" :style="trackStyle">
              <div v-for="(date, index) in weeks" :key="index" class="carousel-item">
                <div v-for="(day, i) in date" :key="i" class="day-container">
                  <div>{{ format(day, 'EEE') }}</div>
                  <div :class="{ 'today-circle': isToday(day) }">{{ format(day, 'dd') }}</div>
                  <div>{{ format(day, 'M') }}월</div>
                </div>
              </div>
            </div>
          </div>
          <!-- 오른쪽 버튼 -->
          <v-btn density="compact" icon="mdi-chevron-right" @click="nextWeek"
            :disabled="currentWeekIndex === weeks.length - 1"></v-btn>
        </v-col>
      </v-row>
    </v-container>

    <DetailReady v-if="tripState === '준비'" />
    <DetailProgress v-else />

    <v-btn @click="goFinish">정산하기</v-btn>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router'
import { eachDayOfInterval, format } from 'date-fns';

import DetailReady from '@/components/TripDetailView/DetailReady.vue';
import DetailProgress from '@/components/TripDetailView/DetailProgress.vue';

const router = useRouter();

// 오늘 날짜
const today = new Date();
today.setHours(0, 0, 0, 0)

// 여행 날짜
const startDate = new Date(2024, 7, 10);  // 2024년 8월 10일
const endDate = new Date(2024, 7, 27);  // 2024년 8월 27일

// 여행 날짜의 범위
const tripRange = eachDayOfInterval({
  start: startDate,
  end: endDate,
});

// 여행 상태
const tripState = ref('준비')

// 현재 날짜의 주차 인덱스
const currentWeekIndex = ref(0);

// 여행 날짜의 범위를 6일 단위로 구분
const weeks = [];
for (let i = 0; i < tripRange.length; i += 5) {
  const tmp = tripRange.slice(i, i + 5);
  weeks.push(tmp);
  if (tmp[0] <= today && today <= tmp[tmp.length - 1]) {
    currentWeekIndex.value = i / 5
    tripState.value = ''
  }
}

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

// 오늘 날짜인지를 판별
const isToday = (day) => {
  if (day.getFullYear() === today.getFullYear() && day.getMonth() === today.getMonth() && day.getDate() === today.getDate()) {
    return true
  } else {
    return false
  }
}

const trackStyle = computed(() => ({
  transform: `translateX(-${currentWeekIndex.value * 100}%)`,
}));

const goFinish = () => {
  return router.push({ name: 'tripFinish' })
}
</script>

<style scoped>
.carousel-container {
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
}

.day-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 6px;
}

.v-btn {
  cursor: pointer;
}

.v-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.today-circle {
  background-color: #4b72e1;
  color: white;
  border-radius: 24px;
  padding: 5px 10px;
}
</style>
