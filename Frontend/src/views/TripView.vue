<template>
  <v-container>
    <v-row class="my-10 justify-center">
      <h1>ㅇㅇㅇ 님</h1>
    </v-row>
    <v-row v-if="tripState === 0" class="py-5 my-5 justify-center">
      <v-btn @click="makeTrip">여행 만들기</v-btn>
    </v-row>
    <v-row v-else-if="tripState === 1" class="background-image py-5 my-5 justify-center" @click="goProgress">
      <v-icon icon="mdi-music"></v-icon>
      <h2>현재 스페인 여행 준비 중</h2>
      <v-icon icon="mdi-music"></v-icon>
    </v-row>
    <v-row v-else-if="tripState === 2" class="background-image py-5 my-5 justify-center" @click="goProgress">
      <v-icon icon="mdi-music"></v-icon>
      <h2>현재 스페인 여행 중</h2>
      <v-icon icon="mdi-music"></v-icon>
    </v-row>
    <v-row v-if="tripStore.tripExperiences.length > 0" class="justify-center py-5 my-5">
      <h2>총 {{ tripStore.tripExperiences.length }}회 SOL로 여행을 다녀오셨네요!</h2>
      <v-container>
        <v-row class="d-flex align-center">
          <v-col cols="2">
            <v-btn icon @click="prevSlide">
              <v-icon icon="mdi-chevron-left"></v-icon>
            </v-btn>
          </v-col>
          <v-col>
            <v-carousel v-model="currentSlide" :show-arrows="false">
              <v-carousel-item
                v-for="(experience, index) in tripStore.tripExperiences"
                :key="index"
                class="background-image"
              >
                  <v-img :src="experience.imageUrl" class="align-center"></v-img>
                <h2>{{ experience.city }}</h2>
                <h2>{{ experience.cost }}</h2>
              </v-carousel-item>
            </v-carousel>
          </v-col>
          <v-col cols="2">
            <v-btn icon @click="nextSlide">
              <v-icon icon="mdi-chevron-right"></v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script setup>
import { useUserStore } from '@/stores/userStore';
import { useTripStore } from '@/stores/tripStore';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';

const userStore = useUserStore();
const tripStore = useTripStore();

const router = useRouter();

const tripState = ref(1)  // 0: 여행 만들기 1: 여행 준비 중 2: 여행 중
const currentSlide = ref(0)

const getImageUrl = async (countryName) => {
  try {
    const response = await axios.get(
      `http://apis.data.go.kr/1262000/CountryFlagService2/getCountryFlagList2?serviceKey=vai590Q3ljVdLT1dzNoE5dEHmfwscfRSDAeUOKG%2Bl6GMUILcwCkmxrx2blG2%2FxO5ozfg4eC1ER%2B5nzpCg3Vdrw%3D%3D&pageNo=1&numOfRows=1&cond[country_nm::EQ]=${countryName}`
    )
    return response.data.data[0]?.download_url;
  } catch (error) {
    console.error(error);
    return null;
  }
};

onMounted(async () => {
  for (const experience of tripStore.tripExperiences) {
    experience.imageUrl = await getImageUrl(experience.country);
  }
});

const prevSlide = () => {
  currentSlide.value = currentSlide.value > 0 ? currentSlide.value - 1 : tripStore.tripExperiences.length - 1;
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % tripStore.tripExperiences.length;
};

const makeTrip = () => {
  router.push({ name: 'createTrip' })
}

const goProgress = () => {
  router.push({ name: 'progresstrip' })
}
</script>

<style scoped>
.v-carousel {
  height: 300px !important;
}

.background-image {
  background-image: url('@/assets/img/travel.png');
  background-size: cover;
  background-position: center;
}

.v-carousel-item {
  text-align: center;
  color: black;

  display: flex;
  justify-content: center;
}

.v-img {
  width: 50%;
}
</style>