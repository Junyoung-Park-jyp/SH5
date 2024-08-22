<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <!-- 계좌 선택 드롭다운 -->
        <h1>여행용 출금 계좌 선택하기</h1>
        <v-select
          v-model="selectedAccount"
          :items="accounts"
          label="계좌 선택"
          item-text="bank" 
          item-value="accountNo"
          outlined
        ></v-select>

        <!-- 시간 입력 필드 -->
        <h1>일일 정산 시간 설정하기</h1>
        <v-text-field
          v-model="settlementTime"
          label="정산 시간 선택"
          type="time"
          outlined
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useBalanceStore } from '@/stores/balanceStore';
import { useTripStore } from '@/stores/tripStore';

const balanceStore = useBalanceStore();
const tripStore = useTripStore();

const selectedAccount = ref(null);

const settlementTime = ref(null);

const accounts = balanceStore.userAccounts;
</script>

<style scoped>

</style>