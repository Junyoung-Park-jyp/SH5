<template>
  <div class="main-container">
    <!-- 계좌 선택 드롭다운 -->
    <div class="fourth">
      <v-row>
        <div class="question">여행용 출금 계좌 선택하기</div>
        <v-col cols="12">
          <v-select
            v-model="selectedAccount"
            :items="accounts"
            label="계좌 선택"
            item-text="bank" 
            item-value="accountNo"
            outlined
          ></v-select>
        </v-col>
      </v-row>
    </div>

    <!-- 시간 입력 필드 -->
    <div class="fifth">
      <v-row>
        <div class="question">일일 정산 시간 설정하기</div>
        <div class="explanation">지정 시간에 자동으로 PUSH 알림 전송</div>
        <v-col cols="12">
          <v-text-field
            v-model="settlementTime"
            label="정산 시간 선택"
            type="time"
            outlined
          ></v-text-field>
        </v-col>
      </v-row>
    </div>
  </div>
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
.fourth, .fifth {
  margin: 0px 10px;
}

.fourth {
  margin-top: 30px;
  margin-bottom: 70px;
}

.question {
  font-size: x-large;
  font-weight: bold;
  margin-bottom: 5px;
  margin-left: 15px;
  width: 90%;
}

.explanation {
  font-size: small;
  font-weight: light;
  margin-bottom: 10px;
  margin-left: 15px;
  width: 90%;
}
</style>