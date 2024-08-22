<template>
  <div>
    날짜 / 멤버 / 환율계산기 / 여행자보험
    <v-btn @click="goDetail">
      지출내역
    </v-btn>
  </div>
</template>

<script setup>
import { useTripStore } from '@/stores/tripStore'

const store = useTripStore()

const goDetail = function () {
  store.tripProgressStage = 1
}
</script>

<style scoped>

</style>