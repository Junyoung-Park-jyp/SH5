<template>
  <v-dialog v-model="errorStore.isError" width="auto">
    <v-card>
      <v-card-text>{{ errorStore.errorMessage }}</v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="closeDialog">OK</v-btn>
      </v-card-actions>
    </v-card>
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
  width: 300px;
  height: 300px;
}
</style>
