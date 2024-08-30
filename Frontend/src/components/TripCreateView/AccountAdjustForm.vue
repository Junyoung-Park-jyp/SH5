<template>
  <div v-if="isLoading" class="loading">
    <v-progress-circular indeterminate :size="79" :width="10" color="#4b72e1"></v-progress-circular>
  </div>
  <div v-else class="main-container">
    <!-- 계좌 선택 드롭다운 -->
    <div class="fourth">
      <v-row>
        <div class="question">여행용 출금 계좌 선택하기</div>
        <v-col cols="12">
          <v-select v-model="selectedAccount" :items="formattedAccounts" item-title="title" item-value="value"
            label="계좌를 선택하세요">
          </v-select>
          <!-- <div v-for="(account, index) in accounts" :key="index">
            <p>{{ account.bankName }} - {{ account.accountNo }} - {{ account.accountBalance }}</p>
          </div> -->
        </v-col>
      </v-row>
    </div>

    <!-- 시간 입력 필드 -->
    <div class="fifth">
      <v-row>
        <div class="question">일일 정산 시간 설정하기</div>
        <div class="explanation">지정 시간에 자동으로 PUSH 알림 전송</div>
        <v-col cols="12">
          <v-text-field v-model="settlementTime" label="정산 시간 선택" type="time" outlined></v-text-field>
        </v-col>
      </v-row>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useBalanceStore } from "@/stores/balanceStore";
import { useTripStore } from "@/stores/tripStore";
import { useUserStore } from "@/stores/userStore";

const balanceStore = useBalanceStore();
const tripStore = useTripStore();
const userStore = useUserStore();

const accounts = computed(() => balanceStore.accounts || []);
const selectedAccount = ref(null);
const settlementTime = ref('22:00');
const isLoading = ref(true);  // 로딩 상태 추가

onMounted(async () => {
  try {
    await balanceStore.getAccounts(userStore.email);
    // console.log(accounts.value)
    // balanceStore.bank = accounts.value[0].bankName
    // balanceStore.accountNum = accounts.value[0].accountNo
    // balanceStore.balance = accounts.value[0].accountBalance
    // console.log(balanceStore.bank, balanceStore.accountNum, balanceStore.balance)
    isLoading.value = false;  // 로딩 완료 후 false로 변경
  } catch (error) {
    console.error("Failed to load accounts:", error);
    isLoading.value = false;  // 에러 발생 시에도 로딩 상태 false로 변경
  }
});

// 은행명과 계좌 형식
const formattedAccounts = computed(() =>
  accounts.value.map(account => ({
    title: `${account.bankName.slice(0, account.bankName.length - 2)} ${account.accountNo}`,
    value: account
  }))
);

// selectedAccount 값 변경 시 balanceStore 값 업데이트
watch(selectedAccount, (newValue) => {
  if (newValue) {
    balanceStore.bank = selectedAccount.value.bankName
    balanceStore.accountNum = selectedAccount.value.accountNo
    balanceStore.balance = selectedAccount.value.accountBalance
    console.log(balanceStore.bank, balanceStore.accountNum, balanceStore.balance)
  }
})
</script>

<style scoped>
.fourth,
.fifth {
  margin: 0px 10px;
}

.fifth {
  padding-bottom: 120px;
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

/* 로딩 화면 */
.loading {
  text-align: center;
  margin-top: 150px;
}
</style>
