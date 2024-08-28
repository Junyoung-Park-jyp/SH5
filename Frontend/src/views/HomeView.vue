<template>
  <div class="main-container">
    <div class="menu-container">
      <v-row>
        <v-col cols="12">
          <v-card class="account-card">
              <v-col cols="8" class="text-left p-3">
                <div class="mb-2 account-name">{{ userStore.userName }} 님</div>
                <div class="account-num">
                  <span>{{ userStore.userBank.slice(0, userStore.userBank.length - 2) }}</span>
                  <span class="mx-2">{{ userStore.userAccountNum }}</span>
                </div>
                <div class="account-balance">
                  <span>잔액</span>
                  <span class="mx-2">{{ formatCost(userStore.userBalance) }}</span>
                </div>
              </v-col>
              <v-col cols="4" class="text-right">
                <img
                  src="../assets/img/account.png"
                  alt="account"
                  style="width: 100%"
                />
              </v-col>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-10">
        <v-col cols="4">
          <v-card class="menu-card green-card pa-4" outlined>
            <div class="menu">SOL트래블</div>
            <div class="menu-icon">
              <img src="../assets/img/menu1.png" alt="menu1" />
            </div>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card
            class="menu-card blue-card pa-4"
            outlined
            @click="navigateToBridge"
          >
            <div class="menu">SOL로 여행</div>
            <div class="menu-icon">
              <img src="../assets/img/menu2.png" alt="menu2" />
            </div>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="menu-card white-card pa-4" outlined>
            <div class="menu">환율조회</div>
            <div class="menu-icon">
              <img src="../assets/img/menu3.png" alt="menu3" />
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-2">
        <v-col cols="4">
          <v-card class="menu-card white-card pa-4" outlined>
            <div class="menu">환전</div>
            <div class="menu-icon">
              <img src="../assets/img/menu4.png" alt="menu4" />
            </div>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="menu-card white-card pa-4" outlined>
            <div class="menu">목표환율<br />환전</div>
            <div class="menu-icon">
              <img src="../assets/img/menu5.png" alt="menu5" />
            </div>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="menu-card gray-card pa-4" outlined>
            <div class="plus-icon">
              <img src="../assets/img/menu6.png" alt="menu6" />
            </div>
            <div class="text-center menu">메뉴추가</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- footer -->
    <div class="sticky-container">
      <div class="footer" color="white">
        <v-row
          justify="space-around"
          align="center"
          no-gutters
          class="footer-container"
        >
          <v-col cols="auto" class="text-center">
            <button icon>
              <v-icon color="primary" size="28">mdi-home</v-icon>
            </button>
            <div class="footer-label active">홈</div>
          </v-col>

          <v-col cols="auto" class="text-center">
            <button icon>
              <v-icon color="grey" size="28">mdi-chart-pie</v-icon>
            </button>
            <div class="footer-label">자산관리</div>
          </v-col>

          <v-col cols="auto" class="text-center">
            <button icon>
              <v-icon color="grey" size="28">mdi-shopping</v-icon>
            </button>
            <div class="footer-label">상품</div>
          </v-col>

          <v-col cols="auto" class="text-center">
            <button icon>
              <v-icon color="grey" size="28">mdi-gift</v-icon>
            </button>
            <div class="footer-label">혜택</div>
          </v-col>

          <v-col cols="auto" class="text-center">
            <button icon>
              <v-icon color="grey" size="28">mdi-view-grid</v-icon>
            </button>
            <div class="footer-label">전체메뉴</div>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/userStore";
import { useStateStore } from "@/stores/stateStore";
import "../assets/base.css";

const userStore = useUserStore();

// 라우터 훅 설정
const router = useRouter();
const stateStore = useStateStore();

onMounted(() => {
  userStore.signIn({ email: "email9629@naver.com" });
})

// BridgeView로 라우팅하는 함수
const navigateToBridge = () => {
  stateStore.toggleTrip();
  router.push({ name: "bridge" });
};

// cost 포맷팅
const formatCost = (cost) => {
  return cost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "원";
};
</script>

<style scoped>
.main-container {
  padding-bottom: 20px;
  width: 100%;
  margin: 10px auto 0px auto;
  padding: 0px 15px;
  background-color: #f4f6fa;
  /* border: 1px solid black; */
}

.menu-container,
.sticky-container {
  width: 100%;
  margin: 0px auto;
}

/* 계좌 정보 */
.account-card {
  background-color: #ffffff;
  border-radius: 12px;
  height: 200px;
  width: 100%;
  font-size: large;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
}

.account-name {
  font-size: xx-large;
  font-weight: bolder;
}

.account-num,
.account-balance {
  font-size: medium;
}

.text-left {
  height: 100%;
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  padding-left: 25px;
  /* border: 1px solid blue; */
}

.text-right {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: end;
  margin: auto;
  padding: 0 10px 20px 0;
  /* border: 1px solid black; */
}

.menu-card {
  border-radius: 12px;
  width: 100%;
  aspect-ratio: 1;
  font-size: 0.8rem;
  position: relative;
}

.menu {
  font-weight: 700;
  font-size: 12px;
}

.menu-icon {
  position: absolute;
  bottom: 2px;
  right: 5px;
}

.menu-icon img {
  width: 50px;
}

.plus-icon {
  text-align: center;
}

.plus-icon img {
  width: 50px;
}

.green-card {
  background-color: #5e9bc1;
  color: #ffffff;
  font-weight: lighter;
}

.blue-card {
  background-color: #4b72e1;
  color: #ffffff;
  font-weight: lighter;
}

.white-card {
  background-color: #ffffff;
}

.gray-card {
  background-color: #e3e6eb;
  color: #626569;
}

/* footer */
/* sticky-container에 sticky 속성 추가 */
.sticky-container {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  margin: 0px auto;
  padding: 0px;
  background-color: white; /* 추가: 배경색 지정으로 투명도를 방지 */
  width: 100%;
}

.footer {
  border-top: 1px solid #e0e0e0;
  background-color: #f4f6fa;
  width: auto;
}

.footer-container {
  padding: 10px 0;
  /* width: 100%; */
  margin: 0px auto;
}

.footer-label {
  font-size: 0.75rem;
  color: #9e9e9e;
}

.footer-label.active {
  color: #1976d2;
}

.v-btn {
  padding: 0;
}

/* class 값 */

.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 16px;
}

.mt-2 {
  margin-top: 8px;
}
</style>
