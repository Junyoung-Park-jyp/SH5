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

    <!-- footer -->
    <div class="sticky-container">
      <div class="footer">
        <div class="d-flex justify-space-between">
          <div>
            예산 보험료
            <v-icon icon="mdi-help-circle-outline"></v-icon>
          </div>
          <div>
            6000원
          </div>
        </div>
        <v-btn @click="nextStep">다 음</v-btn>
      </div>
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

const nextStep = () => {
  insuranceStage.value++;
}

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

/* footer */
.sticky-container {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  margin: 0px auto;
  padding: 0px;
  background-color: white;  /* 추가: 배경색 지정으로 투명도를 방지 */
  width: 100%;
}

.footer {
  border-top: 1px solid #e0e0e0;
  width: auto;
}
</style>