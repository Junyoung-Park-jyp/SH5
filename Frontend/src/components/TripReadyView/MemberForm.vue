<template>
  <v-container>
<!-- 여행 멤버 선택창 -->
<v-row>
      <v-col cols="12">
        <h1>누구와 여행을 떠나시나요?</h1>
        <p>닉네임과 이메일 입력시 자동으로 PUSH알림 일일 전송</p>
        <v-row>
          <v-col v-for="(member, index) in tripStore.tripMembers" :key="index">
            <v-chip>{{ member }}</v-chip>
          </v-col>
        </v-row>
         <!-- 사용자명 입력 필드 -->
         <v-text-field
          label="사용자명"
          placeholder="닉네임"
          outlined
          v-model="userName"
        ></v-text-field>
        
        <!-- 이메일 입력 필드 -->
        <v-text-field
          label="이메일"
          placeholder="이메일"
          outlined
          type="email"
          v-model="email"
        ></v-text-field>
      </v-col>
      <v-btn @click="addMember">+ 멤버 추가</v-btn>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useTripStore } from '@/stores/tripStore';

const userStore = useUserStore();
const tripStore = useTripStore();

const userName = ref('')
const email = ref('')

const addMember = async() => {
  const userData = await userStore.getUser(userName.value, email.value)

  if (userData) {
    tripStore.members.push(userData)
  } else {
    console.error('멤버 추가 실패')
  }
}
</script>

<style scoped>

</style>