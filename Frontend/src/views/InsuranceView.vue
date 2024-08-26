<template>
  <div class="container">
    <!-- 뒤로가기 / 취소하기 -->
    <div class="header my-2">
      <div class="back">
        <v-icon class="btns" icon="mdi-arrow-left" size="xx-large" @click="backStep"></v-icon>
      </div>
    </div>

    <!-- MAIN -->
    <div class="main px-2">
      <!-- 각 단계에 따른 폼을 조건부로 렌더링 -->
       <InsuranceMain v-if="insuranceStage === 0" />
       <InsuranceDetail v-else-if="insuranceStage === 1" />
       <InsuranceMember v-else-if="insuranceStage === 2" />
       <InsuranceInvite v-else />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

import InsuranceMain from '@/components/InsuranceView/InsuranceMain.vue';
import InsuranceDetail from '@/components/InsuranceView/InsuranceDetail.vue';
import InsuranceMember from '@/components/InsuranceView/insuranceMember.vue';
import InsuranceInvite from '@/components/InsuranceView/insuranceInvite.vue';

const insuranceStage = ref(0)

const backStep = () => { };
</script>

<style scoped>
.container {
  width: 100%;
  height: 90vh;
  margin: 0px auto;
  padding: 10px 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main {
  margin: 30px auto 0px auto;
  width: 100%;
  overflow-y: scroll;
  scrollbar-width: none;
}
</style>