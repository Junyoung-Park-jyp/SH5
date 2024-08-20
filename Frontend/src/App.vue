<template>
  <v-app class="app-gradient">
    <v-container>
      <v-toolbar
        :color="isHomeView ? 'white-3' : 'white-4'"
        class="toolbar-layout"
      >
        <!-- 커스텀 스위치 버튼 -->
        <div class="custom-switch" @click="toggleSwitch">
          <div class="switch-thumb" :class="{ active: !isTraveling }"></div>
          <span class="switch-label" :class="{ active: !isTraveling }" style=" padding-left: 5px;">홈</span>
          <span class="switch-label" :class="{ active: isTraveling }" style=" padding-right: 5px;">여행</span>
        </div>

        <!-- 이 요소가 왼쪽과 오른쪽의 요소들을 양 끝으로 배치 -->
        <v-spacer></v-spacer>

        <!-- 오른쪽 아이콘 그룹 -->
        <div class="icon-group">
          <v-btn icon class="icons">
            <v-icon>mdi-message-text</v-icon>
          </v-btn>
          <v-btn icon class="icons">
            <v-icon>mdi-microphone</v-icon>
          </v-btn>
          <!-- HomeView에서는 멤버 아이콘 -->
          <v-btn v-if="isHomeView" icon class="icons">
            <v-icon>mdi-account-outline</v-icon>
          </v-btn>
          <!-- HomeView 이외는 홈 아이콘 -->
          <v-btn v-if="!isHomeView" icon class="icons">
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </div>
      </v-toolbar>
    </v-container>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import './assets/base.css'

const route = useRoute();
const isTraveling = ref(false);

// HomeView에서는 별도의 스타일 적용
const isHomeView = computed(() => route.name === 'HomeView');

// 토글 스위치 함수
const toggleSwitch = () => {
  isTraveling.value = !isTraveling.value;
};
</script>

<style scoped>
/* v-app의 배경 그라데이션 */
.app-gradient {
  background: linear-gradient(to bottom, #ffffff, #f4f6fa);
  min-height: 100vh; /* 페이지 전체 높이를 채우기 위해 */
  display: flex;
  flex-direction: column;
  margin: 0px;
  padding: 0px;
}

.v-container {
  padding: 0px;
}

/* 툴바 레이아웃 조정 */
.toolbar-layout {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 0px;
  margin: 0px;
  font-size: 1.1rem;
}

/* 커스텀 스위치 스타일 */
.custom-switch {
  display: flex;
  align-items: center;
  width: 110px;
  height: 50px;
  background-color: rgb(222, 222, 222);
  border-radius: 25px;
  position: relative;
  cursor: pointer;
  padding: 0px;
  margin: 0px;
}

.switch-thumb {
  width: 45%;
  height: 80%;
  background-color: #4b72e1;
  border-radius: 25px;
  position: absolute;
  margin: auto 5px;
  transition: transform 0.3s ease;
}

.switch-thumb.active {
  transform: translateX(100%);
}

.switch-label {
  flex: 1;
  text-align: center;
  color: white;
  font-weight: bold;
  z-index: 1;
  transition: color 0.3s ease;
}

.switch-label.active {
  color: black;
}

/* 아이콘 그룹 스타일 */
.icon-group {
  display: flex;
  gap: 7px; /* 아이콘 간의 간격 */
}

.icon-group .icons {
  width: 30px;
  height: 30px;
}

/* navbar css */
.btn-switch {

}
</style>
