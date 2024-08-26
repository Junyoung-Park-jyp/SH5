<template>
  <div class="main-container">
    <!-- 정산 금액 -->
    <div class="amount">{{ amount }}</div>

    <!-- 입금/출금 -->
    <div class="type">
      <div class="deposit">
        <div class="deposit-img"><img src="@/assets/img/deposit.png" alt="입금"></div>
        입금
      </div>
      <div class="withdraw">
        <div class="withdraw-img"><img src="@/assets/img/withdraw.png" alt="출금"></div>
        출금
      </div>
    </div>

    <!-- 정산완료 -->
    <div class="complete">
      <div class="img"><img src="@/assets/img/check.png" alt="체크"></div>
      <div class="message">정 산 완 료</div>
    </div>

    <!-- 상세내역 -->
    <div class="explanation">
      <table class="settlement-table">
        <thead>
          <tr>
            <th></th>
            <th>지출액</th>
            <th>정산액</th>
            <th>잔액</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(member, index) in members" :key="index">
            <td>
              <div class="member">
                <div :class="`circle circle-${index}`">{{ member.initial }}</div>
              </div>
            </td>
            <td>{{ member.expense }}</td>
            <td :class="{'positive': member.adjustment > 0, 'negative': member.adjustment < 0}">
              {{ member.adjustment > 0 ? '+' : '' }}{{ member.adjustment }}
            </td>
            <td>{{ member.balance }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const amount = route.query.amount;

// Example data (You will replace this with real data)
const members = ref([
  { name: '최', initial: '최', expense: '₩ 426,864', adjustment: 24125, balance: '₩ 1,426,864' },
  { name: '박', initial: '박', expense: '₩ 526,864', adjustment: -174698, balance: '₩ 3,426,864' },
  { name: '임', initial: '임', expense: '₩ 726,864', adjustment: 37243, balance: '₩ 2,426,864' },
  { name: '정', initial: '정', expense: '₩ 326,864', adjustment: 89775, balance: '₩ 4,426,864' },
]);
</script>


<style scoped>
.main-container {
  height: 92vh;
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 0px;
  background-color: #f4f6fa;
}

.amount {
  width: 100%;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: end;
  text-align: center;
  /* border: 1px solid black; */
  color: #4b72e1;
  font-size: xx-large;
  font-weight: bolder;
  margin: 0px auto;
  padding-bottom: 30px;
}

.type {
  background-color: #ffffff;
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  /* border: 1px solid blue; */
  margin: auto;
  font-size: large;
}

.withdraw, .deposit {
  height: 50%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  text-align: center;
  font-weight: bold;
  /* border: 1px solid green; */
}

.withdraw-img, .deposit-img {
  width: 70px;
  margin: auto 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.withdraw-img img, .deposit-img img {
  height: 55px;
  width: 40px;
  /* border: 1px solid black; */
  margin: auto;
}

.complete {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  /* border: 1px solid black; */
  color: #4b72e1;
  margin: 0px auto;
}

.img > img {
  height: 60px;
  width: 60px;
}

.message {
  font-size: 22px;
  font-weight: bolder;
}

.explanation {
  width: 100%;
  height: 60%;
  background-color: #ffffff;
  padding: 20px;
}

.settlement-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 1.2rem;
}

.settlement-table th,
.settlement-table td {
  padding: 10px;
}


.settlement-table .member {
  display: flex;
  align-items: center;
  gap: 10px;
}

.circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: white;
  font-weight: bold;
}

.circle-0 {
  background-color: #a7c7e7;
}

.circle-1 {
  background-color: #e7a7e7;
}

.circle-2 {
  background-color: #a7e7a7;
}

.circle-3 {
  background-color: #e7c7a7;
}

.positive {
  color: #1d72e7;
  font-weight: bold;
}

.negative {
  color: #e71d1d;
  font-weight: bold;
}
</style>