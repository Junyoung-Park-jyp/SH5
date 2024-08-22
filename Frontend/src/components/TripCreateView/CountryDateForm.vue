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
            <button @click="addCity" class="mt-1 btn-add">
              + 추가
            </button>
          </div>
      </v-row>
    </div>

    <!-- 하단 날짜 선택 입력창 -->
    <div class="second">
      <v-row>
        <div class="question">언제 여행을 떠나시나요?</div>
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