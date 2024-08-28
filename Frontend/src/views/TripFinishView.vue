<template>
  <div class="main-container">
    <!-- 정산 금액 -->
    <div class="amount">{{ amount }}</div>

    <!-- 입금/출금 -->
    <div class="type">
      <div class="deposit">
        <div class="deposit-img">
          <img src="@/assets/img/deposit.png" alt="입금" />
        </div>
        <div class="deposit-list">
          <div>박준영님에게 172,860원 출금</div>
          <div>임광영님에게 252,440원 출금</div>
        </div>
      </div>
      <div class="withdraw">
        <div class="withdraw-img">
          <img src="@/assets/img/withdraw.png" alt="출금" />
        </div>
        <div class="withdraw-list">
          <div>이선재님으로부터 375,988원 입금</div>
          <div>최한진님으로부터 82,350원 입금</div>
        </div>
      </div>
    </div>

    <!-- 정산완료 -->
    <div class="complete">
      <div class="img"><img src="@/assets/img/check.png" alt="체크" /></div>
      <div class="message">정 산 완 료</div>
    </div>

    <!-- 상세내역 -->
    <div class="detail">
      <table class="settlement-table">
        <thead>
          <tr>
            <th></th>
            <th style="border: 1px dashed lightgrey;">지출액</th>
            <th style="border: 1px dashed lightgrey;">정산액</th>
            <th style="border: 1px dashed lightgrey;">잔액</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(member, index) in tripMembers" :key="index">
            <td class="member-td">
              <div
              class="member-symbol member d-flex justify-center align-center"
              :style="{
                backgroundColor: rgbaColor(memberColors[index], 0.7),
              }"
              >
                <div class="member-familyname">
                  {{ member.name.slice(0, 1) }}
                </div>
              </div>
            </td>
            <td style="border: 1px dashed lightgrey;">{{ formatWithComma(member.expense) }}</td>
            <td style="border: 1px dashed lightgrey;"
            :class="{
              positive: member.adjustment > 0,
              negative: member.adjustment < 0,
            }"
              >
              {{ member.adjustment > 0 ? "+" : "" }}
              {{ formatWithComma(member.adjustment) }}
            </td>
            <td style="border: 1px dashed lightgrey;">{{ formatWithComma(member.balance) }}</td>
          </tr>
        </tbody>
      </table>
      <div class="explanation">개인별 잔액 = 예산 - 총 지출액</div>
    </div>
  </div>
</template>

<script setup>
import { useMemberColors } from "@/stores/colorStore";
import { formatWithComma } from "@/stores/currencyStore";
import { useRoute } from "vue-router";

const route = useRoute();
const amount = route.query.amount;

const tripMembers = [
  {
    name: "박준영",
    expense: 426864,
    adjustment: 24125,
    balance: 1426864,
  },
  {
    name: "이선재",
    expense: 526864,
    adjustment: -174698,
    balance: 3426864,
  },
  {
    name: "임광영",
    expense: 726864,
    adjustment: 37243,
    balance: 2426864,
  },
  {
    name: "정태완",
    expense: 326864,
    adjustment: 89775,
    balance: 4426864,
  },
  {
    name: "최한진",
    expense: 286864,
    adjustment: 89775,
    balance: 5426864,
  },
];

const { memberColors, rgbaColor } = useMemberColors(tripMembers);
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
  align-items: center;
  text-align: center;
  /* border: 1px solid black; */
  color: #4b72e1;
  font-size: xx-large;
  font-weight: bolder;
  margin: 0px auto;
  /* padding-bottom: 30px; */
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

.withdraw,
.deposit {
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

.withdraw-img,
.deposit-img {
  width: 70px;
  margin: auto 15px auto 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.withdraw-img img,
.deposit-img img {
  height: 55px;
  width: 40px;
  /* border: 1px solid black; */
  margin: auto;
}

.withdraw-list,
.deposit-list {
  text-align: left;
  font-size: 15px;
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

.detail {
  width: 100%;
  height: 70%;
  background-color: #ffffff;
  margin: auto;
  padding: 5px 15px 5px 0px;
}

.settlement-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 1.2rem;
  margin: 30px auto 5px auto;
}

.settlement-table thead tr th {
  font-weight: bold;
}

.settlement-table th,
.settlement-table td {
  padding: 10px;
  /* border: 1px dashed lightgrey; */
}

.settlement-table td {
  font-size: 15px;
}

.settlement-table .member {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: large;
}

.member-td {
  text-align: center;
  display: flex;
  justify-content: center;
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 35px;
  height: 35px;
}

.positive {
  color: #1d72e7;
  font-weight: bold;
}

.negative {
  color: #e71d1d;
  font-weight: bold;
}

.explanation {
  width: 100%;
  margin: 0px auto;
  text-align: right;
  padding-right: 10px;
  font-size: 0.8rem;
}
</style>
