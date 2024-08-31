<template>
  <div v-if="payments" class="main-container">
    <div class="content-container">
      <!-- 예산 -->
      <div
        v-if="showAllContainers || showBudgetAndBookingOnly"
        class="budget-container"
        @click="toggleBudget"
      >
        <div class="title d-flex justify-space-between">
          <div v-if="currentBudgetType === 'initial'" class="prepare">초기</div>
          <div v-else-if="currentBudgetType === 'used'" class="prepare">소비</div>
          <div v-else class="prepare">잔여</div>
          <div class="line">&nbsp;&nbsp;</div>
          <div class="budget">예산</div>
          <v-spacer></v-spacer>
          <!-- <div class="sum" @click="toggleCurrency">
            {{ formattedTotalBalance }}
          </div> -->
          <div v-if="currentBudgetType ==='initial'" class="sum">
            ₩ {{ formatWithComma(totalInitialBudget) }}
          </div>
          <div v-else-if="currentBudgetType === 'used'">
            ₩ {{ formatWithComma(totalUsedBudget) }}
          </div>
          <div v-else class="sum">
            ₩ {{ formatWithComma(totalRemainBudget) }}
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
              <!-- <div class="member-balance" @click="toggleCurrency">
                {{ formattedMemberBalance(member.balance) }}
              </div> -->
              <div class="member-balance" >
                <template v-if="currentBudgetType === 'initial'">
                  ₩ {{ formatWithComma(getMemberBudget(member.member).initial_budget) }}
                </template>
                <template v-else-if="currentBudgetType === 'used'">
                  ₩ {{ formatWithComma(getMemberBudget(member.member).used_budget) }}
                </template>
                <template v-else>
                  ₩ {{ formatWithComma(getMemberBudget(member.member).remain_budget) }}
                </template>
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
            :style="payment.is_completed === 1 ? { 'pointer-events': 'auto' } : {}"
          >
            <!-- 체크 버튼 -->
            <div v-if="accountNum == payment.bank_account" class="check-area">
              <v-btn
                @click="toggleCheck(paymentIndex, 'trip')"
                variant="text"
                :color="payment.is_completed === 1 
                  ? 'grey' 
                  : (payment.checked 
                    ? 'primary' 
                    : 'grey')"
                :icon="payment.is_completed === 1 
                  ? 'mdi-circle' 
                  : (payment.checked 
                    ? 'mdi-check-circle' 
                    : 'mdi-checkbox-blank-circle-outline')"
                density="compact"
              ></v-btn>
            </div>
            
            <div v-else class="check-area">
              <v-btn icon="mdi-close-circle" variant="text" color="grey" disabled></v-btn>
            </div>

            <!-- 카테고리 -->
            <div class="category-area">
              <v-icon class="category-icon" :icon="getCategoryIcon(payment.category)" color="grey" size="large"></v-icon>
              <!-- <div>{{ payment.category }}</div> -->
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
                  @click="personClick(paymentIndex, member.member, 'trip')"
                  >
                  <img class="crown" v-if="member.bank_account === payment.bank_account" src="@/assets/img/crown.png" alt="crown">
                  <div
                    :class="{
                      'person-familyname-crown': member.bank_account === payment.bank_account,
                      'person-familyname': member.bank_account !== payment.bank_account
                    }"
                  >
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
            :class="{ 'completed-payment': payment.is_completed === 1 }"
            @click="(payment.is_completed === 1 || !payment.checked)"
            :style="payment.is_completed === 1 ? { 'pointer-events': 'auto' } : {}"
          >
            <!-- 체크 버튼 -->
            <div v-if="accountNum == payment.bank_account" class="check-area">
              <v-btn
                @click="toggleCheck(paymentIndex, 'trip')"
                variant="text"
                :color="payment.is_completed === 1 
                  ? 'grey' 
                  : (payment.checked 
                    ? 'primary' 
                    : 'grey')"
                :icon="payment.is_completed === 1 
                  ? 'mdi-circle' 
                  : (payment.checked 
                    ? 'mdi-check-circle' 
                    : 'mdi-checkbox-blank-circle-outline')"
                density="compact"
              ></v-btn>
            </div>

            <div v-else class="check-area">
              <v-btn icon="mdi-close-circle" variant="text" color="grey" disabled></v-btn>
            </div>

            <!-- 카테고리 -->
            <div class="category-area">
              <v-icon class="category-icon" :icon="getCategoryIcon(payment.category)" color="grey" size="large"></v-icon>
              <!-- <div>{{ payment.category }}</div> -->
            </div>

            <!-- 결제 금액 및 내역 -->
            <div class="cost-area" @click="openModal(payment)">
              <div class="cost">
                {{ formattedCost(payment.amount) }}
              </div>
              <div class="name">{{ payment.brand_name }}</div>
            </div>

            <!-- 정산 대상 -->
            <div
              class="person-area"
              :class="{'scrollable-person-area': payment.is_completed === 1}"
            >
              <div
                v-for="(member, index) in tripMembers"
                :key="index"
                class="person-info"
              >
              <div
                class="person-symbol d-flex justify-center align-center"
                :style="personStyle(member.member, payment.members, index)"
                @click="payment.is_completed !== 1 && personClick(paymentIndex, member.member, 'trip')"
                >
                  <img class="crown" v-if="member.bank_account === payment.bank_account" src="@/assets/img/crown.png" alt="crown">
                  <div
                    :class="{
                      'person-familyname-crown': member.bank_account === payment.bank_account,
                      'person-familyname': member.bank_account !== payment.bank_account
                    }"
                  >
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

      <v-dialog v-model="dialog" max-width="600px">
        <div class="modal">
          <div class="modal-title">
            결제 상세 정보
          </div>
          
          <div class="modal-content">
            <div class="modal-amount">
              <span class=modal-subtitle>금액</span> {{ selectedPayment.amount }}
            </div>
            <div class="modal-brandname">
              <span class=modal-subtitle>항목</span> {{ selectedPayment.brand_name }}
            </div>
            <div class="modal-member">
              <!-- 정산 대상에 대한 테이블 추가 -->
              <table class="modal-member-table">
                <tr>
                  <th>정산 대상</th>
                  <th>금액</th>
                </tr>
                <tr v-for="(member, index) in selectedPayment.members" :key="index">
                  <td>{{ member.member }}</td>
                  <td>
                    <v-text-field
                      v-model="memberCosts[index]"
                      type="number"
                      min="0"
                      :placeholder="getPlaceholder(selectedPayment.id, member.bank_account, index)"
                      @input="updateRemainingAmount"
                      hide-details
                      dense
                    ></v-text-field>
                  </td>
                </tr>
              </table>
              <p>남은 금액: {{ remainingAmount }}</p>
              <v-btn @click="modifyCost" color="primary">확인</v-btn>
            </div>
          </div>
          <div class="modal-button">
            <button class="modal-btn" text @click=closeModal>닫기</button>
          </div>
        </div>
      </v-dialog>
      <!-- <div class="summary">
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
      </div> -->

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
import { useUserStore } from '@/stores/userStore'

const tripStore = useTripStore();
const paymentStore = usePaymentStore();
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();

const payments = computed(() => paymentStore.payments)
const accountNum = computed(() => userStore.accountNum)
const budgets = computed(() => paymentStore.budgets)
const budgetTypes = ['initial', 'used', 'remain'];
const currentBudgetType = ref('initial'); 
const selectedPayment = ref(null);
const memberCosts = ref([]);
const remainingAmount = ref(0);

const getMemberBudget = (memberName) => {
      return budgets.value[memberName] || { initial_budget: 0, remain_budget: 0, used_budget: 0 };
    };

const toggleBudget = () => {
      const currentIndex = budgetTypes.indexOf(currentBudgetType.value);
      currentBudgetType.value = budgetTypes[(currentIndex + 1) % budgetTypes.length];
    };

const totalInitialBudget = computed(() => {
  return Object.values(budgets.value).reduce((sum, budget) => sum + budget.initial_budget, 0);
});

const totalUsedBudget = computed(() => {
  return Object.values(budgets.value).reduce((sum, budget) => sum + budget.used_budget, 0);
});

const totalRemainBudget = computed(() => {
  return Object.values(budgets.value).reduce((sum, budget) => sum + budget.remain_budget, 0);
});

const dialog = ref(false);

const openModal = (payment) => {
  if(payment.bank_account == userStore.accountNum) {
    selectedPayment.value = payment;
    dialog.value = true;
  }

  };

const modifyCost = () => {
  // 각 멤버의 정산 금액을 selectedPayment에 반영
  selectedPayment.value.members.forEach((member, index) => {
    member.assignedCost = memberCosts.value[index];
  });

  // payment 데이터를 adjustment 형식으로 변환
  const paymentData = {
    payment_id: selectedPayment.value.id, // payment의 id가 payment_id에 해당
    bills: selectedPayment.value.members.map((member) => {
      return {
        cost: member.assignedCost,         // 각 멤버가 부담해야 하는 비용
        bank_account: member.bank_account  // 멤버의 bank_account
      };
    }),
  };

  const tripData = {
    trip_id: route.params.id,
    payments: [paymentData],
  };

  const existingIndex = adjustment.value.findIndex(
    (p) => p.payments.some(payment => payment.payment_id === selectedPayment.value.id)
  );

  if (existingIndex !== -1) {
    // 이미 adjustment에 있는 데이터라면 해당 데이터를 업데이트
    adjustment.value[existingIndex] = tripData;
  } else {
    // 없으면 새로 추가
    adjustment.value.push(tripData);
    selectedPayment.value.checked = true; // 상태를 체크 상태로 변경
  }

  updateRemainingAmount();

  if (remainingAmount.value < 2 && remainingAmount.value >= -2) { // 남은 금액이 0일 때만 모달 닫기
    dialog.value = false;
  } else {
    alert('금액이 일치하지 않습니다. 모든 금액을 분배해주세요.');
  }
};

const updateRemainingAmount = () => {
  const totalAssigned = memberCosts.value.reduce((sum, cost) => sum + parseInt(cost || 0), 0);

  remainingAmount.value = selectedPayment.value.amount - totalAssigned;
  console.log(remainingAmount.value)
};


const closeModal = () => {
  dialog.value = false;
}

const defaultCostPerMember = computed(() => {
  return Math.floor(selectedPayment.value.amount / selectedPayment.value.members.length);
});

const getPlaceholder = (paymentId, bankAccount) => {
  // adjustment에서 payment_id가 일치하는 항목을 찾음
  const adjustmentEntry = adjustment.value.find((entry) =>
    entry.payments.some((payment) => payment.payment_id === paymentId)
  );

  if (adjustmentEntry) {
    // payment_id가 일치하는 payment 데이터를 찾음
    const paymentData = adjustmentEntry.payments.find(
      (payment) => payment.payment_id === paymentId
    );

    // 해당 paymentData에서 bank_account가 일치하는 bill을 찾음
    const bill = paymentData.bills.find(
      (b) => b.bank_account === bankAccount
    );

    if (bill) {
      return bill.cost // 해당 멤버의 cost를 반환
    }
  }

  // adjustment에 해당 데이터가 없을 경우 기본 더치페이 금액 반환
  return defaultCostPerMember.value;
};

watch(dialog, (newVal) => {
  if (newVal) {
    // 각 멤버별 초기 금액 설정
    memberCosts.value = selectedPayment.value.members.map((member, index) => {
      const existingBill = getPlaceholder(selectedPayment.value.id, member.bank_account);
      return parseInt(existingBill) || defaultCostPerMember.value;
    });
    updateRemainingAmount();
  }
});


// 체크 토글 기능 수정
const toggleCheck = (index, type) => {
  if (type === "trip") {
    const payment = filteredPayments.value[index];
    const actualIndex = paymentsDuringTrip.value.findIndex(
      (p) => p === payment
    );
    const paymentToUpdate = paymentsDuringTrip.value[actualIndex];

    const adjustmentIndex = adjustment.value.findIndex(
      (p) => p.payments.some(payment => payment.payment_id === paymentToUpdate.id)
    );

    if (adjustmentIndex !== -1) {
      // adjustment에 이미 존재하는 경우 해당 항목 제거
      adjustment.value.splice(adjustmentIndex, 1);
      paymentToUpdate.checked = false;
    } else {
      // adjustment에 없으면 새로운 항목 추가
      const newPaymentData = {
        payment_id: paymentToUpdate.id, // payment의 id가 payment_id에 해당
        bills: paymentToUpdate.members.map((member) => {
          return {
            cost: member.assignedCost,         // 각 멤버가 부담해야 하는 비용
            bank_account: member.bank_account  // 멤버의 bank_account
          };
        }),
      };

      const newTripData = {
        trip_id: route.params.id,
        payments: [newPaymentData],
      };

      adjustment.value.push(newTripData);
      paymentToUpdate.checked = true;
    }
  }
};





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
  console.log('adjustment', adjustment.value)
}

// 결제 카테고리별 아이콘 설정
const categoryIcons = {
  "항공": "mdi-airplane",
  "숙소": "mdi-bed",
  "식비": "mdi-silverware-fork-knife",
  "카페": "mdi-coffee",
  "교통": "mdi-bus",
  "쇼핑": "mdi-shopping",
  "관광": "mdi-bank",
  "기타": "mdi-dots-horizontal-circle",
};

// 카테고리 아이콘을 반환하는 함수
const getCategoryIcon = (category) => {
  return categoryIcons[category] || "mdi-help-circle-outline"; // 기본값으로 도움말 아이콘 사용
};



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
const addCrownClass = (member, payment) => {
  return member.bank_account === payment.bank_account ? 'crown' : '';
};

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

const adjustment = ref([]);

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
  return [...bookingPayments.value, ...paymentsDuringTrip.value].filter(payment => payment.checked);
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
  const isMemberIncluded = reservationMembers.some(member => member.member === memberName);

  if (isMemberIncluded) {
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

  // 현재 멤버가 payment.members에 있는지 확인
  const memberIndex = payment.members.findIndex(member => member.member === memberName);

  if (memberIndex !== -1) {
    // 이미 멤버가 있는 경우, 제거
    payment.members = payment.members.filter((member) => member.member !== memberName);
  } else {
    // 멤버가 없는 경우, 추가
    payment.members.push({ member: memberName });
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
  console.log(adjustment.value)
  setTimeout(() => {
    paymentStore.makeAdjustment(route.params.id, adjustment.value)
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
  font-size: 0.85rem;
  font-weight: light;
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
  /* border: 1px solid black; */
}

.check-area {
  width: 7%;
}

.category-area {
  width: 12%;
  margin-left: 5px !important;
  /* border: 1px solid black; */
}

.cost-area {
  margin-left: -25px !important;
  width: 50%;
  /* border: 1px solid black; */
}

.person-area {
  width: 16%;
  padding-top: 3px;
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
  font-size: 0.65rem;
  font-weight: 300;
  white-space: nowrap; /* 텍스트를 한 줄로 표시 */
  overflow: hidden; /* 넘치는 텍스트를 숨김 */
  text-overflow: ellipsis; /* 넘치는 텍스트에 '...' 표시 */
  /* text-overflow: clip; */
  max-width: 97%; /* 요소의 최대 너비를 지정 */
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

.scrollable-person-area {
  pointer-events:fill;
  overflow-y: auto;

}

.person-info {
  width: calc(50% - 5px);
  height: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2px 0;
  position: relative;
  /* border: 1px solid black; */
}

.person-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
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
  background-color: #ffffff;
}
.payment {
  padding: 5px 10px;
}
.completed-payment {
  background-color: #d3d3d3; /* Light gray background */
  cursor: not-allowed; /* Show a not-allowed cursor */
}

.payment {
  padding: 5px 10px;
}

.completed-payment {
  background-color: #d3d3d3; /* Light gray background */
  cursor: not-allowed; /* Show a not-allowed cursor */
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

.crown {
  transform: rotate(-35deg);
  z-index: 10;
  width: 20px;
  z-index: 1000;
  padding: 0;
  margin: 0;
  display: flex;
  margin-left: -14px;
  margin-bottom: 17px;
  position: absolute;
}

.person-familyname-crown {
  position: relative;
  z-index: 1;
  font-size: 0.8rem;
}

.modal {
  background-color: #ffffff;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: black;
}

.modal-title {
  width: 80%; 
  height: 50px;
  font-weight: bold;
  font-size: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  border-bottom: 1px dashed grey;
  /* border: 1px solid black; */
}

.modal-content {
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: leftr;
  margin: 0 auto;
  border: 1px solid black;
}

.modal-subtitle {
  font-weight: 600;
}

.modal-button {
  padding: 0px;
  width: 100%;
  text-align: center;
  padding: 20px 0;
  margin: 0 auto;
  background-color: #ffffff;
}

.modal-btn {
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
</style>
