<template>
  <div class="container">
    <!-- 뒤로가기 / 취소하기 -->
    <div class="header my-2">
      <div class="back">
        <v-icon class="btns" icon="mdi-arrow-left" size="xx-large" @click="backStep"></v-icon>
      </div>
      <div class="cancel">
        <v-icon class="btns" icon="mdi-window-close" size="xx-large" @click="cancelTrip"></v-icon>
      </div>
    </div>

    <!-- MAIN -->
    <div class="main px-2">
      <!-- 각 단계에 따른 폼을 조건부로 렌더링 -->
      <CountryDateForm v-if="tripFormStage == 0" />
      <MemberForm v-if="tripFormStage == 1" />
      <AccountAdjustForm v-if="tripFormStage == 2" />
    </div>
    
    <!-- 다음으로 -->
    <div class="bottom">
      <button class="next-btn" @click="nextStep">다 &nbsp; 음</button>
    </div>

    <!-- 모달 다이얼로그 통합 -->
    <!-- <v-dialog v-model="showCancelModal" max-width="400">
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
    </v-dialog> -->

    <v-dialog v-model="showCancelModal" max-width="400">
      <div class="modal-container">
        <div class="modal-message">
          <span>여행 생성을 취소하시겠습니까?</span>
        </div>
        <div class="modal-btns">
          <button class="modal-btn" @click="clearTrip">네</button>
          <button class="modal-btn"@click="closeCancelModal">아니오</button>
        </div>
      </div>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import CountryDateForm from '@/components/TripCreateView/CountryDateForm.vue';
import MemberForm from '@/components/TripCreateView/MemberForm.vue';
import AccountAdjustForm from '@/components/TripCreateView/AccountAdjustForm.vue';
import { useTripStore } from '@/stores/tripStore';
import { useBalanceStore } from '@/stores/balanceStore';

const tripStore = useTripStore();
const balanceStore = useBalanceStore();
const tripFormStage = ref(0) // 초기 스테이지 설정
const showCancelModal = ref(false);
const router = useRouter();

const cancelTrip = () => {
  showCancelModal.value = true;
};

const closeCancelModal = () => {
  showCancelModal.value = false;
};

const clearTrip = () => {
  tripStore.clearTrip();
  tripFormStage.value = 0
  showCancelModal.value = false
  router.replace({ name: 'home' });
};

const backStep = () => {

}

const nextStep = () => {
  if (tripFormStage.value == 0) {
    if (tripStore.country != '' && tripStore.startDate != null && tripStore.endDate != null) {
      tripFormStage.value++;
    } else {
      // alert('누락된 정보가 있습니다!');
      tripFormStage.value++; // 정보가 누락되었어도 다음 단계로 진행
    }
  } else if (tripFormStage.value == 1) {
    if (tripStore.members.length > 0) {
      tripFormStage.value++;
    } else {
      // alert('누락된 정보가 있습니다!');
      tripFormStage.value++; // 정보가 누락되었어도 다음 단계로 진행
    }
  } else if (tripFormStage.value == 2) {
    if (balanceStore.bank) {
      showLoadingSequence(); // 여행 생성 중 -> 여행 생성 완료 -> 이동 시퀀스 시작
    } else {
      // alert('누락된 정보가 있습니다!');
      showLoadingSequence(); // 정보가 누락되었어도 시퀀스 실행
    }
  }
};

const showLoadingSequence = () => {
  // "여행 생성 중" 페이지로 이동
  router.push({
    name: 'loadingMessage',
    params: {
      message: '여행 생성 중...',
      status: 'loading', // 여행 생성 중 상태
    },
  });

  // 2초 후 "여행 생성 완료" 메시지로 변경
  setTimeout(() => {
    router.push({
      name: 'loadingMessage',
      params: {
        message: '여행 생성 완료',
        status: 'success', // 여행 생성 완료 상태
      },
    });

    // 1.5초 후 TripView로 이동
    setTimeout(() => {
      router.replace({ name: 'trip' });
    }, 1500);
  }, 2000);
};
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

.bottom {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  text-align: center;
  padding: 20px 0;
  margin: 0 auto;
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
}

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

.modal-btn:hover, .modal-btn:click {
  background-color: grey;
}

</style>