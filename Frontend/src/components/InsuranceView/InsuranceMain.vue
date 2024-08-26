<template>
  <div>
    <div>원하시는 보장을 선택해 주세요.</div>
    <v-btn>추천해주세요</v-btn>
    <v-btn>직접할게요</v-btn>
    
  </div>
</template>

<script setup>
const products = {
  '추천해주세요': [
    ['기본형', '최소한의 보장이 필요한 분들', '5660원'],
    ['고급형', '많은 보장이 필요한 분들', '12820원'],
  ]
}
</script>

<style scoped>

</style>