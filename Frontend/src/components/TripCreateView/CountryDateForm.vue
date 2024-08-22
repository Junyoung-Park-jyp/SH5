<template>
  <div class="main-container">
    <!-- 상단 국가 입력창 -->
    <div class="first">
      <v-row>
        <div class="question">어디로 여행을 떠나시나요?</div>
        <v-col cols="12">
          <v-text-field
            v-model="selectedCountry"
            label="국가"
            @input="fetchCities"
            outlined
          ></v-text-field>
          <v-select
            v-model="selectedCity"
            :items="cities"
            label="도시"
            outlined
          ></v-select>
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
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useTripStore } from '@/stores/tripStore';

const userStore = useUserStore();
const tripStore = useTripStore();

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