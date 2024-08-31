<template>
  <div v-if="!loading" class="main-container">
    <!-- 국가 -->
    <div class="my-10 trip country">
      <div class="background" :style="{ backgroundImage: `url('${tripStore.imageUrl}')` }"></div>
      <div v-if="showReferenceMessage" class="reference-message" @click="scrollToTarget">
        AI 여행 스케치 생성하기
        <v-icon icon="mdi-arrow-down-thick" size="16px"></v-icon>
      </div>
      <span class="text mx-2" v-for="(location, index) in locations" :key="index">
        {{ location.country }}
      </span>
    </div>

    <!-- <div class="profile-destination">
          <span
            class="profile-country"
            v-for="(location, index) in tripStore.locations"
            :key="index"
          >
            {{ location.country }}
          </span>
        </div> -->

    <!-- 날짜 -->
    <div class="trip date">
      <div class="title d-flex justify-space-between">
        날짜<v-spacer></v-spacer>
        <div class="subtitle">{{ duration }}</div>
      </div>
      <div class="content">
        <p>시작일 &nbsp; | &nbsp; {{ formatDay(startDate) }}</p>
        <p>종료일 &nbsp; | &nbsp; {{ formatDay(endDate) }}</p>
      </div>
    </div>

    <!-- 멤버 -->
    <div class="trip member">
      <div class="title">
        멤버<v-spacer></v-spacer>
        <div class="subtitle">{{ tripMembers.length }}명</div>
      </div>
      <div class="background-member content">
        <div v-for="(member, index) in tripMembers" :key="index" class="member-list" :style="{
          backgroundImage: `url(${getImagePath(index)})`,
          paddingRight: calculatePadding(index),
        }">
          <div class="member-symbol d-flex justify-center align-center"
            :style="{ backgroundColor: rgbaColor(memberColors[index], 0.7) }">
            <div class="member-familyname">{{ member.member.slice(0, 3) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 지출 내역 -->
    <div class="paymentTrip">
      <div class="title">나의 지출</div>
      <div class="content">
        <PieChart @updateMostCharacter="handleMostCharacterUpdate" />
      </div>
    </div>

    <!-- 소BTI -->
    <div class="trip mbti">
      <div class="title">여행 소BTI</div>
      <div class="content">
        <!-- 아이콘 -->
        <div class="info">
          <v-icon @click="showExplanation = true" class="info-icon" icon="mdi-information" size="22px"
            color="gray"></v-icon>
        </div>
        <!-- 캐릭터 -->
        <div class="mb-5 d-flex justify-space-evenly" style="background-color: white;">
          <v-img class="category-image" :src="receivedCharacter"></v-img>
          <div class="d-flex flex-column justify-center mbti-info">
            <div>당신의 소BTI 캐릭터는</div>
            <div style="font-size: 1.5rem; font-weight: bolder;">{{ receivedCharacterName }}</div>
            <div>
              <v-chip class="ma-2" color="primary" size="xx-small">#항공마일리지왕</v-chip>
              <v-chip class="ma-2" color="primary" size="xx-small">#하늘길애호가</v-chip>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <v-dialog v-model="showExplanation" max-width="500px" max-height="70vh" class="explanation">
      <Mbti />
    </v-dialog>

    <!-- 여행 스케치 -->
    <div class="trip sketch" ref="sketchSection">
      <div class="title">여행 스케치</div>
      <div class="content">
        <DrawPicture />
      </div>
    </div>
  </div>
  <div v-else class="loading">
    <v-progress-circular indeterminate :size="79" :width="10" color="#4b72e1"></v-progress-circular>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from "vue";
import { useTripStore } from "@/stores/tripStore";
import { usePaymentStore } from "@/stores/paymentStore";
import { useRoute } from "vue-router";
import { format } from "date-fns";
import { useMemberColors } from "@/stores/colorStore";

import DrawPicture from "./DrawPicture.vue";
import PieChart from "./PieChart.vue";
import Mbti from './MBTI.vue';

const route = useRoute();
const tripStore = useTripStore();
const paymentStore = usePaymentStore();
const showExplanation = ref(false); // 다이얼로그 열고 닫는 상태 관리

const tripId = route.params.id;

const loading = ref(true);

const locations = computed(() => tripStore.locations);

const startDate = computed(() => new Date(tripStore.startDate));
const endDate = computed(() => new Date(tripStore.endDate));

const durationInDays = computed(() => {
  const start = startDate.value;
  const end = endDate.value;

  if (start instanceof Date && !isNaN(start) && end instanceof Date && !isNaN(end)) {
    const diffTime = end.getTime() - start.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  } else {
    return 0;
  }
});

const nights = computed(() => durationInDays.value - 1);
const days = computed(() => durationInDays.value);

const formatDuration = (nights, days) => {
  return `${nights}박 ${days}일`;
};

const duration = computed(() => formatDuration(nights.value, days.value));

const formatDay = (date) => {
  return format(date, "yyyy년 MM월 dd일");
};

const tripMembers = computed(() => tripStore.members);

const membersWithColors = ref([]);

const { memberColors, rgbaColor } = useMemberColors(tripMembers);

const receivedCharacterName = ref(null);
const receivedCharacter = ref(null);

const handleMostCharacterUpdate = (characterName, character) => {
  receivedCharacterName.value = characterName;
  receivedCharacter.value = character;
};

onMounted(async () => {
  try {
    await Promise.all([
      tripStore.getTrip(tripId),
      paymentStore.getPayments(tripId),
    ]);

    if (paymentStore.getAllPayments().length > 0) {
      loading.value = false;
    }
  } catch (error) {
    loading.value = false;
  }
});

onMounted(() => {
  membersWithColors.value = tripMembers.value.map((member, index) => ({
    ...member,
    color: memberColors.value[index],
  }));
});

const showReferenceMessage = computed(() => !tripStore.imageUrl);

import member1 from "@/assets/img/member1.png";
import member2 from "@/assets/img/member2.png";
import member3 from "@/assets/img/member3.png";
import member4 from "@/assets/img/member4.png";

const images = [member1, member2, member3, member4];

const getImagePath = (index) => {
  return images[index % images.length];
};

const calculatePadding = (index) => {
  const paddingValues = [0, 15, 40, 40];
  return `${paddingValues[index % paddingValues.length]}px`;
};

const sketchSection = ref(null);

const scrollToTarget = () => {
  if (sketchSection.value) {
    sketchSection.value.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
.main-container {
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  margin: 0px auto;
  padding: 0px;
  background-color: #f4f6fa;
  /* border: 1px solid black; */
}

/* 구획 나누기 */
.trip {
  margin: 20px auto;
  /* border: 2px solid blue; */
}

.paymentTrip {
  margin: 10px auto;
  /* border: 2px solid blue; */
}

.title {
  font-size: x-large;
  font-weight: bolder;
  padding: 5px 20px;
}

.subtitle {
  font-size: medium;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.content {
  background-color: #ffffff;
  padding: 10px 20px;
}

.content * {
  font-size: 1rem;
}

/* 국가 */
.country {
  display: flex;
  justify-content: center;
  /* 수평 가운데 정렬 */
  align-items: center;
  /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 200px;
  font-size: 40px;
  /* font-weight: bolder; */
  position: relative;
  overflow: hidden;
}

.background {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background-size: cover;
  background-position: center;
  opacity: 0.4;
  z-index: 1;
}

.reference-message {
  position: absolute;
  top: 10px;
  right: 10px;
  /* background-color: rgba(255, 255, 255, 0.7); */
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 12px;
  z-index: 2;
  /* Ensure it's above the background */
  color: rgb(169, 169, 169);
  display: flex;
  justify-content: center;
  align-items: center;
  /* border: 1px solid black; */

}

/* 날짜 */
.date {
  margin-top: -10px;
}

.date>.content {
  padding-left: 35px;
}

.dday {
  font-size: large;
  margin: auto;
}

/* 멤버 */
.member * {
  margin: 0px auto;
}

.member>.title {
  display: flex;
}

.background-member {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 200px;
  max-width: 400px;
  /* 한 화면에 4명씩 (4 * 100px) */
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.member-list {
  display: flex;
  align-items: center;
  justify-content: flex;
  width: 100px;
  /* 각 사진의 너비 */
  height: 100%;
  background-size: cover;
  background-position: center;
  scroll-snap-align: start;
  /* Snap alignment */
  flex-shrink: 0;
  /* Prevent shrinking */
  /* border: 1px solid black; */
  padding-bottom: 55px;
  padding-left: 10px;
}

.member-symbol {
  border: 1px solid black;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.member-familyname {
  font-weight: 500;
}

/* 지출내역 */
.money {
  width: 100%;
  padding: 10px 0;
  margin: 0 auto;
  padding: 20px 0 50px 0;
}

.money .content {
  width: 100%;
  /* border: 1px solid black; */
}

/* 스케치 */
.sketch {
  width: 100%;
  overflow-x: hidden;
  margin: 0 auto;
}

.sketch .content {
  padding: 30px 20px;
}

.text {
  position: relative;
  z-index: 2;

  font-weight: 500;

  text-decoration-line: underline;
  text-decoration-thickness: 2px;
  text-decoration-style: wavy;
  text-underline-offset: 7px;
  /* 글자-밑줄 간격 */
  text-decoration-skip-ink: none;

  /* 페이드인 페이드아웃 */
  /* transition: opacity 0.5s ease-in-out;
  opacity: 0;
  animation: fadeInOut 3s infinite; */
}

@keyframes fadeInOut {

  0%,
  100% {
    opacity: 0;
  }

  50% {
    opacity: 1;
  }
}

.info {
  text-align: right;
}

.category-image {
  max-width: 30%;
}

.mbti-info {
  text-align: center;
}

/* 로딩 화면 */
.loading {
  height: 93vh;
  overflow-y: none;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  padding: 0px;
  background-color: #f4f6fa;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
