<template>
  <v-row>
    <v-col cols="12">
      <h1>어디로 여행을 떠나시나요?</h1>

    </v-col>
  </v-row>

  <!-- 하단 날짜 선택 입력창 -->
  <v-row>
      <v-col cols="12" sm="6">
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
              v-model="startDate"
              label="시작일"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="startDate" @input="menu1 = false"></v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="12" sm="6">
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
              v-model="endDate"
              label="종료일"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="endDate" @input="menu2 = false"></v-date-picker>
        </v-menu>
      </v-col>
    </v-row>
  <div class="main-container">
    <!-- 상단 국가 입력창 -->
    <div class="first">
      <v-row>
        <v-text-field
        v-model="countryInput"
        label="국가를 입력하세요"
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

      <v-select
        v-model="cityInput"
        :items="cities"
        label="도시를 선택하세요"
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
      </v-row>
    </div>

    <!-- 하단 날짜 선택 입력창 -->
    <div class="second">
      <v-row>
        <div class="question">언제 여행을 떠나시나요?</div>
        <!-- <v-col cols="12" sm="6">
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
                v-model="startDate"
                label="시작일"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-input v-model="startDate" @input="menu1 = false"></v-date-input>
          </v-menu>
        </v-col>
        <v-col cols="12" sm="6">
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
                v-model="endDate"
                label="종료일"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-input v-model="endDate" @input="menu2 = false"></v-date-input>
          </v-menu>
        </v-col> -->
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useTripStore } from '@/stores/tripStore';

const tripStore = useTripStore();

const countryInput = ref('');
const cityInput = ref('');
const cities = ref([]);

// 도시 목록을 가져오기 위한 예제 데이터
const cityData = {
  '한국': ['서울', '부산', '인천', '대구'],
  '일본': ['도쿄', '오사카', '교토', '삿포로'],
  '미국': ['뉴욕', '로스앤젤레스', '시카고', '샌프란시스코']
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
    countryInput.value = '';
    console.log("국가 목록:", tripStore.country)
  }
};

// 도시를 배열에 추가하는 함수
const addCity = () => {
  if (cityInput.value && !tripStore.city.includes(cityInput.value)) {
    tripStore.city.push(cityInput.value);
    cityInput.value = '';
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

</script>

<style scoped>
.chip-container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 8px;
}
.first, .second {
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
</style>