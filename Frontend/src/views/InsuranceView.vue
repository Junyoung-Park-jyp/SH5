<template>
  <div class="container">
    <!-- 뒤로가기 / 취소하기 -->
    <div class="header my-2">
      <div class="back">
        <v-icon
          class="btns"
          icon="mdi-arrow-left"
          size="xx-large"
          @click="backStep"
        ></v-icon>
      </div>
    </div>

    <!-- MAIN -->
    <div class="main px-2">
      <!-- 각 단계에 따른 폼을 조건부로 렌더링 -->
      <InsuranceStart v-if="insuranceStage === 0" />
      <InsuranceMain v-if="insuranceStage === 1" />
      <InsuranceMember v-if="insuranceStage === 2" />
    </div>

    <!-- 다음으로 -->
    <div class="bottom">
      <button class="next-btn" @click="nextStep">다 &nbsp; 음</button>
    </div>

    <!-- footer -->
    <!-- <div class="sticky-container">
      <div class="footer">
        <div class="d-flex justify-space-between">
          <div>
            예산 보험료
            <v-icon icon="mdi-help-circle-outline"></v-icon>
          </div>
          <div>6000원</div>
        </div>
        <v-btn @click="nextStep">다 음</v-btn>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import InsuranceStart from "@/components/InsuranceView/InsuranceStart.vue";
import InsuranceMain from "@/components/InsuranceView/InsuranceMain.vue";
import InsuranceMember from "@/components/InsuranceView/InsuranceMember.vue";

const insuranceStage = ref(0);
const router = useRouter();

const nextStep = () => {
  if (insuranceStage.value < 2) {
    insuranceStage.value++;
  } else {
    router.push({ name: 'tripMain' });
  }
};

const backStep = () => {};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100vh;
  margin: 0px auto;
  padding: 0px 10px;
  /* border: 5px solid black; */
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

.bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  padding: 0px;
  width: 100%;
  text-align: center;
  padding: 20px 0;
  margin: 0 auto;
  background-color: #ffffff;
}

.next-btn {
  width: 80%;
  background-color: #4b72e1;
  border-radius: 30px;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin: auto;
}

/* footer */
/* .sticky-container {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  margin: 0px auto;
  padding: 0px;
  background-color: white;
  width: 100%;
}

.footer {
  border-top: 1px solid #e0e0e0;
  width: auto;
} */
</style>
