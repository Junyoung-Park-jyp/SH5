<template>
  <div class="main-container">
    <div class="title">보험료 결제</div>
    <div class="explanation">함께 가입할 분이 있다면<br>추가해주세요</div>
    <div class="register-info">
      <div>본인 포함 최대 10명까지 가입할 수 있어요.</div>
    </div>

    <!-- 큐알 -->
    <div class="qr">
      <button @click="qrInvite">QR 로 한 번에 초대하기</button>
    </div>

    <!-- 모달 -->
    <v-dialog v-model="showModal" max-width="400">
      <div class="modal-container">
        <div class="modal-message">
          <div class="modal-header">
            <div>신한 SOL 트래블 해외여행보험</div>
            <div class="close" @click="showModal = false">&times;</div>
          </div>
          <img class="qr-code" src="@/assets/img/qr-code.png" alt="QR" @click="navigateToUrl">
          <div class="modal-content">
            <div style="font-weight: bold;">카메라를 켜고 QR코드를 인식해주세요.</div>
            <div class="detail">신한 SOL 트래블 해외여행보험 바코드<br>이미지 클릭시 다이렉트로 이동합니다.</div>
          </div>
        </div>
      </div>
    </v-dialog>

    <!-- 멤버 -->
    <div class="member">
      <div
        v-for="(member, index) in tripMembers"
        :key="index"
        class="d-flex content"
      >
        <div class="member-list">
          <div
            class="member-symbol d-flex justify-center align-center"
            :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }"
          >
            <div class="member-familyname">{{ member.name.slice(0, 1) }}</div>
          </div>
          <div class="member-name">{{ member.name }}</div>
        </div>
        <div class="invite">
          <button class="invite-btn" :class="{ 'clicked': member.invited }" @click="inviteMember(index)">{{ member.invited ? '초대완료' : '+ 초대하기' }}</button>
        </div>
      </div>
    </div>

    <div class="image">
      <img src="@/assets/img/friend.jpg" alt="동반 추가" />
    </div>

    <!-- 예상 보험료 -->
    <div class="bottom">
      <div class="price-info">보험료
        <div class="discount" v-if="totalInvited > 0">
          <span class="blue">{{ discountPercentage }}% 할인</span>
        </div>
      </div>
      <div class="amount">
        &nbsp; 인당
        <div class="before" :class="{ 'cancel': totalInvited > 0 }">{{ formatWithComma(basePrice) }}원</div>
        <div class="after" v-if="totalInvited > 0">
          <span class="blue">{{ formatWithComma(discountedPrice) }}</span>&nbsp;원
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useMemberColors } from "@/stores/colorStore";
import { formatWithComma } from "@/stores/currencyStore";

const showModal = ref(false);
const basePrice = 15500;

// 여행 멤버와 계좌번호
const tripMembers = ref([
  { name: "박준영", account: "신한 0276524561730773", invited: false },
  { name: "이선재", account: "신한 000-000-000", invited: false },
  { name: "임광영", account: "국민 000-000-000", invited: false },
  { name: "정태완", account: "우리 000-000-000", invited: false },
  { name: "최한진", account: "계좌 미등록", invited: false },
]);

const { memberColors, rgbaColor } = useMemberColors(tripMembers.value);

const totalInvited = computed(() => {
  return tripMembers.value.filter(member => member.invited).length;
});

const discountPercentage = computed(() => {
  if (totalInvited.value === 1) {
    return 5; // 5% 할인
  } else if (totalInvited.value >= 2) {
    return 10; // 10% 할인
  } else {
    return 0;
  }
});

const discountedPrice = computed(() => {
  if (totalInvited.value === 1) {
    return (basePrice * 0.95).toFixed(0); // 5% 할인
  } else if (totalInvited.value > 1) {
    return (basePrice * 0.90).toFixed(0); // 10% 할인
  } else {
    return basePrice;
  }
});

const inviteMember = (index) => {
  tripMembers.value[index].invited = !tripMembers.value[index].invited;
};

// QR 모달
const qrInvite = () => {
  showModal.value = true;
};

// 이미지 클릭 시 호출되는 함수
const navigateToUrl = () => {
  window.location.href = 'https://direct.shinhanez.co.kr/#PDROTIOTI_M01';
};
</script>

<style scoped>
.main-container {
  width: 100%;
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 150px;
  /* background-color: #f4f6fa; */
}

.title {
  color: #4b72e1;
  font-weight: 500;
  font-size: 0.8rem;
}

.explanation {
  font-size: 1.5rem;
  font-weight: bold;
}

.register-info {
  display: flex;
  margin: 10px auto;
  color: #878787;
  font-size: 0.8rem;
}

/* 큐알 */
.qr {
  text-align: center;
  color: #4b72e1;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 50px auto 10px auto;
}

/* 모달 스타일 */
.modal-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  border-radius: 10px;
  margin: 0px auto;
  width: 90%;
  height: 450px;
  color: black;
}

.modal-message {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 0 auto;
  height: 100%;
  font-size: 16px;
  /* border: 1px solid black; */
}

.modal-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0px 20px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.qr-code {
  width: 100%;
  padding: 0 10px;
}

.modal-content {
  margin: 10px 20px;
  font-size: 14px;
}

.detail {
  margin: 2px auto;
  font-size: 12px;
}

/* 멤버 */
.member {
  width: 100%;
  margin: auto;
  display: flex;
  flex-direction: column;
  justify-content:space-evenly;
  align-content: center;
  text-align: center;
  margin: 20px auto 50px auto;
  /* border: 1px solid black; */
}

.content {
  width: 100%;
  margin: auto;
  display: flex;
  flex-direction: row;
  justify-content:space-between;
  align-content: center;
  text-align: center;
  background-color: #ffffff;
  padding: 10px 20px;
}

.content * {
  font-size: 1.1rem;
}

.member-list {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
  /* border: 1px solid blue; */
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  margin-right: 15px;
}

.member-name {
  width: 50px;
}

.invite {
  width: 80px;
  text-align: right;
}

.invite-btn {
  color: #878787;
  font-size: 0.9rem;
}

.clicked {
  color: #4b72e1;
}


/* 이미지 */
.image {
  width: 100%;
  /* border: 1px solid black; */
}

.image > img {
  width: 100%;
}

/* 하단 */
.bottom {
  position: fixed;
  bottom: 80px;
  left: 0;
  z-index: 1000;
  padding: 0px;
  width: 100%;
  text-align: center;
  padding: 20px 25px;
  margin: auto;
  background-color: #ffffff;
  /* border: 1px solid black; */
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: start;
  align-content: start;
  text-align: center;

  border-radius: 30px 30px 0px 0px;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0px -4px 6px rgba(0, 0, 0, 0.1);
}

.price-info {
  display: flex;
  gap: 5px;
}

.amount {
  display: flex;
  height: 100%;
  /* border: 1px solid blue; */
}

.cancel {
  text-decoration: line-through;
  margin: 0px 5px;
}

.real {
  display: flex;
  font-weight: bold;
}

.blue {
  font-weight: bold;
  color: #4b72e1;
}

</style>
