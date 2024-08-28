<template>
  <div class="main-container">
    <!-- 여행 멤버 선택창 -->
    <div class="first">
      <v-row>
        <div class="question">누구와 여행을 떠나시나요?</div>
        <div class="explanation">
          닉네임과 이메일 입력시 자동으로 초대 PUSH 알림 전송
        </div>
        <v-col cols="12">
          <!-- <v-row>
            <v-col v-for="(member, index) in tripStore.tripMembers" :key="index">
              <v-chip>{{ member }}</v-chip>
            </v-col>
          </v-row> -->

          <!-- 닉네임 입력 필드 -->
          <v-text-field
            label="닉네임"
            placeholder="닉네임"
            outlined
            type="text"
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
        <div class="btn-container">
          <button @click="addMember" class="mt-1 btn-add">+ 등록</button>
        </div>
      </v-row>
    </div>

    <!-- 여행 별칭 입력창 -->
    <div class="second">
      <v-row>
        <div class="question">여행 별칭 정하기</div>
        <!-- <div class="explanation"></div> -->
        <v-col cols="12">
          <!-- 여행이름 입력 필드 -->
          <v-text-field
            label="여행 이름"
            placeholder="여행 별칭"
            outlined
            type="text"
            v-model="tripName"
          ></v-text-field>
        </v-col>
        <!-- <div class="btn-container">
          <button @click="addTripName" class="mt-1 btn-add">저장</button>
        </div> -->
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/userStore";
import { useTripStore } from "@/stores/tripStore";

const userStore = useUserStore();
const tripStore = useTripStore();
const userName = ref("");
const email = ref("");
const tripName = ref("");

const addMember = async () => {
  const userData = await userStore.getUser(email.value);

  if (userData) {
    tripStore.members.push(userData);
  } else {
    console.error("멤버 추가 실패");
  }
};

const addTripName = async () => {
  if (tripName.value != "") {
    tripStore.tripName = tripName.value;
    alert("여행 이름이 저장되었습니다.");
    console.log(tripStore.tripName);
  } else {
    alert("여행 이름을 입력해주세요.");
  }
};
</script>

<style scoped>
.first,
.second {
  margin: 0px 10px;
}

.first {
  margin-top: 30px;
  margin-bottom: 70px;
}

.second {
  padding-bottom: 120px;
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
  margin-bottom: 30px;
  margin-left: 15px;
  width: 90%;
}

.btn-container {
  margin: 0px auto;
  width: 100%;
  text-align: center;
}

.btn-add {
  margin: 0px auto;
  width: 80%;
  text-align: center;
  cursor: pointer;
}
</style>
