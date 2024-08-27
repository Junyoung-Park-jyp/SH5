<template>
  <div class="main-container">
    <div class="title">신한 해외여행보험</div>
    <div class="explanation">원하시는 보장을 알려주세요</div>
    <div class="trip-info">
      <div class="duration">
        <v-icon icon="mdi-calendar-blank" size="small"></v-icon>
        <div class="duration-text">9일</div>
      </div>
      &nbsp;|&nbsp;
      <div class="country">
        <v-icon icon="mdi-map-marker-outline" size="small"></v-icon>
        <div class="country-text">프랑스</div>
      </div>
    </div>
    <div class="image">
      <img src="@/assets/img/insurance_main.png" alt="항목" />
    </div>

    <!-- 예상 보험료 -->
    <div class="bottom">
      <div>보험료</div>
      <div class="amount">
        <div>15,500원</div>
      </div>
    </div>
    <!-- <h1>원하시는 보장을 선택해 주세요.</h1>

    <v-btn-toggle v-model="selectedType" mandatory class="d-flex">
      <v-btn value="추천해주세요" class="toggle-btn"> 추천해주세요 </v-btn>
      <v-btn value="직접할게요" class="toggle-btn"> 직접할게요 </v-btn>
    </v-btn-toggle>

    <v-btn-toggle
      v-model="selectedProduct"
      class="d-flex flex-column align-start"
    >
      <v-btn
        v-for="(product, index) in products[selectedType]"
        :key="index"
        :value="product"
      >
        {{ product }}
      </v-btn>
    </v-btn-toggle>

    <v-btn>
      <v-icon icon="mdi-magnify"></v-icon>
      보장 비교해 보기
    </v-btn>

    <div class="text-decoration-underline">이런 기준으로 추천해 드려요</div> -->
  </div>
</template>

<script setup>
import { ref } from "vue";

// 보장 선택
// const selectedType = ref("추천해주세요");

// 보장에 따른 상품 선택
// const selectedProduct = ref(null);

// 상품 내용
// const products = {
//   추천해주세요: [
//     ["기본형", "최소한의 보장이 필요한 분들", "5,660원"],
//     ["고급형", "많은 보장이 필요한 분들", "12,820원"],
//   ],
//   직접할게요: [
//     ["기본형", "최소한의 보장이 필요한 분들", "5,660원"],
//     ["고급형", "많은 보장이 필요한 분들", "12,820원"],
//   ],
// };
</script>

<style scoped>
.main-container {
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  margin: 0px auto;
  padding: 0px;
  padding-bottom: 150px;
  /* background-color: #f4f6fa; */
}

.title {
  color: #4b72e1;
  font-weight: 500;
  font-size: 0.8rem;
}

.explanation {
  font-size: 1.5rem;
  font-weight: bold;
}

.trip-info {
  display: flex;
  flex-direction: row;
  margin: 10px auto;
  color: #878787;
  gap: 5px;
}

.duration,
.country {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: 0.8rem;
}

.duration-text {
  margin: 0 3px;
}

.country-text {
  margin: 0px;
}

.image {
  width: 100%;
  /* border: 1px solid black; */
}

.image > img {
  width: 100%;
}

.bottom {
  position: fixed;
  bottom: 80px;
  left: 0;
  z-index: 1000;
  padding: 0px;
  width: 100%;
  text-align: center;
  padding: 20px 25px;
  margin: auto;
  background-color: #ffffff;
  /* border: 1px solid black; */
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: start;
  align-content: start;
  text-align: center;

  border-radius: 30px 30px 0px 0px;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0px -4px 6px rgba(0, 0, 0, 0.1);
}

.amount {
  display: flex;
  height: 100%;
  /* margin: 0px 5px; */
  /* border: 1px solid blue; */
}

/* .toggle-btn {
  flex: 1;
}

.product-btn {
  text-align: left;
} */
</style>
