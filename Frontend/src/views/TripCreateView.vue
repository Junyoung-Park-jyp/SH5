<template>
  <v-container>
    <!-- 각 단계에 따른 폼을 조건부로 렌더링 -->
    <CountryDateForm v-if="tripFormStage === 0" />
    <MemberForm v-if="tripFormStage === 1" />
    <AccountAdjustForm v-if="tripFormStage === 2" />

    <v-row>
      <v-col cols="6">
        <v-btn @click="nextStep">다음으로</v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn @click="cancelTrip">취소하기</v-btn>
      </v-col>
    </v-row>

    <!-- 모달 다이얼로그 통합 -->
    <v-dialog v-model="showCancelModal" max-width="400">
      <v-card>
        <v-card-title>
          <span class="text-h5">여행 생성을 취소할까요?</span>
        </v-card-title>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="clearTrip">네</v-btn>
          <v-btn text @click="closeCancelModal">아니오</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CountryDateForm from '@/components/TripCreateView/CountryDateForm.vue';
import MemberForm from '@/components/TripCreateView/MemberForm.vue';
import AccountAdjustForm from '@/components/TripCreateView/AccountAdjustForm.vue';

import { useTripStore } from '@/stores/tripStore';

const tripStore = useTripStore();
const tripFormStage = ref(0); // 초기 스테이지 설정
const showCancelModal = ref(false);
const router = useRouter();

const cancelTrip = () => {
  showCancelModal.value = true;
};

const closeCancelModal = () => {
  showCancelModal.value = false;
};

const clearTrip = () => {
  console.log("clear")
  tripStore.clearTravel();
  router.replace({ name: 'trip' });
};

const nextStep = () => {
  if (tripFormStage.value < 2) {
    tripFormStage.value++;
  }
};
</script>

<style scoped>
</style>