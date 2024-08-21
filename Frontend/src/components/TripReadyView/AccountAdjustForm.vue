<template>
  <v-container>
    
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