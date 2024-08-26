<template>
  <div class="main-container">
    <!-- 상단 국가/도시 선택 입력창 -->
    <div class="first">
      <v-row>
        <div class="question">어디로 여행을 떠나시나요?</div>
        <v-col cols="12">
          <!-- 국가 -->
          <v-text-field
            v-model="countryInput"
            label="국가"
            @keyup.enter="addCountry"
            outlined
          ></v-text-field>
          <div class="chip-container">
            <v-chip
              v-for="(country, index) in tripStore.country"
              :key="index"
              color="primary"
              class="ma-1"
              close
              @click:close="removeCountry(index)"
            >
              {{ country }}
            </v-chip>
          </div>

          <!-- 도시 -->
          <v-select
            v-model="cityInput"
            label="도시"
            :items="cities"
            @change="addCity"
            outlined
          ></v-select>
          <div class="chip-container">
            <v-chip
              v-for="(city, index) in tripStore.city"
              :key="index"
              color="primary"
              class="ma-1"
              close
              @click:close="removeCity(index)"
            >
              {{ city }}
            </v-chip>
          </div>
        </v-col>
        <div class="btn-container">
          <button @click="addCity" class="mt-1 btn-add">+ 추가</button>
        </div>
      </v-row>
    </div>

    <!-- 하단 날짜 선택 입력창 -->
    <div class="second">
      <v-row>
        <div class="question">
          언제 여행을 떠나시나요?
          <p class="subtitle">자택 출발/도착 기준</p>
        </div>
        <v-col cols="12">
          <!-- 출발일시 -->
          <v-menu
            v-model="departureMenu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="290px"
            class="calendar"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="departureDateFormatted"
                label="출발일시"
                prepend-icon="mdi-calendar"
                readonly
                @click="departureMenu = true"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="departureDate"
              @update:modelValue="updateDepartureDate"
              locale="ko"
              class="custom-picker"
              :weekday-format="getDay"
              :month-format="getMonth"
              :title-date-format="getMonth"
              :header-date-format="getHeaderTitleMonth"
            ></v-date-picker>
          </v-menu>

          <!-- 도착일시 -->
          <v-menu
            v-model="arrivalMenu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="290px"
            class="calendar"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="arrivalDateFormatted"
                label="도착일시"
                prepend-icon="mdi-calendar"
                readonly
                @click="arrivalMenu = true"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="arrivalDate"
              @update:modelValue="updateArrivalDate"
              locale="ko"
              class="custom-picker"
              :weekday-format="getDay"
              :month-format="getMonth"
              :title-date-format="getMonth"
              :header-date-format="getHeaderTitleMonth"
            ></v-date-picker>
          </v-menu>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6">
          <!-- 시작일 선택 -->
          <v-menu
            v-model="menu1"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="formattedStartDate"
                label="시작일"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="startDate" @input="selectStartDate"></v-date-picker>
          </v-menu>
        </v-col>

        <v-col cols="12" sm="6">
          <!-- 종료일 선택 -->
          <v-menu
            v-model="menu2"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="formattedEndDate"
                label="종료일"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="endDate" @input="selectEndDate"></v-date-picker>
          </v-menu>
        </v-col>
      </v-row>
      <!-- 선택된 날짜를 텍스트로 표시 -->
      <v-row>
        <v-col cols="12">
          <p>선택된 기간: {{ formattedStartDate }} ~ {{ formattedEndDate }}</p>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useTripStore } from "@/stores/tripStore";
import { format } from "date-fns";
import { ko } from "date-fns/locale";

const tripStore = useTripStore();

const countryInput = ref("");
const cityInput = ref("");
const cities = ref([]);

// 출발일시 및 도착일시 관리
const departureDate = ref(null);
const arrivalDate = ref(null);
const departureDateFormatted = ref("");
const arrivalDateFormatted = ref("");
const departureMenu = ref(false);
const arrivalMenu = ref(false);

// 날짜 포맷을 업데이트하는 함수
const updateDepartureDate = (newDate) => {
  departureDate.value = newDate;
  departureDateFormatted.value = format(newDate, "yyyy-MM-dd", { locale: ko });
  tripStore.startDate = newDate;
  departureMenu.value = false;
};

const updateArrivalDate = (newDate) => {
  arrivalDate.value = newDate;
  arrivalDateFormatted.value = format(newDate, "yyyy-MM-dd", { locale: ko });
  tripStore.endDate = newDate;
  arrivalMenu.value = false;
};

// 도시 목록을 가져오기 위한 예제 데이터
const cityData = {
  한국: ["서울", "부산", "인천", "대구"],
  일본: ["도쿄", "오사카", "교토", "삿포로"],
  미국: ["뉴욕", "로스앤젤레스", "시카고", "샌프란시스코"],
};

// 사용자가 국가를 입력하면 해당 국가의 도시 목록을 가져오는 함수
const fetchCities = () => {
  if (cityData[countryInput.value]) {
    cities.value = cityData[countryInput.value];
  } else {
    cities.value = [];
  }
};

// 국가를 배열에 추가하는 함수
const addCountry = () => {
  if (countryInput.value && !tripStore.country.includes(countryInput.value)) {
    tripStore.country.push(countryInput.value);
    countryInput.value = "";
  }
};

// 도시를 배열에 추가하는 함수
const addCity = () => {
  if (cityInput.value && !tripStore.city.includes(cityInput.value)) {
    tripStore.city.push(cityInput.value);
    cityInput.value = "";
  }
};

// 추가된 국가를 제거하는 함수
const removeCountry = (index) => {
  tripStore.country.splice(index, 1);
};

// 추가된 도시를 제거하는 함수
const removeCity = (index) => {
  tripStore.city.splice(index, 1);
};

// 국가가 변경될 때마다 도시 목록을 업데이트
watch(countryInput, fetchCities);

// 날짜 포맷팅 함수
const getDay = (date) => {
  const daysOfWeek = ["일", "월", "화", "수", "목", "금", "토"];
  let i = new Date(date).getDay(date);
  return daysOfWeek[i];
};

const getMonth = (date) => {
  const monthName = [
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
    "11월",
    "12월",
  ];

  let i = new Date(date).getMonth(date);
  return monthName[i];
};

const getHeaderTitleMonth = (date) => {
  const monthName = [
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
    "11월",
    "12월",
  ];
  let i = new Date(date).getMonth(date);
  const year = new Date(date).getFullYear(date);
  const month = monthName[i];
  return "${year}년 ${month}";
};
</script>

<style scoped>
.chip-container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 8px;
}

.first,
.second {
  margin: 0px 10px;
}

.first {
  margin-top: 30px;
  margin-bottom: 70px;
}

.question {
  font-size: x-large;
  font-weight: bold;
  margin-bottom: 10px;
  margin-left: 15px;
  width: 90%;
}

.subtitle {
  font-size: small;
  padding-left: 2px;
}

.calendar {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.btn-container {
  margin: 0px auto;
  width: 100%;
  text-align: center;
}

.btn-add {
  margin: 0px auto;
  width: 80%;
  text-align: center;
  cursor: pointer;
}

/* 날짜 */
/* .custom-picker {
  border-radius: 10px !important;

  .v-btn--active.green {
    background-color: #edffff !important;

    .v-btn__content {
      color: #00b1bb !important;
      font-weight: bold !important;
    }
  }

  .v-picker__title {
    display: none !important;
  }

  .v-date-picker-header {
    padding-top: 10px !important;
  }
}

.v-date-picker-table thead tr th {
  color: #1c1c1c !important;
  font-weight: 400 !important;

  &:nth-child(1) {
    color: #ff7451 !important;
  }

  &:nth-child(7) {
    color: #ff7451 !important;
  }
}

.v-date-picker-table tbody tr td {
  &:nth-child(1) {
    .v-btn--disabled {
      .v-btn__content {
        color: #ffcbbe;
      }
    }

    .v-btn__content {
      color: #ff7451;
    }
  }

  &:nth-child(7) {
    .v-btn--disabled {
      .v-btn__content {
        color: #ffcbbe;
      }
    }

    .v-btn__content {
      color: #ff7451;
    }
  }
} */
</style>
