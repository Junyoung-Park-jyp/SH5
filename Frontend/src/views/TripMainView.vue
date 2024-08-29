<template>
  <div class="main-container">
    <!-- 수정 -->
    <div class="modify" @click="modifyTrip">
      <button class="icon-btn">
        <v-icon icon="mdi-pencil" size="medium"></v-icon>
        <span>수정</span>
      </button>
    </div>

    <!-- 프로필 -->
    <div class="my-10 profile">
      <img class="profile-img" src="../assets/img/profile.png" alt="프로필" />
      <div class="profile-status">
        {{ userStore.name }} 님은<br />
        <span class="profile-destination">{{ destination }}</span>
        <!-- <span class="profile-destination">{{ tripStore.locations[0].country }}</span>-->
        {{ tripState }}
      </div>
    </div>

    <!-- 날짜 -->
    <div class="trip date">
      <div class="title d-flex justify-space-between">
        날짜
        <v-spacer></v-spacer>
        <div class="dday" v-if="tripState === '여행 준비 중'">
          D-{{
            Math.ceil(
              (new Date(tripStore.startDate) - today) / (1000 * 60 * 60 * 24) -
                1
            )
          }}
        </div>
      </div>
      <div class="content">
        <p>시작일 &nbsp; | &nbsp; {{ formatDay(tripStore.startDate) }}</p>
        <p>종료일 &nbsp; | &nbsp; {{ formatDay(tripStore.endDate) }}</p>
      </div>
    </div>

    <!-- 멤버 -->
    <div class="trip member">
      <div class="title">멤버</div>
      <div
        v-for="(member, index) in tripMembers"
        :key="index"
        class="d-flex align-center content"
      >
        <!-- 심볼 -->
        <div
          class="member-symbol d-flex justify-center align-center"
          :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }"
          @click="changeColor(index)"
        >
          <div class="member-familyname">{{ member.member.slice(0, 1) }}</div>
        </div>
        <!-- 이름 -->
        <div class="member-name">{{ member.member }}</div>

        <!-- 은행 -->
        <div class="member-bankname">
          {{ member.bank_name.slice(0, member.bank_name.length - 2) }}
        </div>

        <!-- 계좌 -->
        <div v-if="member.bank_account != ''" class="member-account">
          <div class="member-bankaccount">{{ member.bank_account }}</div>
          <div class="member-bankbalance">
            {{ formatWithComma(member.balance) }} 원
          </div>
        </div>
        <div v-else class="member-account">
          계좌 미등록 - {{ member.budget }}
        </div>
      </div>
    </div>

    <!-- 지출 내역 -->
    <div class="trip money">
      <button class="detail-btn" @click="goDetail">지 출 내 역</button>
    </div>

    <!-- 환율 -->
    <div class="trip exchange">
      <div class="title d-flex justify-space-around">
        환율 계산기
        <v-spacer></v-spacer>
        <v-select
          class="currency"
          v-model="selectCurrency"
          :items="currencies"
          @change="updateCurrencyRate"
        ></v-select>
      </div>
      <div class="content">
        <div class="detail-content d-flex justify-space-around">
          <!-- 외국환 입력 -->
          <v-text-field
            class="foreign"
            v-model="formattedForeignCurrency"
          ></v-text-field>
          <!-- 외국환 기호 -->
          <button class="symbol-box">
            <v-icon
              class="foreign-symbol"
              :icon="currencyIcons[selectCurrency]"
              size="24px"
              color="#4b72e1"
            ></v-icon>
          </button>
          <!-- 화살표 -->
          <v-icon
            class="arrow"
            icon="mdi-arrow-left-right"
            size="xx-large"
          ></v-icon>
          <!-- 한국환 출력 -->
          <v-text-field
            class="korea"
            v-model="formattedKoreaCurrency"
          ></v-text-field>
          <!-- 한국환 기호 -->
          <button class="symbol-box">
            <v-icon
              class="korea-symbol"
              icon="mdi-currency-krw"
              size="20px"
              color="#4b72e1"
            ></v-icon>
          </button>
        </div>
        <div class="explanation">
          현재 환율은 1 {{ currencyText[selectCurrency] }} &nbsp; = &nbsp;
          {{ formattedOneUnitKoreaCurrency }} 원 입니다.
        </div>
      </div>
    </div>

    <!-- 여행자 보험 -->
    <div class="trip insurance">
      <div class="title d-flex justify-space-between">
        여행자 보험
        <button class="invite-btn" @click="goInsurance">
          함 께 &nbsp; 가 입 하 기
        </button>
      </div>
      <div class="discription">
        <div class="text">
          <div class="insurance-explanation">친구와 함께 가족과 함께</div>
          <div class="insurance-benefit">
            2인 가입 시 5% 할인<br />
            3인 이상 가입 시 총 10% 할인
          </div>
        </div>
        <div class="image">
          <img src="@/assets/img/insurance_small.png" alt="보험" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { format } from "date-fns";
import { useMemberColors } from "@/stores/colorStore";
import {
  exchangeArray,
  formatToTwoDecimal,
  formatWithComma,
  convertCurrency,
  currencyIcons,
  currencyText,
  fetchExchangeRates,
} from "@/stores/currencyStore";
import { useTripStore } from "@/stores/tripStore";
import { useUserStore } from "@/stores/userStore";
import { useBalanceStore } from "@/stores/balanceStore";

const router = useRouter();
const tripStore = useTripStore();
const userStore = useUserStore();
const balanceStore = useBalanceStore();

// 여행 목적지
const country = computed(() => tripStore.country.join(""));
const city = computed(() => tripStore.city.join(""));

// 대한민국 여행일 경우 목적지는 도시로 설정
const destination = ref(country.value);
if (country === "대한민국") {
  destination.value = city.value;
}

// 오늘 날짜
const today = new Date();
today.setHours(0, 0, 0, 0);

// 여행 상태
const tripState = ref("");

// 여행 상태를 갱신하는 함수
const updateTripState = () => {
  if (tripStore.startDate && new Date(tripStore.startDate) > today) {
    tripState.value = "여행 준비 중"; // 여행 준비중
  } else if (tripStore.startDate && new Date(tripStore.endDate) >= today) {
    tripState.value = "여행 중"; // 여행 진행중
  } else {
    tripState.value = "여행 종료"; // 종료된 경우 추가
  }
};

const formatDay = (date) => {
  // date가 유효한 경우에만 포맷팅, 그렇지 않으면 빈 문자열 반환
  return date ? format(new Date(date), "yyyy년 MM월 dd일") : "";
};

// 여행 멤버와 계좌번호
// const tripMembers = [
//   { name: "박준영", account: "신한 0276524561730773" },
//   { name: "이선재", account: "신한 000-000-000" },
//   { name: "임광영", account: "국민 000-000-000" },
//   { name: "정태완", account: "우리 000-000-000" },
//   { name: "최한진", account: "계좌 미등록" },
// ];

const tripMembers = computed(() => tripStore.members);

// computed 값은 변경할 수 없으므로, 별도의 ref로 상태 관리
const membersWithColors = ref([]);

const { memberColors, changeColor, rgbaColor } = useMemberColors(tripMembers);

// `onMounted`에서 `membersWithColors`를 초기화
onMounted(() => {
  membersWithColors.value = tripMembers.value.map((member, index) => ({
    ...member,
    color: memberColors.value[index],
  }));
});

// 선택한 통화
const selectCurrency = ref("USD");

// 지원하는 통화 배열
const currencies = ["USD", "EUR", "JPY", "CNY", "GBP", "CHF", "CAD"];

// 환율 계산
const foreignCurrency = ref(1);

const selectedExchange = computed(() => {
  return exchangeArray.value.find(
    (item) => item.currency === selectCurrency.value
  );
});

const koreaCurrency = computed(() => {
  if (!selectedExchange.value) {
    return 0; // selectedExchange가 없을 경우 기본값으로 0 반환
  }
  const exchangeRate = parseFloat(
    selectedExchange.value.exchangeRate.replace(/,/g, "")
  );
  return convertCurrency(foreignCurrency.value, exchangeRate, false);
});

// 외화 금액 포맷팅을 위한 computed property
const formattedForeignCurrency = computed({
  get() {
    return formatWithComma(formatToTwoDecimal(foreignCurrency.value));
  },
  set(value) {
    foreignCurrency.value = parseFloat(value.replace(/,/g, "")) || 0;
  },
});

// 원화 금액 포맷팅을 위한 computed property
const formattedKoreaCurrency = computed(() => {
  return selectedExchange.value
    ? formatWithComma(formatToTwoDecimal(koreaCurrency.value))
    : "N/A"; // selectedExchange가 없을 경우 "N/A" 반환
});

// 1 단위의 외국 통화를 한국 원화로 변환하여 보여줄 값
const formattedOneUnitKoreaCurrency = computed(() => {
  if (!selectedExchange.value) {
    return "N/A"; // selectedExchange가 없을 경우 "N/A" 반환
  }
  const exchangeRate = parseFloat(
    selectedExchange.value.exchangeRate.replace(/,/g, "")
  );
  return formatWithComma(formatToTwoDecimal(exchangeRate));
});

// 선택된 통화에 따른 환율 업데이트 메서드
function updateCurrencyRate() {
  foreignCurrency.value = 1; // 외화를 기본 1로 설정하여 한화 환율을 표시
}

// 환율 데이터 가져오기
// onMounted(() => {
//   fetchExchangeRates();
//   updateCurrencyRate();
// });

onMounted(async () => {
  const tripId = tripStore.tripId;
  if (tripId) {
    const tripData = await tripStore.getTrip(tripId);
    if (tripData) {
      // 데이터 할당
      destination.value = tripData.locations[0].country || "Unknown";
      updateTripState();
      tripStore.startDate = tripData.start_date
        ? new Date(tripData.start_date)
        : null;
      tripStore.endDate = tripData.end_date
        ? new Date(tripData.end_date)
        : null;
    }
  }

  await fetchExchangeRates();
  updateCurrencyRate();
});

const modifyTrip = () => {
  return router.push({ name: "createTrip" });
};

const goDetail = () => {
  return router.push({ name: "tripDetail" });
};

const goInsurance = () => {
  return router.push({ name: "insurance" });
};
</script>

<style scoped>
.main-container {
  height: 92vh;
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 20px;
  background-color: #f4f6fa;
}

/* 수정 */
.modify {
  display: flex;
  justify-content: right;
  align-items: center;
  padding: 10px 10px 20px 20px;
  margin: 0px auto -52px auto;
}

.icon-btn {
  display: flex;
  align-items: center;
}

/* 프로필 */
.profile {
  display: flex;
  justify-content: left; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 100px;
}

.profile-img {
  height: 75px;
  margin-left: 20px;
  margin-right: 25px;
}

.profile-status {
  font-weight: bold;
  font-size: 1.25rem;
}

.profile-destination {
  font-weight: bolder;
  font-size: x-large;
  padding-right: 4px;
  text-decoration-line: underline;
  text-decoration-style: wavy;
  text-decoration-thickness: 2px;
  text-underline-offset: 4px; /* 글자-밑줄 간격 */
  text-decoration-skip-ink: none;
}

/* 구획 나누기 */
.trip {
  margin: 20px auto;
  /* border: 2px solid blue; */
}

.title {
  font-size: x-large;
  font-weight: bolder;
  padding: 5px 20px;
}

.content {
  background-color: #ffffff;
  padding: 10px 20px;
}

.content * {
  font-size: 1rem;
}

.image {
  width: 20%;
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  align-items: end;
  align-content: end;
  text-align: end;
}

.image img {
  width: 100%;
}

/* 날짜 */
.date {
  margin-top: -10px;
}

.date > .content {
  padding-left: 35px;
}

.dday {
  font-size: large;
  margin: auto;
}

/* 멤버 */
.member * {
  margin: 0px auto;
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 35px;
  height: 35px;
}

.member-name {
  width: 50px;
}

.member-account {
  width: 200px;
}

/* 지출내역 */
.money {
  width: 100%;
  text-align: center;
  padding: 10px 0;
  margin: 0 auto;
  padding: 20px 0 50px 0;
}

.detail-btn {
  width: 80%;
  background-color: #4b72e1;
  border-radius: 30px;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: 500;
  text-align: center;
}

/* 환율 */
.exchange > .content {
  margin-top: -20px;
}

.currency {
  margin-top: -10px;
}

.detail-content {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: auto;
}

.detail-content * {
  align-self: center;
  font-size: 0.9rem;
  font-weight: bolder;
}

.currency {
  width: 15%;
}

.symbol-box {
  background-color: #c9c9c9;
  border-radius: 0px 5px 5px 0px;
  width: 40px;
  height: 57px;
  margin-bottom: 6%;
}

.foreign-symbol,
.korea-symbol {
  color: white;
}

.arrow {
  width: 15%;
  margin-bottom: 6%;
}

.explanation {
  display: flex;
  justify-content: center;
  text-align: center;
  margin: 0 auto;
  color: grey;
  font-size: 0.9rem;
}

/* 여행자 보험 */
.insurance {
  padding: 30px 0;
}

.invite-btn {
  width: 150px;
  background-color: #4b72e1;
  border-radius: 15px;
  color: white;
  margin-top: -5px;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
}

.discription {
  display: flex;
  justify-content: space-around;
  align-items: center;
  align-content: center;
  margin-top: 5px;
  background-color: #ffffff;
  padding: 10px 20px;
}

.insurance-explanation {
  color: grey;
  margin: 10px auto;
}

.insurance-benefit {
  font-size: large;
  font-weight: 500;
  margin-bottom: 10px;
}
</style>
