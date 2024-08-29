<template>
  <div class="main-container">
    <!-- 프로필 -->
    <div class="my-5 profile">
      <img class="profile-img" src="../assets/img/profile.png" alt="프로필" />
      <span>{{ userStore.userName }} 님
      </span>
    </div>

    <!-- 미래/현재 -->
    <div class="non-past">
      <v-row class="d-flex align-center">
        <v-carousel
          :show-arrows="true"
          hide-delimiters
          :cycle="false"
          class="non-past-carousel"
        >
          <template v-slot:prev="{ props }">
            <v-btn icon color="none" variant="text" @click="props.onClick">
              <v-icon
                class="btns"
                icon="mdi-chevron-left"
                size="xx-large"
              ></v-icon>
            </v-btn>
          </template>
          <template v-slot:next="{ props }">
            <v-btn icon color="none" variant="text" @click="props.onClick">
              <v-icon
                class="btns"
                icon="mdi-chevron-right"
                size="xx-large"
              ></v-icon>
            </v-btn>
          </template>

          <v-carousel-item
            v-for="(ongoingTrip, index) in ongoingTrips"
            :key="index"
            class="background-image-now"
            @click="goTripMain(ongoingTrip.id)"
          >
            <div class="info">
              <span>
                <v-icon icon="mdi-music"></v-icon>
                {{ ongoingTrip.trip_name }}
                <v-icon icon="mdi-music"></v-icon>
              </span>
            </div>
          </v-carousel-item>
        </v-carousel>
      </v-row>
    </div>

    <!-- 과거 -->
    <div class="past">
      <v-row
        v-if="pastTrips.length > 0"
        class="justify-center py-5 my-5"
      >
        <div class="record">
          총 {{ pastTrips.length }}회 SOL로 여행을 다녀오셨네요!
        </div>
        <div class="record-carousel">
          <v-row class="d-flex align-center">
            <!-- <v-col cols="2">
              <v-btn icon @click="prevSlide" variant="tonal">
                <v-icon icon="mdi-chevron-left" size="xx-large"></v-icon>
              </v-btn>
            </v-col> -->
            <v-col>
              <v-carousel
                v-model="currentSlide"
                :show-arrows="false"
                cycle
                interval="3000"
              >
                <!-- <v-carousel-item
                  v-for="(experience, index) in tripStore.tripExperiences"
                  :key="index"
                  class="background-image"
                >
                  <div class="info2">
                    <v-img
                      :src="experience.imageUrl"
                      class="align-center"
                    ></v-img>
                    <div class="trip-name">{{ experience.tripName }}</div>
                    <div class="city">
                      {{
                        Array.isArray(experience.city)
                          ? experience.city.join(", ")
                          : experience.city
                      }}
                    </div>
                    <div class="cost">{{ formatCost(experience.cost) }}</div>
                  </div>
                </v-carousel-item> -->
                <v-carousel-item
                  v-for="(experience, index) in tripStore.pastTrips"
                  :key="index"
                  class="background-image"
                  @click="goTripGallery(experience.id)"
                >
                  <div class="info2">
                    <v-img
                      :src="experience.imageUrl"
                      class="align-center"
                    ></v-img>
                    <div class="trip-name">{{ experience.trip_name }}</div>
                    <div class="city">
                      {{
                        Array.isArray(experience.city)
                          ? experience.city.join(", ")
                          : experience.city
                      }}
                    </div>
                  </div>
                </v-carousel-item>
              </v-carousel>
            </v-col>
            <!-- <v-col cols="2">
              <v-btn icon @click="nextSlide" variant="tonal">
                <v-icon icon="mdi-chevron-right" size="xx-large"></v-icon>
              </v-btn>
            </v-col> -->
          </v-row>
        </div>
      </v-row>
      <div v-else class="non-record">
        <div class="txt">SOL로 여행 기록이 없습니다</div>
        <div class="circle"></div>
      </div>
    </div>

    <!-- 여행 만들기 -->
    <div class="bottom" ref="bottomDiv">
      <button class="create-btn" @click="makeTrip">여행 만들기</button>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/userStore";
import { useTripStore } from "@/stores/tripStore";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useStateStore } from "@/stores/stateStore";

import axios from "axios";

const userStore = useUserStore();
const tripStore = useTripStore();
const router = useRouter();
const ongoingTrips = computed(() => tripStore.futureTrips)
const pastTrips = computed(() => tripStore.pastTrips)
const stateStore = useStateStore();
const currentSlide = ref(0);
const bottomDiv = ref(null);

const getImageUrl = async (countryName) => {
  // try {
  //   const response = await axios.get(
  //     'http://apis.data.go.kr/1262000/CountryFlagService2/getCountryFlagList2?serviceKey=vai590Q3ljVdLT1dzNoE5dEHmfwscfRSDAeUOKG%2Bl6GMUILcwCkmxrx2blG2%2FxO5ozfg4eC1ER%2B5nzpCg3Vdrw%3D%3D&pageNo=1&numOfRows=1&cond[country_nm::EQ]=${countryName}'
  //   )
  //   return response.data.data[0]?.download_url;
  // } catch (error) {
  //   console.error(error);
  //   return null;
  // }
};

onMounted(async () => {
  await Promise.all([
    tripStore.getPastTrips(),
    tripStore.getFutureTrips()
  ]);

  for (const experience of tripStore.tripExperiences) {
    experience.imageUrl = await getImageUrl(experience.country);
  }
  stateStore.getAILABapi({});
});

const prevSlide = () => {
  currentSlide.value =
    currentSlide.value > 0
      ? currentSlide.value - 1
      : tripStore.tripExperiences.length - 1;
};

const nextSlide = () => {
  currentSlide.value =
    (currentSlide.value + 1) % tripStore.tripExperiences.length;
};

const makeTrip = () => {
  const bottom = bottomDiv.value;
  bottom.classList.add("expand");

  // 애니메이션이 끝난 후 페이지 이동
  setTimeout(() => {
    router.push({ name: "createTrip" });
  }, 1000); // 애니메이션 길이와 일치시켜야 함
};

const goTripMain = (tripId) => {
  console.log('Navigating to tripMain with ID:', tripId);  // 디버그 로그 추가
  router.push({ name: "tripMain", params: { id: tripId } });
};

const goTripGallery = (tripId) => {
  console.log('Navigating to gallery with ID:', tripId);  // 디버그 로그 추가
  router.push({ name: "gallery", params: { id: tripId } });
};

// cost 포맷팅
const formatCost = (cost) => {
  return cost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "원";
};

</script>

<style scoped>
.main-container {
  height: 92vh;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  margin: 0px auto;
  padding-bottom: 60px;
  background-color: #f4f6fa;
}

.profile {
  display: flex;
  justify-content: left; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  margin: 0px auto;
  height: 100px;
}

.profile > img {
  height: 75px;
  margin-left: 30px;
  margin-right: 20px;
}

.profile > span {
  font-weight: bolder;
  font-size: xx-large;
}

.past {
  /* margin: 50px; */
  padding-top: 20px;
  margin: 0 auto;
  width: 100%;
  justify-content: center;
  text-align: center;
}

.record {
  width: 100%;
  /* background-color: grey; */
  text-align: center;
  font-size: 20px;
  font-weight: bold;
}

.record-carousel {
  width: 85%;
  margin: 0 auto;
  margin-top: 15px;
}

.v-carousel {
  height: 300px !important;
}

.v-carousel-item {
  display: flex;
  justify-content: center; /* 수평 가운데 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  text-align: center;
  color: black;
  height: 100%;
}

.background-image-now {
  background-image: url("@/assets/img/spain.jpg");
  background-size: cover;
  background-position: center;
  opacity: 0.8;
  pointer-events: auto;
}

.background-image {
  /* background-image: url("@/assets/img/travel.png"); */
  background-color: lightgrey;
  background-size: cover;
  background-position: center;
  pointer-events: auto;
}

.non-past {
  margin: 0 auto;
}

.non-past-carousel {
  margin-top: 0px;
  height: 120px !important;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: large;
  height: 100%;
}

.info2 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: large;
  height: 65%;
}

.info * {
  font-size: x-large;
  font-weight: bolder;
}

.trip-name {
  font-size: 28px;
  font-weight: 500;
}

.city {
  font-size: 18px;
  font-weight: 500;
}

.cost {
  font-size: 22px;
  font-weight: 500;
}

.v-img {
  width: 50%;
}

/* 기록이 없는 경우 */
.non-record {
  width: 100%;
  height: 100%;
  position: absolute;
  bottom: 20%;
  /* border: 1px solid black; */
}

.non-record .txt {
  position: absolute;
  width: 100%;
  bottom: 5%;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 35px;
  /* border: 1px solid blue; */
}

.non-record .circle {
  position: absolute;
  left: 50%;
  bottom: 0%;
  transform: translateX(-50%);
  width: 12px;
  height: 12px;
  background-color: black;
  border-radius: 50%;
  animation: bounce 0.65s infinite alternate cubic-bezier(0.1, 0.49, 0.42, 0.99);
}

@keyframes bounce {
  0% {
    transform: translate(-50%, 25px);
  }

  100% {
    transform: translate(-50%, -15px);
  }
}

/* 하단 */
.bottom {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 90px;
  text-align: center;
  padding: 20px 0;
  margin: 0 auto;
  background-color: rgba(80, 80, 80, 0.2);
  border-radius: 20px 20px 0px 0px;
  transition: height 1s ease, bottom 1s ease;
}

.bottom.expand {
  height: 100vh;
  bottom: 0;
  left: 50%;
  /* transform: none; */
  border-radius: 0px;
  background-color: rgba(80, 80, 80, 0.6);
  border-radius: 20px 20px 0px 0px;
}

.create-btn {
  width: 80%;
  background-color: #4b72e1;
  border-radius: 30px;
  color: white;
  padding: 8px 20px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}
</style>
