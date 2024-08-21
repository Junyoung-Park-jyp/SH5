<template>
  <v-container>
    {{ tripStore.travelExperiences }}
    <v-row>
      {{ userStore.name }} 님
    </v-row>
    <v-row>
      <v-icon icon="mdi-music"></v-icon>
      <div>현재 {{ tripStore.country }} 여행 중</div>
      <v-icon icon="mdi-music"></v-icon>
    </v-row>
    <v-row>
      총 0회 SOL로 여행을 다녀오셨네요!
      <v-container>
        <v-row>
          <v-col></v-col>
        </v-row>
      </v-container>
    </v-row>
    <v-btn>여행 만들기</v-btn>
  </v-container>
</template>

<script setup>
import { useUserStore } from '@/stores/userStore';
import { useTripStore } from '@/stores/tripStore';

const userStore = useUserStore()
const tripStore = useTripStore()
</script>

<style scoped>

</style>