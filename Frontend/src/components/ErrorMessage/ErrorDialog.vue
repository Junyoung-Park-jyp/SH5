<template>
  <v-dialog v-model="errorStore.isError">
    <div class="modal-container">
      <div class="modal-message">
        <span v-html="errorStore.errorMessage"></span>
      </div>
      <div class="modal-btns">
        <button class="modal-btn" @click="closeDialog">확인</button>
      </div>
    </div>
  </v-dialog>
</template>

<script setup>
import { useErrorStore } from '@/stores/errorStore';

const errorStore = useErrorStore();

const closeDialog = () => {
  errorStore.clearError();
};
</script>

<style scoped>
.v-card {
  height: 300px;
}

/* 모달 */
.modal-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  border-radius: 10px;
  margin: 0px auto;
  padding: 0px 30px;
  width: 90%;
  height: 150px;
  color: black;
}

.modal-message {
  text-align: center;
  margin: 10px 0px;
  font-size: large;
}

.modal-btns {
  margin: 10px 5px;
}

.modal-btn {
  background-color: lightgrey;
  text-align: center;
  width: 120px;
  margin: 0px 5px;
  padding: 10px 10px;
  border-radius: 10px;
}

.modal-btn:hover,
.modal-btn:click {
  background-color: grey;
}
</style>
