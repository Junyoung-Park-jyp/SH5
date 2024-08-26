<template>
  <div class="main-container">
    <v-card class="py-8 px-10 upper-card">
      <v-card-text class="pt-5 title">SOL로 여행으로</v-card-text>
      <v-card-text class="pt-2 text">여행의 시작부터 끝까지<br>지출 관리와 정산으로 편리하게!</v-card-text>
      <div class="mt-5 btn-container">
        <button class="btn-click" @click="goToTrip">여행 시작</button>
      </div>
    </v-card>
    
    <div class="mt-10 px-7 pb-7">
      <div class="my-5">
        <div class="my-5" style="font-size:large; font-weight:bold;">여행 짐만큼 중요한 혜택 챙기기</div>
        <v-btn-toggle v-model="selectedCardType" mandatory class="toggle">
          <v-btn value="체크카드" :color="selectedCardType === '체크카드' ? '#4b72e1' : 'grey'">
            체크카드
          </v-btn>
          <v-btn value="신용카드" :color="selectedCardType === '신용카드' ? '#4b72e1' : 'grey'">
            신용카드
          </v-btn>
        </v-btn-toggle>
      </div>

      <div class="card">
        <div class="benefit-title">SOL트래블 {{ selectedCardType }} 혜택</div>
        <div class="benefit-list">
          <div class="benefit-item" v-for="(benefit, index) in benefits[selectedCardType]" :key="index">
            <div class="benefit-item-title">
              <span class="benefit-idx">{{ index + 1 }}</span><span v-html="benefit"></span>
            </div>
          </div>
        </div>
        <div class="benefit-btn">
          <v-btn class="benefit-btn-click">혜택 더보기</v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 카드 타입 상태 관리
const selectedCardType = ref('체크카드');
const router = useRouter();

// 카드별 혜택 목록 정의
const benefits = {
  '체크카드': [
    '42종 통화 <span class="text-blue font-weight-bold">100% 환율 우대</span>',
    '해외에서 결제, ATM 이용 시 <span class="text-blue font-weight-bold">수수료 면제</span>',
    '전세계 공항 <span class="text-blue font-weight-bold">라운지 무료 입장</span>(연 2회)',
    '국내 4대 <span class="text-blue font-weight-bold">편의점 5% 캐시백</span>',
  ],
  '신용카드': [
    '42종 통화 <span class="text-blue font-weight-bold">100% 환율 우대</span>',
    '해외에서 결제, ATM 이용 시 <span class="text-blue font-weight-bold">수수료 면제</span>',
    '국내 · 해외 이용 <span class="text-blue font-weight-bold">최대 2%적립</span>',
    '전세계 공항 <span class="text-blue font-weight-bold">라운지 무료 입장</span>(연 3회)',
  ],
};

// 여행 시작 페이지 이동 함수
function goToTrip() {
  router.push({ name: 'home' });
  userStore.signIn({ email: 'email9629@naver.com' })
}

// 테스트용 로그인 코드
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore';
const userStore = useUserStore()

</script>

<style scoped>
.main-container {
  height: 90vh;
}

.upper-card {
  background-color: #5e9bc1;
  height: 300px;
  color: white;
  border-radius: 0px;
  margin: 0px auto;
}

.title {
  font-size: 1.1rem;
  font-weight: 500;
}

.text {
  letter-spacing: 0.5px;
  word-spacing: 2px;
  line-height: 19px;
  font-size: 0.85rem;
}

.btn-container {
  text-align: center;
  margin: 0px auto;
}

.btn-click {
  width: 95%;
  height: 60px;
  margin: 0px auto;
  padding: 5px;
  border-radius: 10px;
  background-color: #ffffff;
  font-family: "Spoqa Han Sans Neo";
  font-size: 1.5rem;
  font-weight: bolder;
  color: #4b72e1;
}

.btn-click:hover {
  background-color: lightgray;
}

.toggle {
  border: 1px solid grey;
  box-sizing: border-box;
}

.toggle-btn {
  font-size: 1.2rem;
}

/* card */
.card {
  border: 1px solid black;
  border-radius: 10px;
  padding: 30px;
  margin-top: 30px;
}

.benefit-title {
  font-weight: bold;
  font-size: 1.5rem;
}

.benefit-list {
  margin: 20px auto;
}

.benefit-item {
  margin: 5px auto;
  padding: 0px;
}

.benefit-item-title {
  font-size: 0.9rem; /* 혜택 목록의 글자 크기를 작게 조정 */
  margin: 0px;
  padding: 5px;
}

.benefit-idx {
  background-color: #d8e2fc;
  color: #4b72e1;
  padding: 3px 6px;
  margin-right: 10px;
}

.benefit-btn {
  margin: 0 auto;
  width: 80%;
  border: 1px solid black;
  box-shadow: none;
  border-radius: 10px;
  background-color: grey;
}

.benefit-btn-click {
  text-align: center;
  margin: 0 auto;
  padding: 0 auto;
  border-radius: 10px;
  width: 100%;
  background-color: #ffffff;
}

</style>
