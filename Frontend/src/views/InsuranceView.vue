<template>
  <div class="container">
    <!-- 뒤로가기 / 취소하기 -->
    <div class="header my-2">
      <div class="back">
        <v-icon
         v-if="insuranceStage > 0"
          class="btns"
          icon="mdi-arrow-left"
          size="xx-large"
          @click="backStep"
        ></v-icon>
      </div>
      <div class="cancel">
        <v-icon
          class="btns"
          icon="mdi-window-close"
          size="xx-large"
          @click="cancelInsurance"
        ></v-icon>
      </div>
    </div>

    <!-- MAIN -->
    <div class="main px-2" ref="mainContainer">
      <!-- 각 단계에 따른 폼을 조건부로 렌더링 -->
      <InsuranceStart v-if="insuranceStage === 0" />
      <InsuranceMain v-if="insuranceStage === 1" />
      <InsuranceMember v-if="insuranceStage === 2" />
    </div>

    <!-- 다음으로 -->
    <div class="bottom">
      <button class="next-btn" @click="nextStep">다 &nbsp; 음</button>
    </div>

    <!-- 취소 모달 -->
    <v-dialog v-model="showCancelModal" max-width="400">
      <div class="modal-container">
        <div class="modal-message">
          <span>여행자 보험 가입을<br>취소하시겠습니까?</span>
        </div>
        <div class="modal-btns">
          <button class="modal-btn" @click="clearInsurance()">네</button>
          <button class="modal-btn" @click="closeCancelModal">아니오</button>
        </div>
      </div>
    </v-dialog>

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
import { ref, watch, nextTick } from "vue";
import { useRouter, useRoute } from "vue-router";

import InsuranceStart from "@/components/InsuranceView/InsuranceStart.vue";
import InsuranceMain from "@/components/InsuranceView/InsuranceMain.vue";
import InsuranceMember from "@/components/InsuranceView/InsuranceMember.vue";

const insuranceStage = ref(0);
const mainContainer = ref(null);
const showCancelModal = ref(false);
const router = useRouter();
const route = useRoute();

// URL에서 tripId를 가져옴
const tripId = route.params.id;


const scrollToTop = () => {
  if (mainContainer.value) {
    mainContainer.value.scrollTop = 0; // mainContainer의 스크롤을 맨 위로 이동
  }
};

const nextStep = () => {
  if (insuranceStage.value < 2) {
    insuranceStage.value++;
  } else {
    router.push({ name: 'tripMain', params: { id: tripId } });
  }

  nextTick(() => {
    scrollToTop();
  });
};

const backStep = () => {
  if (insuranceStage.value > 0) {
    insuranceStage.value--;
    console.log(insuranceStage.value)
  }
};

const cancelInsurance = () => {
  showCancelModal.value = true;
};

const closeCancelModal = () => {
  showCancelModal.value = false;
};

const clearInsurance = () => {
  if (tripId) {
    insuranceStage.value = 0;
    showCancelModal.value = false;
    router.replace({ name: "tripMain", params: { id: tripId } });
  } else {
    console.error("Invalid tripId:", tripId);
  }
};

// watch 사용하여 insuranceStage가 변경될 때 스크롤 위치 조정
watch(insuranceStage, () => {
  nextTick(() => {
    scrollToTop();
  });
});
</script>

<style scoped>
.container {
  width: 100%;
  height: 90vh;
  margin: 0px auto;
  padding: 0px 10px;
  background-color: #f4f6fa;
  /* border: 5px solid black; */
}

.header {
  position: fixed;
  top: 60px;
  left: 0;
  z-index: 1000;
  width: 100%;
  text-align: center;
  padding: 10px;
  margin: 0 auto;
  background-color: #f4f6fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main {
  margin: 0px auto 0px auto;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  padding-top: 60px;
  padding-bottom: 0px;
  /* border: 1px solid black; */
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

 /* 모달 */
 .modal-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  border-radius: 10px;
  margin: 0px auto;
  width: 90%;
  height: 150px;
  color: black;
}

.modal-message {
  text-align: center;
  margin: 10px 0px;
  font-size: large;
}

.modal-btns {
  margin: 10px 5px;
}

.modal-btn {
  background-color: lightgrey;
  text-align: center;
  width: 120px;
  margin: 0px 5px;
  padding: 10px 10px;
  border-radius: 10px;
}

.modal-btn:hover,
.modal-btn:click {
  background-color: grey;
}
</style>
