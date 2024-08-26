<template>
  <div>
    <h1>원하시는 보장을 선택해 주세요.</h1>

    <!-- 보장 토글 버튼 -->
    <v-btn-toggle v-model="selectedType" mandatory class="d-flex">
      <v-btn value="추천해주세요" class="toggle-btn">
        추천해주세요
      </v-btn>
      <v-btn value="직접할게요" class="toggle-btn">
        직접할게요
      </v-btn>
    </v-btn-toggle>

    <!-- 보장에 따른 상품 목록 -->
    <v-btn-toggle v-model="selectedProduct" class="d-flex flex-column align-start">
      <v-btn v-for="(product, index) in products[selectedType]" :key="index" :value="product">
        {{ product }}
      </v-btn>
    </v-btn-toggle>

    <v-btn>
      <v-icon icon="mdi-magnify"></v-icon>
      보장 비교해 보기
    </v-btn>

    <div class="text-decoration-underline">이런 기준으로 추천해 드려요</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 보장 선택
const selectedType = ref('추천해주세요');

// 보장에 따른 상품 선택
const selectedProduct = ref(null);

// 상품 내용
const products = {
  '추천해주세요': [
    ['기본형', '최소한의 보장이 필요한 분들', '5,660원'],
    ['고급형', '많은 보장이 필요한 분들', '12,820원'],
  ],
  '직접할게요': [
    ['기본형', '최소한의 보장이 필요한 분들', '5,660원'],
    ['고급형', '많은 보장이 필요한 분들', '12,820원'],
  ]
};
</script>

<style scoped>
.toggle-btn {
  flex: 1;
}

.product-btn {
  text-align: left;
}
</style>
