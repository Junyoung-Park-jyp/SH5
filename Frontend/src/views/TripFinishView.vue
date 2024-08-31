<template>
  <div class="main-container">
    <!-- 뒤로가기 & 취소하기 -->
    <div class="header my-2">
      <!-- BACK -->
      <!-- <div class="back" @click="backStep">
        <button class="icon-btn">
          <v-icon
            class="btns"
            icon="mdi-arrow-left"
            size="large"
          ></v-icon>
        </button>
      </div> -->
      <!-- 취소 -->
      <div class="cancel">
        <v-icon
          class="btns"
          icon="mdi-window-close"
          size="large"
          @click="cancelTrip"
        ></v-icon>
      </div>
    </div>
    
    <!-- 정산완료 -->
    <div class="complete">
      <div class="img"><img src="@/assets/img/check.png" alt="체크" /></div>
      <div class="amount">{{ formatWithComma(amount) }}</div>
      <div class="message">정 산 완 료</div>
    </div>
    
    <!-- 입금/출금 -->
    <div class="type">
      <div class="withdraw">
        <div class="withdraw-img">
          <img src="@/assets/img/withdraw.png" alt="출금" />
        </div>
        <div class="withdraw-list">
          <div v-for="(member, index) in budgetData" :key="index" class="progress-container">
            <div class="progress-text">
              {{ member.member }} {{ calculateProgress(member) }}%
            </div>
            <div class="progress-bar">
              <div
                class="progress"
                :style="{ width: calculateProgress(member) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- 상세내역 -->
    <div class="detail">
      <table class="settlement-table">
        <thead>
          <tr>
            <th></th>
            <th style="border: 1px dashed lightgrey">지출금</th>
            <th style="border: 1px dashed lightgrey">정산금</th>
            <th style="border: 1px dashed lightgrey">남은 예산</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(budgets, index) in budgetData" :key="index">
            <td class="member-td">
              <div
                class="member-symbol member d-flex justify-center align-center"
                :style="{
                  backgroundColor: rgbaColor(memberColors[index], 0.7),
                }"
              >
                <div class="member-familyname">
                  {{ budgets.member.slice(0, 1) }}
                </div>
              </div>
            </td>
            <td style="border: 1px dashed lightgrey">
              {{ formatWithComma(budgets.used_budget) }}
            </td>
            <td
              style="border: 1px dashed lightgrey"
              :class="{
                negative: budgets.adjustment > 0,
                positive: budgets.adjustment < 0,
              }"
            >
              {{ budgets.adjustment > 0 ? "-" : "" }}
              {{ formatWithComma(budgets.adjustment) }}
            </td>
            <td style="border: 1px dashed lightgrey">
              {{ formatWithComma(budgets.remain_budget) }}
            </td>
          </tr>

        </tbody>
      </table>
      <div class="explanation">(개인별) 남은 예산 = 초기 예산 - 총 지출금 </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useMemberColors } from "@/stores/colorStore";
import { formatWithComma } from "@/stores/currencyStore";
import { useRoute, useRouter } from "vue-router";
import { useTripStore } from "@/stores/tripStore";
import { usePaymentStore } from "@/stores/paymentStore";

const route = useRoute();
const router = useRouter();
const tripId = route.params.id;

const amount = ref(route.query.amount || 0);
const tripStore = useTripStore();
const paymentStore = usePaymentStore();
const tripMembers = computed(() => tripStore.members);

const budget = computed(()=> paymentStore.budgets)

const budgetData= computed(() => {
  return Object.entries(budget.value).map(([name, data]) => ({
    member: name,
    used_budget: data.used_budget,
    adjustment: data.initial_budget - data.remain_budget,
    remain_budget: data.remain_budget,
    initial_budget: data.initial_budget,
  }));
});


const adjustmentResult = computed(() => paymentStore.adjustmentResult)
// computed 값은 변경할 수 없으므로, 별도의 ref로 상태 관리
const membersWithColors = ref([]);

const { memberColors, rgbaColor } = useMemberColors(tripMembers);

// const withdrawList = computed(() => {
//   const result = [];
  
//   // adjustmentsResult가 정의되어 있는지 확인
//   if (!adjustmentResult.value) {
//     return result;
//   }

//   for (const [name, balance] of Object.entries(adjustmentResult.value)) {
//     if (balance.difference < 0) {
//       result.push({
//         name,
//         amount: Math.abs(balance.difference),
//       });
//     }
//   }
//   return result;
// });

// `onMounted`에서 `membersWithColors`를 초기화
onMounted(() => {
  membersWithColors.value = tripMembers.value.map((member, index) => ({
    ...member,
    color: memberColors.value[index],
  }));

  // 프로그레스바 애니메이션 시작
  nextTick(() => {
    const progressBars = document.querySelectorAll('.progress');
    progressBars.forEach((el, index) => {
      const member = budgetData.value[index];
      el.style.width = calculateProgress(member) + '%';
    });
  });
});


const backStep = () => {
  amount.value = 0;
  router.replace({ name: "tripDetail", params: { id: tripId } });
};

const cancelTrip = () => {
  amount.value = 0;
  router.replace({ name: "tripDetail", params: { id: tripId}});
};

// 프로그레스바
const calculateProgress = (member) => {
  if (member.initial_budget === 0) return 0;
  return Math.round((member.used_budget / member.initial_budget) * 100);
};
</script>

<style scoped>
.main-container {
  height: 92vh;
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 0px;
  background-color: #f4f6fa;
}
.header {
  position: fixed;
  top: 45px;
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
  /* border: 1px solid black; */
}

/* 정산 완료  */
.complete {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: #4b72e1;
  margin: 0px auto;
  margin-top: 30px;
  /* border: 1px solid black; */
}

.img {
  margin: 0;
  padding: 0;
  /* border: 1px solid black; */
}


.img > img {
  height: 60px;
  width: 60px;
}

.amount {
  width: 100%;
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: end;
  text-align: center;
  color: #4b72e1;
  font-size: xx-large;
  font-weight: bolder;
  margin: 0px auto;
  padding: 0px;
  /* padding-bottom: 30px; */
  /* border: 1px solid black; */
}

.message {
  font-size: 22px;
  font-weight: bolder;
}

/* 입금 로고 */
.type {
  background-color: #ffffff;
  width: 100%;
  height: 350px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  /* border: 1px solid blue; */
  margin: auto;
  font-size: large;
}

.withdraw,
.deposit {
  height: 50%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  text-align: center;
  font-weight: bold;
  /* border: 1px solid green; */
}

.withdraw-img,
.deposit-img {
  width: 70px;
  margin: auto 25px auto 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* border: 1px solid red; */
}

.withdraw-img img,
.deposit-img img {
  height: 55px;
  width: 40px;
  /* border: 1px solid black; */
  margin: auto;
}

.withdraw-list,
.deposit-list {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 70%;
  margin-right: 40px;
  text-align: left;
  font-size: 15px;
  /* border: 1px solid blue; */
}

/* 프로그레스바 */
.progress-container {
  /* border: 1px solid black; */
  margin-bottom: 10px;
  width: 100%;
}

.progress-bar {
  background-color: #e0e0e0;
  border-radius: 5px;
  width: 90%;
  height: 15px;
  margin-bottom: 5px;
  position: relative;
}

.progress {
  background-color: #4b72e1;
  height: 100%;
  border-radius: 5px;
  width: 0;
  transition: width 2s ease;
}

@keyframes fillProgressBar {
  0% {
    width: -100%;
  }
  100% {
    width: 100%;
  }
}

.progress.animate {
  animation: fillProgressBar 3s forwards;
}

.progress-text {
  font-size: 12px;
  color: #333;
}


.detail {
  width: 100%;
  height: 70%;
  background-color: #ffffff;
  margin: auto;
  margin-top: -10px;
  padding: 3px 15px 5px 0px;
}

.settlement-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 1.2rem;
  margin: 30px auto 5px auto;
}

.settlement-table thead tr th {
  font-weight: bold;
}

.settlement-table th,
.settlement-table td {
  padding: 10px;
  /* border: 1px dashed lightgrey; */
}

.settlement-table td {
  font-size: 15px;
}

.settlement-table .member {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: large;
}

.member-td {
  text-align: center;
  display: flex;
  justify-content: center;
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 35px;
  height: 35px;
}

.positive {
  color: #1d72e7;
  font-weight: bold;
}

.negative {
  color: #e71d1d;
  font-weight: bold;
}

.explanation {
  width: 100%;
  margin: 0px auto;
  text-align: right;
  padding-right: 10px;
  font-size: 0.8rem;
}
</style>
