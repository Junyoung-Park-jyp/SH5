<template>
  <div class="main-container">
    <div class="sixth">
      <img :src="imageSource" :class="imageClass" alt="Status Image" />
      <p :class="pClass">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import loadingImage from '@/assets/img/loading.gif';
import successImage from '@/assets/img/check.png';

const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  status: {
    type: String,
    required: true,
  },
});

const imageSource = computed(() => {
  return props.status === 'loading' ? loadingImage : successImage;
});

const imageClass = computed(() => {
  return props.status === 'loading' ? 'loading-image' : 'success-image';
});

const pClass = computed(() => {
  return props.status === 'loading' ? 'loading-p' : 'success-p';
});
</script>

<style scoped>
.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 90vh;
  margin: 0 auto;
  text-align: center;
}

.sixth {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-image {
  width: 300px;
  height: 300px;
  margin: 0 auto;
  /* margin-bottom: 20px; */
}

.success-image {
  width: 150px;
  height: 150px;
  margin: 0 auto;
  margin-top: 120px;
}

.loading-p {
  font-size: x-large;
  font-weight: bold;
  margin-top: 20px; /* loading 상태일 때의 margin 값 */
}

.success-p {
  font-size: x-large;
  font-weight: bold;
  margin-top: 60px; /* success 상태일 때의 margin 값 */
}

</style>
