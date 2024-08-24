<template>
  <div>
    <h1>
      박준영 님은
      <span v-if="country === '대한민국'">{{ city }}</span>
      <span v-else>{{ country }}</span>
      도주 중
    </h1>
    <div>
      <div class="d-flex justify-space-between">
        <h2>날짜</h2>
        <div @click="modifyTrip">수정</div>
      </div>
      <div>
        <p>시작일 | {{ startDate }}</p>
        <p>종료일 | {{ endDate }}</p>
      </div>
    </div>
    <div>
      <h2>멤버</h2>
      <div v-for="member in members" class="d-flex align-center">
        <div class="name-symbol d-flex justify-center align-center">
          <div>{{ member[0].slice(0, 1) }}</div>
        </div>
        <div>{{ member[0] }}</div>
        <div>{{ member[1] }}</div>
      </div>
    </div>
    <v-btn @click="goDetail">지출내역</v-btn>
    <div>
      <h2>환율 계산기</h2>
      <div class="d-flex">
        <v-select
          v-model="currency"
          :items="['USD', 'EUR', 'JPY', 'CNY', 'GBP', 'CHF', 'CAD']"
        ></v-select>
        <v-text-field>1.00</v-text-field>
        <v-icon icon="mdi-currency-usd"></v-icon>
        <v-icon icon="mdi-arrow-left-right"></v-icon>
        <v-text-field>1,475.12</v-text-field>
        <v-icon icon="mdi-currency-usd"></v-icon>
      </div>
      <div>현재 환율은 1$ = 1,000$ 입니다.</div>
    </div>
    <div>
      <h2>여행자 보험</h2>
      <div>
        친구와 함께 가족과 함께<br />
        2인 가입 시 5% 할인<br />
        3인 이상 가입 시 총 10% 할인
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useTripStore } from "@/stores/tripStore";

const router = useRouter();

const country = "대한민국";
const city = "기흥";
const startDate = "2024-08-01";
const endDate = "2024-08-21";
const members = [
  ["최한진", "000-000-000"],
  ["최한진", "000-000-000"],
  ["최한진", "000-000-000"],
  ["최한진", "000-000-000"],
];

const currency = ref("USD");

const modifyTrip = () => {
  return router.push({ name: "createTrip" });
};

const goDetail = () => {
  return router.push({ name: "tripDetail" });
};
</script>

<style scoped>
.name-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}
</style>
