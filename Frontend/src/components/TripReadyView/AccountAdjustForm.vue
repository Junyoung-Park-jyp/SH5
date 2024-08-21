<template>
  <v-container>
    <v-row>
      <v-col cols="12">
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useBalanceStore } from '@/stores/balanceStore'
import { useTripStore } from '@/stores/tripStore'

const balanceStore = useBalanceStore();
const tripStore = useTripStore();

const accounts = balanceStore.userAccounts
</script>

<style scoped>

</style>