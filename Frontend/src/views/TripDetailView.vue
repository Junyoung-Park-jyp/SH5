<template>
  <div class="main-container">
    <!-- 프로필 -->
    <div class="my-10 profile">
      <img class="profile-img" src="../assets/img/profile.png" alt="프로필" />
      <div class="profile-status">
        최한진 님은<br />
        <span class="profile-destination">{{ destination }}</span>
        여행 {{ tripState }}중
      </div>
    </div>

    <div class="pick-container">
      <!-- ALL -->
      <div class="all" @click="handleAllClick">
        <div class="upper">&nbsp;</div>
        <div class="middle" :class="{ 'pick-circle': selectedView === 'all' }">
          A
        </div>
        <div class="bottom">ALL</div>
      </div>
      <!-- 준비 -->
      <div class="prepare" @click="handlePrepareClick">
        <div class="upper">&nbsp;</div>
        <div
          class="middle"
          :class="{ 'pick-circle': selectedView === 'prepare' }"
        >
          P
        </div>
        <div class="bottom">준비</div>
      </div>

      <!-- 구분선 -->
      <div class="line">|</div>

      <!-- 날짜 스크롤 -->
      <div class="day-scroll">
        <div
          v-for="(day, i) in date"
          :key="i"
          class="day-container"
          @click="handleDayClick(day)"
        >
          <div class="upper">{{ format(day, "EEE") }}</div>
          <div class="middle" :class="{ 'pick-circle': isSelectedDay(day) }">
            {{ format(day, "d") }}
          </div>
          <div class="bottom">{{ format(day, "M") }}월</div>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="arrow">></div>
    </div>

    <Detail
      :selectedDate="selectedDate"
      :showAllContainers="showAllContainers"
      :showBudgetAndBookingOnly="showBudgetAndBookingOnly"
      :selectedView="selectedView"
      @updateCheckedCost="updateCheckedCost"
    />

    <!-- 정산하기 -->
    <div class="adjustment">
      <div class="adjust-background">
        <button
          class="adjust-btn"
          @mousedown="startDrag"
          @mousemove="onDrag"
          @mouseup="stopDrag"
          @touchstart="startDrag"
          @touchmove="onDrag"
          @touchend="stopDrag"
          ref="adjustmentDiv"
        >
          정 산 하 기
        </button>
        <button class="slide-btn">> > ></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { eachDayOfInterval, format, isSameDay } from "date-fns";
import Detail from "@/components/TripDetailView/Detail.vue";
import { usePaymentStore } from "@/stores/paymentStore";

// 여행 상태 (예: "준비", "진행 중", "완료")
const tripState = ref("준비"); // 예시로 "준비"로 초기화

const router = useRouter();
const adjustmentDiv = ref(null); // 정산 버튼 참조
const isDragging = ref(false); // 드래그 상태를 관리하는 변수
const startX = ref(0); // 드래그 시작 시 X 좌표 저장
const currentX = ref(0); // 현재 드래그 위치의 X 좌표 저장

const country = "대한민국";
const city = "부산";
const destination = ref(country === "대한민국" ? city : country);

const today = new Date();
today.setHours(0, 0, 0, 0);

const selectedDate = ref(today);
const selectedView = ref("all");  // 선택된 뷰 ("all", "prepare", "date")

// 여행 시작일 및 종료일
const startDate = new Date(2024, 7, 10);
const endDate = new Date(2024, 7, 30);

// 여행 기간 동안의 모든 날짜 생성
const date = eachDayOfInterval({
  start: startDate,
  end: endDate,
});

const paymentStore = usePaymentStore();

// "ALL" 버튼이 선택되었을 때 모든 날짜의 지출 내역을, 특정 날짜가 선택되었을 때 해당 날짜의 지출 내역을 계산
const payments = computed(() => {
  if (selectedView.value === "all") {
    return paymentStore.getAllPayments();  // 모든 날짜의 지출 내역 가져오기
  } else {
    return paymentStore.getPaymentsByDate(format(selectedDate.value, "yyyy-MM-dd"));  // 특정 날짜의 지출 내역 가져오기
  }
});

const isToday = (day) => isSameDay(day, today);

const showAllContainers = ref(true); // 모든 컨테이너 표시 여부
const showBudgetAndBookingOnly = ref(false); // 예산 및 예약 컨테이너만 표시 여부

// 특정 날짜를 클릭했을 때 실행되는 함수
const handleDayClick = (day) => {
  selectedDate.value = day;
  selectedView.value = "date";
  showAllContainers.value = false;
  showBudgetAndBookingOnly.value = false;
};

// ALL 버튼을 클릭했을 때 실행되는 함수
const handleAllClick = () => {
  selectedView.value = "all";
  showAllContainers.value = true;
  showBudgetAndBookingOnly.value = false;
};

// 준비 버튼을 클릭했을 때 실행되는 함수
const handlePrepareClick = () => {
  selectedView.value = "prepare";
  showAllContainers.value = false;
  showBudgetAndBookingOnly.value = true;
};

// 특정 날짜가 선택된 날짜인지 확인하는 함수
const isSelectedDay = (day) => {
  return selectedView.value === "date" && isSameDay(day, selectedDate.value);
};

// 오늘 날짜의 인덱스 찾기
const todayIndex = date.findIndex((day) => isToday(day));

onMounted(() => {
  const dayScrollContainer = document.querySelector(".day-scroll");
  const todayElement = dayScrollContainer.children[todayIndex];

  if (todayElement) {
    dayScrollContainer.scrollLeft =
      todayElement.offsetLeft -
      dayScrollContainer.clientWidth / 2 +
      todayElement.clientWidth / 2;
  }

  const arrowElement = document.querySelector(".arrow");
  if (dayScrollContainer.scrollWidth > dayScrollContainer.clientWidth) {
    arrowElement.style.display = "block";
  } else {
    arrowElement.style.display = "none";
  }
});

const startDrag = (event) => {
  isDragging.value = true;
  startX.value = event.clientX || event.touches[0].clientX;
  currentX.value = startX.value;
};

const onDrag = (event) => {
  if (isDragging.value) {
    const x = event.clientX || event.touches[0].clientX;
    const deltaX = x - startX.value;

    const maxDragDistance =
      adjustmentDiv.value.parentElement.offsetWidth -
      adjustmentDiv.value.offsetWidth;

    if (deltaX > 0 && deltaX <= maxDragDistance) {
      adjustmentDiv.value.style.transform = `translateX(${deltaX}px)`;
      currentX.value = x;
    }
  }
};

const stopDrag = () => {
  if (isDragging.value) {
    isDragging.value = false;

    const dragDistance = currentX.value - startX.value;
    const threshold = adjustmentDiv.value.offsetWidth / 2;

    if (dragDistance > threshold) {
      finishTrip();
    } else {
      adjustmentDiv.value.style.transform = `translateX(0)`;
    }
  }
};

// 체크된 비용 저장
const checkedCost = ref("");

// Detail 컴포넌트에서 업데이트된 비용을 저장하는 함수
const updateCheckedCost = (cost) => {
  checkedCost.value = cost; // Update when Detail.vue emits
};

// 정산 완료 버튼 슬라이딩
const finishTrip = () => {
  adjustmentDiv.value.style.transform = `translateX(100%)`;

  setTimeout(() => {
    router.push({
      name: "tripFinish",
      query: { amount: checkedCost.value }, // Use query instead of params
    });
  }, 300);
};
</script>

<style scoped>
.main-container {
  height: 93vh;
  overflow-y: none;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px auto;
  background-color: #f4f6fa;
  /* margin-bottom: -10px; */
}

/* 프로필 */
.profile {
  display: flex;
  justify-content: left; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 100px;
}

.profile-img {
  height: 75px;
  margin-left: 20px;
  margin-right: 25px;
}

.profile-status {
  font-weight: bold;
  font-size: 1.25rem;
}

.profile-destination {
  font-weight: bolder;
  font-size: x-large;
  padding-right: 4px;
  text-decoration-line: underline;
  text-decoration-style: wavy;
  text-decoration-thickness: 2px;
  text-underline-offset: 4px; /* 글자-밑줄 간격 */
  text-decoration-skip-ink: none;
}

/* 구획 나누기 */
.pick-container {
  width: 95%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  height: 100px;
  margin: -40px auto 20px auto;
}

.all,
.prepare {
  width: 30px;
  margin: 0px 5px;
  padding: 0;
  flex-shrink: 0;
}

.line {
  margin: auto 0px;
}

.day-scroll {
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: row;
  white-space: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
  margin: 0px 10px;
}

.arrow {
  margin: 0px 5px;
  display: none;
}

.upper,
.middle,
.bottom {
  height: 30%;
  margin: 0 auto;
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
}

.upper,
.bottom {
  font-size: xx-small;
  color: rgb(109, 109, 109);
}

.middle {
  font-weight: 600;
  margin: 5px 0px;
}

/* 날짜 */
.day-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  padding: 0 10px;
  width: 100%;
}

/* 날짜 */
.day-scroll::-webkit-scrollbar {
  display: none; /* 웹킷 브라우저에서 스크롤바 숨김 */
}

.pick-circle {
  background-color: #4b72e1;
  color: white;
  font-size: 0.7rem;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 6px auto; /* Center horizontally */
}

/* .carousel-container {
  display: flex;
  align-items: center;
}

.carousel {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-item {
  display: flex;
  flex: 0 0 100%;
  justify-content: center;
} */

/* .v-btn {
  cursor: pointer;
}

.v-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
} */

/* 정산하기 */
.adjustment {
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  width: 100%;
  height: 125px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  text-align: center;
  padding: 15px 0;
  margin: 0 auto;
  /* border: 1px solid black; */
  background-color: rgba(255, 255, 255);
}

.adjust-background {
  width: 80%;
  height: 60%;
  background-color: lightgrey;
  border-radius: 30px;
  margin: 8px 20px;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.adjust-btn {
  width: 60%;
  height: 100%;
  background-color: #4b72e1;
  border-radius: 30px;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  transition: transform 0.3s ease; /* 슬라이딩 애니메이션 */
  position: relative;
  z-index: 1;
}

.slide-btn {
  width: 40%;
  height: 100%;
  border-radius: 30px;
  color: rgb(78, 78, 78);
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
  position: absolute;
  right: 0;
  z-index: 0;
}
</style>
