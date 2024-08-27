<template>
  <div class="main-container">
    <h1>날짜</h1>
    <v-row>
      <!-- <p>시작일 | {{ tripData.startDate }}</p>
      <p>종료일 | {{ tripData.endDate }}</p> -->
      <p>시작일 | 2024년 8월 25일</p>
      <p>종료일 | 2024년 8월 27일</p>
    </v-row>
    <h1>멤버</h1>
    <!-- <span>{{ tripData.members.length }}명</span> -->
    <span>4명</span>
    <v-row>
      <!-- 멤버들 반복 v-for로 줄 곳 -->
      <!-- <div v-for="member in tripData.members">
        <div>{{ member.name }}</div>
      </div> -->
      <div>최</div>
      <div>박</div>
      <div>임</div>
      <div>정</div>
    </v-row>
    <h1>여행 스케치</h1>
    <v-row>
      <!-- 그림 들어갈 자리 -->
      <DrawPicture />
    </v-row>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useTripStore } from '@/stores/tripStore';
import { useRoute } from 'vue-router'

import DrawPicture from './DrawPicture.vue';

// const route = useRoute()
// const tripStore = useTripStore()
// const tripId = route.params.tripId
// const tripData = computed(() => {
//   return tripStore.getTrip(tripId)
// })
</script>

<style scoped></style>