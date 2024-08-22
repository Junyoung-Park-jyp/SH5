<template>
  <div>
    <h1>최한진 님은 스페인 여행 중</h1>
    <TripInfoMain v-if="store.tripProgressStage === 0" />
    <TripInfoDetail v-if="store.tripProgressStage === 1" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import TripInfoMain from '@/components/TripProgressView/TripInfoMain.vue'
import TripInfoDetail from '@/components/TripProgressView/TripInfoDetail.vue'

import { useTripStore } from '@/stores/tripStore'

const store = useTripStore()
</script>

<style scoped></style>