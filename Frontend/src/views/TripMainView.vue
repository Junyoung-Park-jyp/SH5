<template>
  <div class="main-container">
    <!-- 프로필 -->
    <div class="my-10 profile">
      <img class="profile-img" src="../assets/img/profile.png" alt="프로필" />
      <span
        >최한진 님은
        <span class="profile-destination">{{ destination }}</span> 여행
        {{ tripState }} 중</span
      >
    </div>

    <!-- 수정 -->
    <div class="modify" @click="modifyTrip">
      <button class="icon-btn">
        <v-icon icon="mdi-pencil" size="large"></v-icon>
        <span>수정</span>
      </button>
    </div>

    <!-- 날짜 -->
    <div class="trip date">
      <div class="d-flex justify-space-between">
        <div class="title">날짜</div>
        <div v-if="tripState === '준비'">
          D-{{ Math.ceil((startDate - today) / (1000 * 60 * 60 * 24)) }}
        </div>
      </div>
      <div class="content">
        <p>시작일 &nbsp; | &nbsp; {{ formatDay(startDate) }}</p>
        <p>종료일 &nbsp; | &nbsp; {{ formatDay(endDate) }}</p>
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
        <div
          class="member-symbol d-flex justify-center align-center"
          :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }"
          @click="changeColor(index)"
        >
          <div class="member-familyname">{{ member[0].slice(0, 1) }}</div>
        </div>
        <div class="member-name">{{ member[0] }}</div>
        <div class="member-account">{{ member[1] }}</div>
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
        <button class="invite-btn">함 께 &nbsp; 가 입 하 기</button>
      </div>
      <div class="content">
        <div class="insurance-explanation">친구와 함께 가족과 함께</div>
        <div class="insurance-benefit">
          2인 가입 시 5% 할인<br />
          3인 이상 가입 시 총 10% 할인
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { format } from "date-fns";
import axios from "axios";

const router = useRouter();

// 여행 목적지
const country = "대한민국";
const city = "부산";

// 대한민국 여행일 경우 목적지는 도시로 설정
const destination = ref(country);
if (country === "대한민국") {
  destination.value = city;
}

// 오늘 날짜
const today = new Date();
today.setHours(0, 0, 0, 0);

// 여행 날짜
const startDate = new Date(2024, 7, 10); // 2024년 8월 10일
const endDate = new Date(2024, 7, 27); // 2024년 8월 27일

// 여행 상태
const tripState = ref("준비");
if (startDate <= today && today <= endDate) {
  tripState.value = "";
}

const formatDay = (date) => {
  return format(date, "yyyy년 MM월 dd일");
};

// 여행 멤버와 계좌번호
const tripMembers = [
  ["박준영", "신한 0276524561730773"],
  ["임광영", "국민 000-000-000"],
  ["정태완", "우리 000-000-000"],
  ["최한진", "계좌 미등록"],
];

// 색상 배열
const colors = [
  "#CA7172",
  "#FBCC98",
  "#D5FB98",
  "#98D1FB",
  "#98B4FB",
  "#B598FB",
  "#FB98F1",
  "#ACACAC",
];

// 멤버별 색상 배열 초기화
const memberColors = ref([]);

// 로컬 스토리지에서 색상 불러오기
const loadColors = () => {
  const storedColors = JSON.parse(localStorage.getItem("memberColors"));
  if (storedColors && storedColors.length === tripMembers.length) {
    memberColors.value = storedColors;
  } else {
    memberColors.value = tripMembers.map(
      (_, index) => colors[index % colors.length]
    );
  }
};

// 로컬 스토리지에 색상 저장
const saveColors = () => {
  localStorage.setItem("memberColors", JSON.stringify(memberColors.value));
};

// 색상을 변경하는 함수
const changeColor = (index) => {
  const currentColor = memberColors.value[index];
  const currentColorIndex = colors.indexOf(currentColor);
  const nextColorIndex = (currentColorIndex + 1) % colors.length;
  memberColors.value[index] = colors[nextColorIndex];
  saveColors(); // 변경된 색상을 저장
};

// Hex 색상을 RGBA로 변환하여 투명도를 조절하는 함수
const rgbaColor = (hex = "#d3d3d3;", alpha = 1) => {
  if (!hex || typeof hex !== "string" || hex.length !== 7) {
    // 기본값 또는 잘못된 hex 값 처리
    hex = "#d3d3d3;"; // 기본값 설정
  }
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

// 페이지 로드 시 색상 로드
onMounted(() => {
  loadColors();
});

// 색상 변경 감지하여 자동 저장
watch(memberColors, saveColors, { deep: true });

// 선택한 통화
const selectCurrency = ref("USD");

// 지원하는 통화 배열
const currencies = ["USD", "EUR", "JPY", "CNY", "GBP", "CHF", "CAD"];

// 환율 GET 요청
const exchangeArray = ref([]);
// onMounted(() => {
//   axios({
//     url: 'http://52.79.246.151:8000/exchange_rate/',
//     method: 'get'
//   })
//     .then(res => {
//       exchangeArray.value = res.data
//       console.log(res)
//     })
//     .catch(err => console.log(err))
// })
exchangeArray.value = [
  {
    id: 5399,
    currency: "CAD",
    exchangeRate: "980.82",
    exchangeMin: "140",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5400,
    currency: "CHF",
    exchangeRate: "1,566.15",
    exchangeMin: "100",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5401,
    currency: "CNY",
    exchangeRate: "186.91",
    exchangeMin: "800",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5402,
    currency: "EUR",
    exchangeRate: "1,486.49",
    exchangeMin: "100",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5403,
    currency: "GBP",
    exchangeRate: "1,744.64",
    exchangeMin: "80",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5404,
    currency: "JPY",
    exchangeRate: "919.63",
    exchangeMin: "100",
    created: "2024-08-22 16:31:47",
  },
  {
    id: 5406,
    currency: "USD",
    exchangeRate: "1,332.4",
    exchangeMin: "100",
    created: "2024-08-22 16:31:47",
  },
];

// 환율 계산
const foreignCurrency = ref(1);
const koreaCurrency = computed(() => {
  const selectedExchange = exchangeArray.value.find(
    (item) => item.currency === selectCurrency.value
  );
  return (
    parseFloat(selectedExchange.exchangeRate.replace(/,/g, "")) *
    foreignCurrency.value
  );
});

// 통화에 따른 버튼 아이콘
const currencyIcons = {
  CAD: "mdi-currency-usd",
  CHF: "mdi-currency-fra",
  CNY: "mdi-currency-cny",
  EUR: "mdi-currency-eur",
  GBP: "mdi-currency-gbp",
  JPY: "mdi-currency-jpy",
  USD: "mdi-currency-usd",
};

// 통화에 따른 텍스트
const currencyText = {
  CAD: "$",
  CHF: "₣",
  CNY: "¥",
  EUR: "€",
  GBP: "£",
  JPY: "¥",
  USD: "$",
};

// 외화 금액 포맷팅을 위한 computed property
const formattedForeignCurrency = computed({
  get() {
    // 세 자리마다 콤마를 추가
    return String(foreignCurrency.value).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  },
  set(value) {
    // 콤마를 제거한 후 저장
    foreignCurrency.value = value.replace(/,/g, "");
  },
});

// 원화 금액 포맷팅을 위한 computed property
const formattedKoreaCurrency = computed({
  get() {
    // 세 자리마다 콤마를 추가
    return String(koreaCurrency.value).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  },
  set(value) {
    // 콤마를 제거한 후 저장
    koreaCurrency.value = value.replace(/,/g, "");
  },
});

// 1 단위의 외국 통화를 한국 원화로 변환하여 보여줄 값
const formattedOneUnitKoreaCurrency = computed(() => {
  const selectedExchange = exchangeArray.value.find(
    (item) => item.currency === selectCurrency.value
  );
  return String(
    parseFloat(selectedExchange.exchangeRate.replace(/,/g, ""))
  ).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
});

const modifyTrip = () => {
  return router.push({ name: "createTrip" });
};

const goDetail = () => {
  return router.push({ name: "tripDetail" });
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
  margin-left: 30px;
  margin-right: 20px;
}

.profile > span {
  font-weight: bold;
  font-size: 1.25rem;
}

.profile-destination {
  font-weight: bolder;
  font-size: x-large;
  padding: 0 4px;
  text-decoration-line: underline;
  text-decoration-style: wavy;
  text-decoration-thickness: 2px;
  text-underline-offset: 4px; /* 글자-밑줄 간격 */
  text-decoration-skip-ink: none;
}

/* 수정 */
.modify {
  display: flex;
  justify-content: right;
  align-items: center;
  margin-top: -70px;
  margin-bottom: -20px;
  padding: 20px;
}

.icon-btn {
  display: flex;
  align-items: end;
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

/* 날짜 */
.date > .content {
  padding-left: 35px;
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
  padding: 20px 0;
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
  width: 5%;
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
  padding-top: 20px;
}

.invite-btn {
  width: 44%;
  background-color: #4b72e1;
  border-radius: 15px;
  color: white;
  margin-top: -5px;
  padding: 8px 12px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 400;
  text-align: center;
}

.insurance-explanation {
  color: grey;
  margin: 10px auto;
}

.insurance-benefit {
  font-size: large;
  font-weight: 500;
}
</style>
