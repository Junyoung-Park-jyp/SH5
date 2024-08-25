<template>
  <div class="main-container">
    <!-- 예산 -->
    <div class="budget-container">
      <div class="title d-flex justify-space-between">
        <div class="prepare">준비</div>
        <div class="line">&nbsp;|&nbsp;</div>
        <div class="budjet">예산</div>
        <v-spacer></v-spacer>
        <div class="sum" @click="toggleCurrency">
          {{ formattedTotalBalance }}
        </div>
      </div>
      <div class="content">
        <div class="left-detail">
          <v-icon icon="mdi-wallet-outline" size="30px"></v-icon>
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
      <div class="d-flex justify-space-between">
        <div>준비 | 사전 예약</div>
        <div>₩ 1,219,064</div>
      </div>
      <div v-for="(reservation, index) in reservations" :key="index">
        <div class="d-flex">
          <!-- 체크 버튼 -->
          <v-btn
            @click="toggleCheck(index)"
            density="compact"
            :icon="
              reservation.checked
                ? 'mdi-check-circle'
                : 'mdi-checkbox-blank-circle-outline'
            "
          ></v-btn>
          <!-- 지출 아이콘 -->
          <v-icon icon="mdi-airplane"></v-icon>
          <!-- 지출 가격과 내역 -->
          <div>
            <div>{{ reservation.cost }}</div>
            <div>{{ reservation.name }}</div>
          </div>
          <!-- 정산 해당 인원 -->
          <v-container>
            <v-row
              v-for="(group, groupIndex) in groupMembers"
              :key="groupIndex"
            >
              <div
                v-for="(member, memberIndex) in group"
                :key="memberIndex"
                class="name-symbol d-flex justify-center align-center"
              >
                {{ member.name.slice(0, 1) }}
              </div>
            </v-row>
          </v-container>
          <!-- 정산 날짜 -->
          <div>
            {{ reservation.date }}
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
import {
  exchangeArray,
  convertCurrency,
  formatToTwoDecimal,
  formatWithComma,
  currencyText,
  fetchExchangeRates,
} from "@/stores/currencyStore";

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
    cost: 1062,
    members: ["최한진", "박준영"],
    date: "5월 10일",
    checked: false,
  },
  {
    name: "대한한공",
    cost: 1420,
    members: ["임광영", "정태완"],
    date: "5월 17일",
    checked: false,
  },
  {
    name: "Hotel Le Relais Du Louvre",
    cost: 201,
    members: ["최한진", "박준영", "임광영", "정태완"],
    date: "6월 30일",
    checked: false,
  },
  {
    name: "Hertz Rental Car",
    cost: 450,
    members: ["최한진", "박준영", "임광영"],
    date: "7월 15일",
    checked: false,
  },
]);

// 체크 상태 토글
const toggleCheck = (index) => {
  reservations.value[index].checked = !reservations.value[index].checked;
};
</script>

<style scoped>
/* 준비 | 예산 */
.budget-container {
  width: 100%;
}

.title {
  font-size: 13px;
  font-weight: bolder;
  padding: 5px 20px;
  color: grey;
}

.content {
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
</style>
