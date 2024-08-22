<template>
  <v-app>
    <div class="main-container">
      <v-toolbar class="px-5 py-1">
        <!-- 커스텀 스위치 버튼 -->
        <div class="custom-switch d-flex align-center rounded-xl" @click="toggleSwitch">
          <div :class="{ active: !isTraveling, 'home-mode': !isTraveling }" class="px-4" style="z-index: 1; font-weight: 500;">홈</div>
          <div :class="{ active: isTraveling, 'travel-mode': isTraveling }" class="px-4" style="z-index: 1; font-weight: 500;">여행</div>
          <div class="switch-thumb rounded-xl" :class="{ active: isTraveling }"></div>
        </div>

        <v-spacer></v-spacer>

        <!-- 오른쪽 아이콘 그룹 -->
        <div class="icon-group">
          <button class="icon-btn">
            <v-icon icon="mdi-message-processing-outline" size="xx-large"></v-icon>
          </button>
          <button class="icon-btn">
            <v-icon icon="mdi-microphone-outline" size="xx-large"></v-icon>
          </button>
          <!-- HomeView에서는 멤버 아이콘 -->
          <button v-if="!isTraveling" class="icon-btn">
            <v-icon icon="mdi-account-outline" size="xx-large"></v-icon>
          </button>
          <!-- HomeView 이외는 홈 아이콘 -->
          <button v-if="isTraveling" class="icon-btn">
            <v-icon icon="mdi-home-outline" size="xx-large"></v-icon>
          </button>
        </div>
      </v-toolbar>
      <HomeView v-if="!isTraveling" />
      <router-view v-else />
    </div>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useStateStore } from '@/stores/stateStore';
import { useUserStore } from './stores/userStore';
import HomeView from './views/HomeView.vue';
import './assets/base.css';

const stateStore = useStateStore();
const userStore = useUserStore();
const route = useRoute();
const isTraveling = computed(() => stateStore.travel)
// 토글 스위치 함수
const toggleSwitch = () => {
  console.log(isTraveling.value, stateStore.isTraveling)
  stateStore.toggleTrip()
};

// onMounted(
//   userStore.signIn({
//     email: '94oldman@gmail.com'
//   })
// )
</script>

<style scoped>
.main-container {
  padding-bottom: 100px;
}

/* 상단 툴바 */
.v-toolbar {
  position: sticky;
  top: 0;
  z-index: 1;

  background-color: white;
  font-size: 1.1rem;
}

.custom-switch {
  position: relative;
  height: 50px;
  background-color: rgb(222, 222, 222);
  cursor: pointer;
}

.switch-thumb {
  width: 45%;
  height: 90%;
  background-color: #4b72e1;
  position: absolute;
  transition: transform 0.3s ease;
}

.switch-thumb.active {
  transform: translateX(46px);
  width: 60%;
}

/* 아이콘 그룹 스타일 */
.icon-group {
  display: flex;
  gap: 0px; 
}

.icon-btn {
  margin: 0px;
  padding: 3px;
}

.icon-btn:hover {
  background-color: lightgray;
}

.home-mode,
.travel-mode {
  color: white;
}

</style>
