<template>
  <div>
    <!-- 예산 -->
    <div>
      <div class="d-flex justify-space-between">
        <div>
          준비 | 예산
        </div>
        <div>
          ₩ 14,751,500
        </div>
      </div>
      <div class="d-flex">
        <v-icon icon="mdi-wallet-outline"></v-icon>
        <v-container>
          <v-row v-for="(group, groupIndex) in groupMembers" :key="groupIndex" class="d-flex justify-space-evenly">
            <div v-for="(member, memberIndex) in group" :key="memberIndex">
              {{ member.name.slice(0, 1) }}
              {{ member.balance }}
            </div>
          </v-row>
        </v-container>
      </div>
    </div>

    <!-- 사전 예약 -->
    <div>
      <div class="d-flex justify-space-between">
        <div>
          준비 | 사전 예약
        </div>
        <div>
          ₩ 1,219,064
        </div>
      </div>
      <div v-for="(reservation, index) in reservations" :key="index" class="d-flex align-center">
        <div>
          <v-btn @click="toggleCheck(index)" density="compact"
            :icon="reservation.checked ? 'mdi-check-circle' : 'mdi-checkbox-blank-circle-outline'"></v-btn>
          {{ reservation.cost }} {{ reservation.name }} {{ reservation.date }}
          <!-- 사람 선택이 4명 이상일 경우도 있는데, 이 부분에 대해서 어떻게 처리해야 할까요? -->
        </div>
      </div>
    </div>

    <v-container>
      <v-row>
        <v-col cols="6">
          <div>쓴 돈</div>
          <div>₩ 4057</div>
          <div>₩ 426864</div>
        </v-col>
        <v-col cols="6">
          <div>남은 돈</div>
          <div>₩ 6024</div>
          <div>₩ 426864</div>
        </v-col>
      </v-row>
      <v-row>
        737353 원 정산하기
      </v-row>
    </v-container>

  </div>
</template>

<script setup>
import { ref } from 'vue'

// 멤버별 예산 더미 데이터
const members = [
  { name: '최한진', balance: 3500 },
  { name: '박준영', balance: 3500 },
  { name: '임광영', balance: 3500 },
  { name: '정태완', balance: 3500 },
]

// 2명씩 그룹으로 묶기
const groupMembers = []
for (let i = 0; i < members.length; i += 2) {
  groupMembers.push(members.slice(i, i + 2));
}

// 사전 예약 더미 데이터
const reservations = ref([
  { name: '에어프랑스', cost: 1062, members: ['최한진', '박준영'], date: '5월 10일', checked: false },
  { name: '대한한공', cost: 1420, members: ['임광영', '정태완'], date: '5월 17일', checked: false },
  { name: 'Hotel Le Relais Du Louvre', cost: 201, members: ['최한진', '박준영', '임광영', '정태완'], date: '6월 30일', checked: false },
  { name: 'Hertz Rental Car', cost: 450, members: ['최한진', '박준영', '임광영'], date: '7월 15일', checked: false },
])

// 체크 상태 토글
const toggleCheck = (index) => {
  reservations.value[index].checked = !reservations.value[index].checked;
}
</script>

<style scoped></style>
