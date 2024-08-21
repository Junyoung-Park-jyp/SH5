<template>
  <v-container>
    <!-- 상단 국가 입력창 -->
    <v-row>
      <v-col cols="12">
        <h1>어디로 여행을 떠나시나요?</h1>
        <v-text-field
          v-model="selectedCountry"
          label="국가를 입력하세요"
          @input="fetchCities"
          outlined
        ></v-text-field>
        <v-select
          v-model="selectedCity"
          :items="cities"
          label="도시를 선택하세요"
          outlined
        ></v-select>
        <v-btn @click="addCity" color="primary" class="mt-2">
          도시 추가
        </v-btn>
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
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const selectedCountry = ref('');
const selectedCity = ref([]);
const cities = ref([]);
const selectedCities = ref([]);

const startDate = ref('');
const endDate = ref('');
const menu1 = ref(false);
const menu2 = ref(false);

const cityData = {
  '한국': ['서울', '부산', '인천', '대구'],
  '일본': ['도쿄', '오사카', '교토', '삿포로'],
  '미국': ['뉴욕', '로스앤젤레스', '시카고', '샌프란시스코']
};

const fetchCities = () => {
  if (cityData[selectedCountry.value]) {
    cities.value = cityData[selectedCountry.value];
  } else {
    cities.value = [];
  }
};

const addCity = () => {
  if (selectedCity.value && !selectedCities.value.includes(selectedCity.value)) {
    selectedCities.value.push(selectedCity.value);
  }
};

const removeCity = (index) => {
  selectedCities.value.splice(index, 1);
};
</script>

<style scoped>
.v-chip {
  margin-top: 10px;
}
</style>