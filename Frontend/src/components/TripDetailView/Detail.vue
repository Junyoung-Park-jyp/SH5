<template>
  <div v-if="payments" class="main-container">
    <div class="content-container">
      <!-- 예산 -->
      <div
        v-if="showAllContainers || showBudgetAndBookingOnly"
        class="budget-container"
      >
        <div class="title d-flex justify-space-between" @click="checkData">
          <div class="prepare">준비</div>
          <div class="line">&nbsp;|&nbsp;</div>
          <div class="budget">예산</div>
          <v-spacer></v-spacer>
          <div class="sum" @click="toggleCurrency">
            {{ formattedTotalBalance }}
          </div>
        </div>
        <div class="budget-content">
          <div class="left-detail">
            <v-icon icon="mdi-wallet-outline" color="grey" size="28px"></v-icon>
          </div>
          <div class="right-detail">
            <div
              v-for="(member, index) in tripMembers"
              :key="index"
              class="member-info"
            >
              <!-- 심볼 -->
              <div
                class="member-symbol d-flex justify-center align-center"
                :style="{
                  backgroundColor: rgbaColor(memberColors[index], 0.7),
                }"
                @click="changeColor(index)"
              >
                <div class="member-familyname">
                  {{ member.member.slice(0, 1) }}
                </div>
              </div>
              <div class="member-balance" @click="toggleCurrency">
                {{ formattedMemberBalance(member.balance) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 준비 | 사전 예약 -->
      <div
        v-if="
          bookingPayments.length &&
          (showAllContainers || showBudgetAndBookingOnly)
        "
        class="booking-container"
      >
        <div class="title d-flex justify-space-between" >
          <div class="subtitle">준비 &nbsp;|&nbsp; 사전 예약</div>
          <v-spacer></v-spacer>
          <div class="sum" @click="toggleCurrency">
            {{ formattedTotalCost(bookingPayments) }}
          </div>
        </div>
        <div class="book-content">
          <div
            class="payment"
            v-for="(payment, paymentIndex) in bookingPayments"
            :key="paymentIndex"
          >
            <!-- 체크 버튼 -->
            <div class="check-area">
              <v-btn
                @click="toggleCheck(paymentIndex, 'booking')"
                variant="text"
                :color="payment.checked ? 'primary' : 'grey'"
                :icon="
                  payment.checked
                    ? 'mdi-check-circle'
                    : 'mdi-checkbox-blank-circle-outline'
                "
              ></v-btn>
            </div>

            <!-- 카테고리 -->
            <div class="category-area">
              <v-icon icon="mdi-airplane" color="grey" size="large"></v-icon>
            </div>

            <!-- 결제 금액 및 내역 -->
            <div class="cost-area">
              <div class="cost" @click="toggleCurrency">
                {{ formattedCost(payment.amount) }}
              </div>
              <div class="name">{{ payment.brand_name }}</div>
            </div>

            <!-- 정산 대상 -->
            <div class="person-area">
              <div
                v-for="(member, index) in tripMembers"
                :key="index"
                class="person-info"
              >
                <div
                  class="person-symbol d-flex justify-center align-center"
                  :style="personStyle(member.member, payment.members, index)"
                  @click="personClick(paymentIndex, member.member, 'booking')"
                >
                  <div class="person-familyname">
                    {{ member.member.slice(0, 1) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 결제 날짜 -->
            <div class="date-area">
              {{ formatDate(payment.pay_date) }}
              {{ formatTime(payment.pay_time) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 결제 | 지출 -->
      <div
        v-if="
          filteredPayments.length &&
          (showAllContainers || !showBudgetAndBookingOnly)
        "
        class="pay-container"
      >
        <div class="title d-flex justify-space-between">
          <div class="subtitle">결제 &nbsp;|&nbsp; 지출</div>
          <v-spacer></v-spacer>
          <div class="sum" @click="toggleCurrency">
            {{ formattedTotalCost(filteredPayments) }}
          </div>
        </div>
        <div class="pay-content">
          <div
            class="payment"
            v-for="(payment, paymentIndex) in filteredPayments"
            :key="paymentIndex"
          >
            <!-- 체크 버튼 -->
            <div class="check-area">
              <v-btn
                @click="toggleCheck(paymentIndex, 'trip')"
                variant="text"
                :color="payment.checked ? 'primary' : 'grey'"
                :icon="
                  payment.checked
                    ? 'mdi-check-circle'
                    : 'mdi-checkbox-blank-circle-outline'
                "
              ></v-btn>
            </div>

            <!-- 카테고리 -->
            <div class="category-area">
              <v-icon icon="mdi-airplane" color="grey" size="large"></v-icon>
              <div>{{ payment.category }}</div>
            </div>

            <!-- 결제 금액 및 내역 -->
            <div class="cost-area">
              <div class="cost" @click="toggleCurrency">
                {{ formattedCost(payment.amount) }}
              </div>
              <div class="name">{{ payment.brand_name }}</div>
            </div>

            <!-- 정산 대상 -->
            <div class="person-area">
              <div
                v-for="(member, index) in tripMembers"
                :key="index"
                class="person-info"
              >
                {{ member.member[0] }}
                <!-- <div
                  class="person-symbol d-flex justify-center align-center"
                  :style="personStyle(member.member, index)"
                  @click="personClick(paymentIndex, member.member, 'trip')"
                >
                  <div class="person-familyname">
                    {{ member.member.slice(0, 1) }}
                  </div>
                </div> -->
              </div>
            </div>

            <!-- 결제 날짜 -->
            <div class="date-area">
              {{ formatDate(payment.pay_date) }}
              {{ formatTime(payment.pay_time) }}
            </div>
          </div>
        </div>
      </div>

      <div class="summary">
        <div class="spend">
          <div class="type">쓴 돈</div>
          <div class="today">₩ 4057</div>
          <div class="total">₩ 426864</div>
        </div>
        <div class="remain">
          <div class="type">남은 돈</div>
          <div class="today">₩ 6024</div>
          <div class="total">₩ 426864</div>
        </div>
      </div>

      <div class="calculation">
        <div class="result" @click="toggleCurrencyInResult">
          {{ formattedCheckedCost }}
        </div>
      </div>

      <!-- 정산하기 -->
      <div class="adjustment">
        <div class="adjust-background">
          <button
            class="adjust-btn"
            @mousedown="startDrag"
            @mousemove="onDrag"
            @mouseup="stopDrag"
            @touchstart="startDrag"
            @touchmove="onDrag"
            @touchend="stopDrag"
            ref="adjustmentDiv"
          >
            정 산 하 기
          </button>
          <button class="slide-btn">> > ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useMemberColors } from "@/stores/colorStore";
import { format } from "date-fns";
import {
  exchangeArray,
  convertCurrency,
  formatToTwoDecimal,
  formatWithComma,
  currencyText,
  fetchExchangeRates,
} from "@/stores/currencyStore";
import { useTripStore } from "@/stores/tripStore";
import { usePaymentStore } from "@/stores/paymentStore";

const tripStore = useTripStore();
const paymentStore = usePaymentStore();
const route = useRoute();
const router = useRouter();

const payments = computed(() => paymentStore.payments)
// Props
const props = defineProps({
  selectedDate: Date,
  showAllContainers: Boolean,
  showBudgetAndBookingOnly: Boolean,
  selectedView: String,
});

// Emits
const emit = defineEmits(["updateCheckedCost"]);

const checkData = () => {
  console.log('startDate', paymentsDuringTrip.value)
  console.log("store payments", paymentStore.payments)
  console.log("const payments", payments.value)
  console.log('booking payments', bookingPayments.value)
  console.log('selected payments', selectedPayments.value)
  paymentStore.makeAdjustment(route.params.id ,selectedPayments.value)
}
const tripMembers = computed(() => tripStore.members);

const totalBalance = computed(() => {
  if (!Array.isArray(tripMembers.value)) {
    return 0;
  }
  return tripMembers.value.reduce(
    (total, member) =>
      total + (member.balance ? parseFloat(member.balance) : 0),
    0
  );
});

const membersWithColors = ref([]);
const { memberColors, changeColor, rgbaColor } = useMemberColors(tripMembers);

// `onMounted`에서 `membersWithColors`를 초기화
onMounted(() => {
  membersWithColors.value = tripMembers.value.map((member, index) => ({
    ...member,
    color: memberColors.value[index],
  }));
});

const currencyIndex = ref(0);
const currencies = ref(["KRW"]);

onMounted(() => {
  fetchExchangeRates();
  currencies.value = [
    "KRW",
    ...exchangeArray.value.map((item) => item.currency),
  ];
});

const toggleCurrency = () => {
  currencyIndex.value = (currencyIndex.value + 1) % currencies.value.length;
};

const selectedExchange = computed(() => {
  const selectedCurrency = currencies.value[currencyIndex.value];
  return exchangeArray.value.find((item) => item.currency === selectedCurrency);
});

const getExchangeRate = () => {
  if (currencies.value[currencyIndex.value] === "KRW") {
    return 1;
  } else if (selectedExchange.value && selectedExchange.value.exchangeRate) {
    return parseFloat(selectedExchange.value.exchangeRate.replace(/,/g, ""));
  } else {
    return 1;
  }
};

const formattedTotalBalance = computed(() => {
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    totalBalance.value,
    exchangeRate,
    currencies.value[currencyIndex.value] !== "KRW"
  );
  const currencySymbol =
    currencies.value[currencyIndex.value] === "KRW"
      ? "₩"
      : currencyText[currencies.value[currencyIndex.value]];
  return `${currencySymbol} ${formatWithComma(
    formatToTwoDecimal(convertedValue)
  )}`;
});

const formattedMemberBalance = (balance) => {
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    balance,
    exchangeRate,
    currencies.value[currencyIndex.value] !== "KRW"
  );
  const currencySymbol =
    currencies.value[currencyIndex.value] === "KRW"
      ? "₩"
      : currencyText[currencies.value[currencyIndex.value]];
  return `${currencySymbol} ${formatWithComma(
    formatToTwoDecimal(convertedValue)
  )}`;
};

const startDate = computed(() => new Date(tripStore.startDate));

// 사전 예약 결제 내역을 스토어에서 가져오기
// const bookingPayments = computed(() => {
//   const filteredPayments = paymentStore.payments.filter(
//     (payment) => new Date(payment.pay_date) < startDate
//   );
//   return filteredPayments;
// });

// 여행 중 결제 내역을 스토어에서 가져오기
// const paymentsDuringTrip = computed(() => {
//   const filteredPayments = paymentStore.payments.filter(
//     (payment) => new Date(payment.pay_date) >= startDate
//   );
//   return filteredPayments;
// });

// // 선택된 날짜에 해당하는 지출 내역 필터링
// const filteredPayments = computed(() => {
//   if (props.selectedView === "all") {

//     return paymentsDuringTrip.value; // 모든 결제 내역을 반환
//   } else {
//     return paymentsDuringTrip.value.filter(
//       (payment) =>
//         new Date(payment.pay_date).toDateString() ===
//         props.selectedDate.toDateString()
//     );
//   }
// });


const filteredPayments = computed(() => {
  if (props.selectedView === 'all') {
    return paymentStore.filterPaymentsAfterDate(startDate.value);
  } else {
    return paymentStore.filterPaymentsByDate(props.selectedDate);
  }
});

const bookingPayments = computed(() => {
  return paymentStore.filterPaymentsBeforeDate(startDate.value);
});

const paymentsDuringTrip = computed(() => {
  return paymentStore.filterPaymentsAfterDate(startDate.value);
});

const totalCheckedCost = computed(() => {
  return [...bookingPayments.value, ...paymentsDuringTrip.value]
    .filter((payment) => payment.checked)
    .reduce((sum, payment) => sum + payment.amount, 0);
});

const selectedPayments = computed(() => {
  return [...bookingPayments.value, ...paymentsDuringTrip.value]
  .filter(payment => payment.checked);
});

const toggleCurrencyInResult = () => {
  currencyIndex.value = (currencyIndex.value + 1) % currencies.value.length;
};

const formattedCheckedCost = computed(() => {
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    totalCheckedCost.value,
    exchangeRate,
    currencies.value[currencyIndex.value] !== "KRW"
  );
  const currencySymbol =
    currencies.value[currencyIndex.value] === "KRW"
      ? "₩"
      : currencyText[currencies.value[currencyIndex.value]];
  const formattedCost = `${currencySymbol} ${formatWithComma(
    formatToTwoDecimal(convertedValue)
  )}`;
  return formattedCost;
});

watch(formattedCheckedCost, (newCost) => {
  emit("updateCheckedCost", newCost);
});

const toggleCheck = (index, type) => {
  if (type === "booking") {
    bookingPayments.value[index].checked =
      !bookingPayments.value[index].checked;
  } else if (type === "trip") {
    // filteredPayments 내의 실제 결제 항목에 접근하여 상태를 업데이트합니다.
    const payment = filteredPayments.value[index];
    const actualIndex = paymentsDuringTrip.value.findIndex(
      (p) => p === payment
    );
    paymentsDuringTrip.value[actualIndex].checked =
      !paymentsDuringTrip.value[actualIndex].checked;
  }
};

const formattedTotalCost = (paymentArray) => {
  const totalCost = paymentArray.reduce(
    (sum, payment) => sum + payment.amount,
    0
  );
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    totalCost,
    exchangeRate,
    currencies.value[currencyIndex.value] !== "KRW"
  );
  const currencySymbol =
    currencies.value[currencyIndex.value] === "KRW"
      ? "₩"
      : currencyText[currencies.value[currencyIndex.value]];
  return `${currencySymbol} ${formatWithComma(
    formatToTwoDecimal(convertedValue)
  )}`;
};

const formattedCost = (cost) => {
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    cost,
    exchangeRate,
    currencies.value[currencyIndex.value] !== "KRW"
  );
  const currencySymbol =
    currencies.value[currencyIndex.value] === "KRW"
      ? "₩"
      : currencyText[currencies.value[currencyIndex.value]];
  return `${currencySymbol} ${formatWithComma(
    formatToTwoDecimal(convertedValue)
  )}`;
};

const personStyle = (memberName, reservationMembers, index) => {
  if (reservationMembers.includes(memberName)) {
    return {
      backgroundColor: rgbaColor(memberColors.value[index], 0.7),
      border: "none",
    };
  } else {
    return {
      backgroundColor: "#ffffff",
      color: "#ffffff",
      border: `1px solid ${memberColors.value[index]}`,
    };
  }
};

const personClick = (index, memberName, type) => {
  const paymentList =
    type === "booking" ? bookingPayments.value : filteredPayments.value;
  const payment = paymentList[index];

  if (payment.members.includes(memberName)) {
    payment.members = payment.members.filter((name) => name !== memberName);
  } else {
    payment.members.push(memberName);
  }

  // paymentsDuringTrip의 실제 항목 업데이트
  if (type === "trip") {
    const actualIndex = paymentsDuringTrip.value.findIndex(
      (p) => p === payment
    );
    paymentsDuringTrip.value[actualIndex] = payment;
  }
};

const formatDate = (date) => {
  return format(new Date(date), "M월 d일");
};

const formatTime = (time) => {
  return format(new Date(`1970-01-01T${time}`), "HH:mm");
};

// 정산
const adjustmentDiv = ref(null); // 정산 버튼 참조
const isDragging = ref(false); // 드래그 상태를 관리하는 변수
const startX = ref(0); // 드래그 시작 시 X 좌표 저장
const currentX = ref(0); // 현재 드래그 위치의 X 좌표 저장

const startDrag = (event) => {
  isDragging.value = true;
  startX.value = event.clientX || event.touches[0].clientX;
  currentX.value = startX.value;
};

const onDrag = (event) => {
  if (isDragging.value) {
    const x = event.clientX || event.touches[0].clientX;
    const deltaX = x - startX.value;

    const maxDragDistance =
      adjustmentDiv.value.parentElement.offsetWidth -
      adjustmentDiv.value.offsetWidth;

    if (deltaX > 0 && deltaX <= maxDragDistance) {
      adjustmentDiv.value.style.transform = `translateX(${deltaX}px)`;
      currentX.value = x;
    }
  }
};

const stopDrag = () => {
  if (isDragging.value) {
    isDragging.value = false;

    const dragDistance = currentX.value - startX.value;
    const threshold = adjustmentDiv.value.offsetWidth / 2;

    if (dragDistance > threshold) {
      finishTrip();
    } else {
      adjustmentDiv.value.style.transform = `translateX(0)`;
    }
  }
};

// 체크된 비용 저장
const checkedCost = ref("");

// Detail 컴포넌트에서 업데이트된 비용을 저장하는 함수
const updateCheckedCost = (cost) => {
  checkedCost.value = cost; // Update when Detail.vue emits
};

// 정산 완료 버튼 슬라이딩
const finishTrip = () => {
  adjustmentDiv.value.style.transform = `translateX(100%)`;

  setTimeout(() => {
    router.push({
      name: "tripFinish",
      query: { amount: checkedCost.value }, // Use query instead of params
    });
  }, 300);
};

</script>

<style scoped>
.main-container {
  width: 100%;
  height: 100%;
  height: 95vh;
  overflow-y: auto;
  background-color: #f4f6fa;
  margin: 0px auto;
  padding-bottom: 22%;
  display: flex;
  flex-direction: column;
}

.content-container {
  flex-grow: 1;
}

/* ------------ 준비 | 예산 ------------ */
.budget-container {
  width: 100%;
}

.title {
  font-size: 13px;
  font-weight: bolder;
  padding: 5px 20px;
  color: grey;
}

.budget-content {
  display: flex;
  background-color: #ffffff;
  width: 100%;
  height: 80px;
}

.left-detail {
  width: 20%;
  height: 100%;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.right-detail {
  width: 80%;
  height: 60px;
  margin: 10px auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start;
  overflow-y: auto;
  gap: 2px;
  -webkit-overflow-scrolling: touch;
  margin-right: 5px;
}

.right-detail::-webkit-scrollbar {
  width: 7px;
}
.right-detail::-webkit-scrollbar-thumb {
  background-color: #757575;
  border-radius: 4px;
}

.right-detail::-webkit-scrollbar-track {
  background-color: #f0f0f0;
  border-radius: 4px;
}

/* 멤버 */
.member-info {
  width: calc(50% - 5px);
  height: 30px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 2px 0;
}

.member-symbol {
  border-radius: 50%;
  width: 20px;
  height: 20px;
  margin: 0 15px 0 20px;
  justify-content: center;
  align-items: center;
}

.member-familyname {
  font-size: 0.8rem;
}

.member-balance {
  font-size: 0.9rem;
  color: rgb(78, 160, 120);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ------------ 준비 | 사전 예약 ------------ */
.booking-container {
  width: 100%;
  margin: 30px auto 0px auto;
}

.book-content {
  display: flex;
  flex-direction: column;
  padding: 5px 10px;
  background-color: #ffffff;
}

.payment {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  height: 65px;
  margin: auto;
}

.check-area {
  width: 11%;
}

.category-area {
  width: 11%;
}

.cost-area {
  width: 50%;
}

.person-area {
  width: 16%;
}

.date-area {
  width: 14%;
}

/* 체크 버튼 */
.check-area {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto;
}

/* 카테고리 */
.category-area {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto;
}

/* 결제 금액 및 내역 */
.cost-area {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin: auto;
  padding-left: 20px;
}

.cost {
  font-size: 0.9rem;
  color: rgb(214, 72, 72);
}

.cost-area .name {
  font-size: 0.7rem;
  font-weight: 300;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
/* 정산 대상 */
.person-area {
  height: 80%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-wrap: wrap;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.person-area::-webkit-scrollbar {
  width: 3px;
}
.person-area::-webkit-scrollbar-thumb {
  background-color: #757575;
  border-radius: 4px;
}

.person-area::-webkit-scrollbar-track {
  background-color: #f0f0f0;
  border-radius: 4px;
}

.person-info {
  width: calc(50% - 5px);
  height: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2px 0;
}

.person-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  justify-content: center;
  align-items: center;
}

.person-familyname {
  font-size: 0.8rem;
  color: inherit;
}

/* 결제 날짜 */
.date-area {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: 0.6rem;
  color: grey;
  font-weight: 300;
  height: 100%;
  margin-left: 5px;
  margin-right: -5px;
}

.pay-container {
  width: 100%;
  margin: 30px auto 0px auto;
}

.pay-content {
  display: flex;
  flex-direction: column;
  padding: 5px 10px;
  background-color: #ffffff;
}

/* 요약 */
.summary {
  /* position: fixed;
  bottom: 150px;
  left: 0;
  z-index: 1000; */
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 0 auto;
  /* border: 1px solid black; */
  padding: 40px 0px 0px 0px;
  /* background-color: rgba(255, 255, 255); */
  /* border-top: 2px solid #4b72e1; */
}

/* 쓴 돈 */
.spend {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-right: 1px solid black;
}

/* 남은 돈 */
.remain {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.type {
  color: grey;
  font-size: smaller;
}

/* 정산 금액 */
.calculation {
  position: fixed;
  bottom: 80px;
  left: 0;
  z-index: 1001;
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #ffffff;
  color: #4b72e1;
  padding-top: 14px;
  margin: 0 auto;
  margin-bottom: -5px;
  /* border: 1px solid black; */
  border-radius: 30px 30px 0px 0px;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0px -4px 6px rgba(0, 0, 0, 0.1);
}

.result {
  font-weight: bold;
  font-size: 1.2rem;
}

/* 정산하기 */
.adjustment {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  width: 100%;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  text-align: center;
  padding: 0;
  margin: 0 auto;
  background-color: rgba(255, 255, 255);
  /* border: 1px solid black; */
}

.adjust-background {
  width: 80%;
  height: 60%;
  background-color: lightgrey;
  border-radius: 30px;
  margin: 8px 20px;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.adjust-btn {
  width: 60%;
  height: 100%;
  background-color: #4b72e1;
  border-radius: 30px;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  transition: transform 0.3s ease; /* 슬라이딩 애니메이션 */
  position: relative;
  z-index: 1;
}

.slide-btn {
  width: 40%;
  height: 100%;
  border-radius: 30px;
  color: rgb(78, 78, 78);
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
  position: absolute;
  right: 0;
  z-index: 0;
}
</style>
