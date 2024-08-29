<template>
  <div class="main-container">
    <PreviousTrip />
    <!-- 소비 패턴 분석 들어갈 자리 -->
  </div>
</template>

<script setup>
import PreviousTrip from "@/components/GalleryView/PreviousTrip.vue";
</script>

<style scoped>
.main-container {
  width: 100%;
  height: 92vh;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  margin: 0px auto;
  /* padding-bottom: 20px; */
  padding: 0px;
  background-color: #f4f6fa;
  /* border: 1px solid black; */
}
</style>
