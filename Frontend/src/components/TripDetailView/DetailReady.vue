<template>
  <div class="main-container">
    <!-- 예산 -->
    <div class="budget-container">
      <div class="title d-flex justify-space-between">
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
          <v-icon icon="mdi-wallet-outline" color="grey" size="30px"></v-icon>
        </div>
        <div class="right-detail">
          <div
            v-for="(member, index) in tripMembers"
            :key="index"
            class="member-info"
          >
            <div
              class="member-symbol d-flex justify-center align-center"
              :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }"
              @click="changeColor(index)"
            >
              <div class="member-familyname">{{ member.name.slice(0, 1) }}</div>
            </div>
            <div class="member-balance" @click="toggleCurrency">
              {{ formattedMemberBalance(member.balance) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 사전 예약 -->
    <div class="booking-container">
      <div class="title d-flex justify-space-between">
        <div class="prepare">준비</div>
        <div class="line">&nbsp;|&nbsp;</div>
        <div class="booking">사전 예약</div>
        <v-spacer></v-spacer>
        <div class="sum" @click="toggleCurrency">
          {{ formattedTotalCost }}
        </div>
      </div>
      <div class="book-content">
        <div
          class="payment"
          v-for="(reservation, index) in reservations"
          :key="index"
        >
          <!-- 체크 버튼 -->
          <div class="check-area">
            <v-btn
              @click="toggleCheck(index)"
              variant="text"
              :color="reservation.checked ? 'primary' : 'grey'"
              :icon="
                reservation.checked
                  ? 'mdi-check-circle'
                  : 'mdi-checkbox-blank-circle-outline'
              "
            ></v-btn>
          </div>

          <!-- 카테고리 -->
          <div class="category-area">
            <v-icon icon="mdi-airplane" color="grey" size="x-large"></v-icon>
          </div>

          <!-- 결제 금액 및 내역 -->
          <div class="cost-area">
            <div class="cost" @click="toggleCurrency">
              {{ formattedCost(reservation.cost) }}
            </div>
            <div class="name">{{ reservation.name }}</div>
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
                :style="personStyle(member.name, reservation.members, index)"
                @click="personClick(member.name)"
              >
                <div class="person-familyname">
                  {{ member.name.slice(0, 1) }}
                </div>
              </div>
            </div>
          </div>

          <!-- 결제 날짜 -->
          <div class="date-area">
            {{ formatDate(reservation.pay_date) }}
            {{ formatTime(reservation.pay_time) }}
          </div>
        </div>
      </div>
    </div>

    <v-container>
      <v-row>
        <v-col cols="6">
          <div>쓴 돈</div>
          <div>₩ 4057</div>
          <div>₩ 426864</div>
        </v-col>
        <v-col cols="6">
          <div>남은 돈</div>
          <div>₩ 6024</div>
          <div>₩ 426864</div>
        </v-col>
      </v-row>
      <v-row> 737353 원 정산하기 </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
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

const tripStore = useTripStore()
// 멤버별 예산 더미 데이터
const tripMembers = [
  { name: "박준영", balance: 3000000 },
  { name: "이선재", balance: 3500000 },
  { name: "임광영", balance: 4000000 },
  { name: "정태완", balance: 4500000 },
  { name: "최한진", balance: 5000000 },
];

// 총 합계 계산
const totalBalance = computed(() => {
  return tripMembers.reduce((total, member) => total + member.balance, 0);
});

// const members = tripStore.members


// 2명씩 그룹으로 묶기
const groupMembers = [];
for (let i = 0; i < tripMembers.length; i += 2) {
  groupMembers.push(tripMembers.slice(i, i + 2));
}

const { memberColors, changeColor, rgbaColor } = useMemberColors(tripMembers);

// 현재 보여줄 통화 인덱스
const currencyIndex = ref(0);

// 모든 지원되는 통화 배열
const currencies = ref(["KRW"]);

// `onMounted`에서 currencies 설정
onMounted(() => {
  fetchExchangeRates(); // 환율 데이터 가져오기
  currencies.value = [
    "KRW",
    ...exchangeArray.value.map((item) => item.currency),
  ];
});

// 통화 전환 함수
const toggleCurrency = () => {
  currencyIndex.value = (currencyIndex.value + 1) % currencies.value.length;
};

// 현재 선택된 통화에 대한 환율 가져오기
const selectedExchange = computed(() => {
  const selectedCurrency = currencies.value[currencyIndex.value];
  return exchangeArray.value.find((item) => item.currency === selectedCurrency);
});

// 환율이 존재하는지 확인하고, 존재하지 않을 경우 기본값을 사용
const getExchangeRate = () => {
  if (currencies.value[currencyIndex.value] === "KRW") {
    return 1; // 한화일 경우 환율 1
  } else if (selectedExchange.value && selectedExchange.value.exchangeRate) {
    return parseFloat(selectedExchange.value.exchangeRate.replace(/,/g, ""));
  } else {
    return 1; // 기본값으로 1을 사용
  }
};

// 총 예산의 변환된 값
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

// 각 멤버의 예산을 변환된 값으로 표시
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

// 사전 예약 더미 데이터
const reservations = ref([
  {
    name: "에어프랑스",
    cost: 1806200,
    members: ["최한진", "박준영"],
    pay_date: "2024-05-10",
    pay_time: "16:21:00",
    checked: false,
  },
  {
    name: "대한한공",
    cost: 2420000,
    members: ["임광영", "정태완"],
    pay_date: "2024-05-17",
    pay_time: "17:24:00",
    checked: false,
  },
  {
    name: "Hotel Le Relais Du Louvre",
    cost: 910000,
    members: ["최한진", "박준영", "임광영", "정태완"],
    pay_date: "2024-06-30",
    pay_time: "09:19:00",
    checked: false,
  },
  {
    name: "Hertz Rental Car",
    cost: 450000,
    members: ["최한진", "박준영", "임광영"],
    pay_date: "2024-07-15",
    pay_time: "22:24:00",
    checked: false,
  },
]);

// 항목 체크 상태 토글
const toggleCheck = (index) => {
  reservations.value[index].checked = !reservations.value[index].checked;
};

// 예약 금액의 합계를 계산하는 computed property
const totalCost = computed(() => {
  return reservations.value.reduce(
    (sum, reservation) => sum + reservation.cost,
    0
  );
});

// 총 예약 금액의 변환된 값
const formattedTotalCost = computed(() => {
  const exchangeRate = getExchangeRate();
  const convertedValue = convertCurrency(
    totalCost.value,
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

// 각 예약의 금액을 변환된 값으로 표시하는 함수
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

// 정산 대상 스타일 적용 함수
const personStyle = (memberName, reservationMembers, index) => {
  // 현재 멤버가 예약 멤버에 포함되어 있는지 확인
  if (reservationMembers.includes(memberName)) {
    // 포함되어 있으면 해당 멤버의 색상을 배경에 적용
    return {
      backgroundColor: rgbaColor(memberColors.value[index], 0.7),
      border: "none",
    };
  } else {
    // 포함되어 있지 않으면 배경을 흰색으로 설정하고 기존 색상으로 테두리 적용
    return {
      backgroundColor: "#ffffff",
      border: `1px solid ${memberColors.value[index]}`,
    };
  }
};

// 정산 대상 선별 클릭 함수
const personClick = (memberName) => {
  reservations.value.forEach((reservation) => {
    if (reservation.members.includes(memberName)) {
      // 이미 포함된 멤버라면 리스트에서 제거
      reservation.members = reservation.members.filter(
        (name) => name !== memberName
      );
    } else {
      // 포함되지 않은 멤버라면 리스트에 추가
      reservation.members.push(memberName);
    }
  });
};
const formatDate = (date) => {
  return format(new Date(date), "M월 d일");
};

const formatTime = (time) => {
  return format(new Date(`1970-01-01T${time}`), "HH:mm");
};
</script>

<style scoped>
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
  /* border: 1px solid blue; */
}

.right-detail {
  width: 80%;
  height: 60px;
  margin: 10px auto;
  display: flex;
  flex-wrap: wrap; /* 여러 줄에 걸쳐 배치되도록 설정 */
  align-items: center;
  justify-content: flex-start; /* 아이템 간의 공간 조절 */
  overflow-y: auto;
  gap: 2px;
  /* border: 1px solid red; */
}

/* 멤버 */
.member-info {
  width: calc(50% - 5px); /* 두 개가 한 줄에 배치되도록 너비 설정 */
  height: 30px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  /* margin: 2px 0; */
  padding: 2px 0;
  /* border: 1px solid green; */
}

.member-symbol {
  border: 1px solid black;
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
  font-size: 1rem;
  color: rgb(78, 160, 120);
}

/* ------------ 준비 | 사전 예약 ------------ */
.booking-container {
  width: 100%;
}

.book-content {
  display: flex;
  flex-direction: column;
  /* border: 1px solid blue; */
}

.payment {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  height: 60px;
  margin: auto;
  /* border: 1px solid green; */
}

.check-area {
  width: 15%;
}

.category-area {
  width: 15%;
}

.cost-area {
  width: 40%;
}

.person-area {
  width: 15%;
}

.date-area {
  width: 15%;
}

/* 체크 버튼 */
.check-area {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto;
  /* border: 1px solid black; */
}

/* 카테고리 */
.category-area {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto;
  /* border: 1px solid black; */
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
  /* border: 1px solid black; */
}

.cost {
  color: rgb(214, 72, 72);
}

.name {
  font-size: 0.7rem;
  font-weight: 300;
}

/* 정산 대상 */
.person-area {
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  overflow-y: auto;
  /* border: 1px solid blue; */
}

.person-info {
  width: calc(50% - 5px);
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* margin: 2px 0; */
  padding: 2px 0;
  /* border: 1px solid red; */
}

.person-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  /* margin: 0 15px 0 20px; */
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
}
</style>
