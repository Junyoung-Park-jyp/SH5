<template>
  <div class="main-container">
    <!-- 여행 멤버 선택창 -->
    <div class="first">
      <v-row>
        <div class="question">누구와 여행을 떠나시나요?</div>
        <div class="explanation">
          이메일 입력시 자동으로 멤버 초대
        </div>
        <v-col cols="12">
          <!-- <v-row>
            <v-col v-for="(member, index) in tripStore.tripMembers" :key="index">
              <v-chip>{{ member }}</v-chip>
            </v-col>
          </v-row> -->

          <!-- 닉네임 입력 필드 -->
          <!-- <v-text-field
            label="닉네임"
            placeholder="닉네임"
            outlined
            type="text"
            v-model="userName"
          ></v-text-field> -->

          <!-- 이메일 입력 필드 -->
          <v-text-field
            label="이메일"
            placeholder="이메일"
            outlined
            type="email"
            v-model="email"
            @keyup.enter="addMember"
          ></v-text-field>
          <div class="chip-container">
          <!-- <v-col v-for="(member, index) in tripStore.members" :key="index"> -->
            <v-chip
              v-for="(member, index) in tripStore.members"
              :key="index"
              color="primary"
              class="ma-1"
              @click="removeMember(index)"
            >
              {{ member.username }}
            </v-chip>
          <!-- </v-col> -->
          </div>
        </v-col>
        <div class="btn-container">
          <button @click="addMember" class="mt-1 btn-add">+ 등록</button>
        </div>
      </v-row>
      <v-row>
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
            label="여행 별칭"
            placeholder="여행 별칭"
            outlined
            type="text"
            v-model="tripStore.tripName"
          />
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
import { useErrorStore } from "@/stores/errorStore";

const userStore = useUserStore();
const tripStore = useTripStore();
const errorStore = useErrorStore()
const userName = ref("");
const email = ref("");
const tripName = ref("");

const addMember = async () => {
  if (email.value === userStore.userEmail) {
    errorStore.showError("자기 자신을 초대할 수 없습니다")
  } else if (tripStore.members.some(element => element.email === email.value)) {
    errorStore.showError("멤버를 중복으로 추가할 수 없습니다")
  } else {
    const userData = await userStore.getUser(email.value);
    tripStore.members.push(userData);
    email.value = "";
  }
  console.log(tripStore.members)

};

// const addTripName = async () => {
//   if (tripName.value != "") {
//     tripStore.tripName = tripName.value;
//     alert("여행 이름이 저장되었습니다.");
//     console.log(tripStore.tripName);
//   } else {
//     alert("여행 이름을 입력해주세요.");
//   }
// };

const removeMember = (index) => {
  tripStore.members.splice(index, 1);
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

.chip-container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 8px;
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
