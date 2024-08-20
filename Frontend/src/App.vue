<template>
  <v-app>
    <v-container>
      <v-switch
        v-model="isTraveling"
        :label="isTraveling ? '홈' : '여행'"
        inset
        color="primary"
      class="btn-switch"
        >
      </v-switch>
    </v-container>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
<script setup>
import { ref } from 'vue';

const isTraveling = ref(false);

</script>
<style>
/* 공통 CSS */
.btn-blue {
  background: #0471E9 !important;
}
.btn-gray {
  background: #979797 !important;
}
.member-blue {
  background: #98D1FB !important;
}
.member-pink {
  background: #FB98F1 !important;
}
.member-green {
  background: #D5FB98 !important;
}
.member-orange {
  background: #FBCC98 !important;
}

.input-bg {
  background: #D9D9D9 !important;
}

.input-font {
  color: #000000 !important;
  opacity: 0.5 !important;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.v-container {
  padding-left: 0px !important;
  padding-right: 0px !important;
}

/* 미디어 쿼리를 이용한 모바일 대응 스타일 */
@media (max-width: 600px) {
  #app {
    font-size: 14px;
  }

  .container {
    padding: 0 8px;
  }
}

@media (min-width: 601px) {
  #app {
    font-size: 16px;
  }

  .container {
    padding: 0 12px;
  }
}

/* navbar css */
.btn-switch {

}
</style>

