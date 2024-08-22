<template>
  <div>
    날짜 / 멤버 / 환율계산기 / 여행자보험
    {{ tripStore.tripProgressStage }}
    <v-btn @click="goDetail">
      지출내역
    </v-btn>
  </div>
</template>

<script setup>
import { useTripStore } from '@/stores/tripStore'

const tripStore = useTripStore()

const goDetail = function () {
  tripStore.tripProgressStage = 1
}
</script>

<style scoped>

</style>