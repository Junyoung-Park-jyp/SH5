<template>
  <div>
    <div class="carousel-container">
      <button @click="prevWeek" :disabled="currentWeek === 0">
        <v-icon icon="mdi-chevron-left"></v-icon>
      </button>
      <div class="carousel">
        <div class="carousel-track" :style="trackStyle">
          <div v-for="(date, index) in weeks" :key="index" class="carousel-item">
            <div v-for="(day, i) in date" :key="i" class="day-container">
              <div class="month">{{ formatMonth(day) }}</div>
              <div class="day">{{ formatDay(day) }}</div>
              <div class="weekday">{{ formatWeekday(day) }}</div>
            </div>
          </div>
        </div>
      </div>
      <button @click="nextWeek" :disabled="currentWeek === weeksLength - 1">
        <v-icon icon="mdi-chevron-right"></v-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { eachDayOfInterval, format } from 'date-fns';

const startDate = ref(new Date(2024, 7, 30));
const endDate = ref(new Date(2024, 8, 20));

const dateRange = computed(() => {
  return eachDayOfInterval({
    start: startDate.value,
    end: endDate.value,
  });
});

const weeks = computed(() => {
  const tmp = [];
  for (let i = 0; i < dateRange.value.length; i+=7) {
    tmp.push(dateRange.value.slice(i, i + 7));
  }
  return tmp;
});

const currentWeek = ref(0);

const weeksLength = computed(() => weeks.value.length);

// 날짜 포맷팅 함수들
const formatDay = (date) => format(date, 'dd');
const formatMonth = (date) => format(date, 'MMM');
const formatWeekday = (date) => format(date, 'EEE');

const prevWeek = () => {
  if (currentWeek.value > 0) {
    currentWeek.value--;
  }
};

const nextWeek = () => {
  if (currentWeek.value < weeksLength.value - 1) {
    currentWeek.value++;
  }
};

// 캐러셀 트랙의 스타일 계산
const trackStyle = computed(() => ({
  transform: `translateX(-${currentWeek.value * 100}%)`,
}));
</script>

<style scoped>
.carousel-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.carousel {
  overflow: hidden;
  width: 70%;
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
  margin: 0 10px;
}

.month {
  font-size: 0.8rem;
  color: gray;
}

.day {
  font-size: 1.5rem;
  font-weight: bold;
}

.weekday {
  font-size: 0.8rem;
  color: gray;
}

button {
  padding: 5px 10px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
