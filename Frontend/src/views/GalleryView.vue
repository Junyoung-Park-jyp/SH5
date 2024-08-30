<template>
  <div class="main-container">
    <!-- 뒤로가기 -->
    <div class="header my-2">
      <div class="back" @click="backStep">
        <button class="icon-btn">
          <v-icon
            class="btns"
            icon="mdi-arrow-left"
            size="large"
          ></v-icon>
        </button>
      </div>
    </div>

    <PreviousTrip />
    <!-- 소비 패턴 분석 들어갈 자리 -->
  </div>
</template>

<script setup>
import PreviousTrip from "@/components/GalleryView/PreviousTrip.vue";
import { useRouter } from "vue-router";
const router = useRouter();

const backStep = () => {
  router.replace({ name: "home"});
};
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

.header {
  position: fixed;
  top: 60px;
  left: 0;
  z-index: 1000;
  width: 100%;
  text-align: center;
  padding: 10px;
  margin: 0 auto;
  background-color: #f4f6fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* border: 1px solid black; */
}
</style>
