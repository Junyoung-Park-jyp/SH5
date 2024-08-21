<template>
  <v-container>
    <CountryDateForm v-if="tripFormStage==0" />
    <MemberForm v-if="tripFormStage==1" />
    <AccountAdjustForm v-if="tripFormStage==2" />
    <v-row>
      <v-col cols="6">
        <v-btn>다음으로</v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn>취소하기</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import CountryDateForm from '@/components/TripReadyView/CountryDateForm.vue';
import MemberForm from '@/components/TripReadyView/MemberForm.vue';
import AccountAdjustForm from '@/components/TripReadyView/AccountAdjustForm.vue';
import TripCancel from '@/components/TripReadyView/TripCancel.vue';

import { useTripStore } from '@/stores/tripStore';

const tripStore = useTripStore();
const tripFormStage = tripStore.tripFormStage
</script>

<style scoped>

</style>