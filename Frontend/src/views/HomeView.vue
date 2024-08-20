<template>
  <v-container fluid class="py-4">
    <v-row>
      <v-col cols="12">
        <v-card class="account-card pa-4">
          <v-row no-gutters>
            <v-col class="text-left">
              <h3 class="mb-2">OOO님</h3>
              <p>계좌번호<br/>잔액</p>
            </v-col>
            <v-col class="text-right">
              <v-img src="your-image-url-here" max-width="100" contain></v-img>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="4">
        <v-card class="menu-card blue-card pa-4" outlined>
          <p class="text-center white--text">SOL트래블</p>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="menu-card blue-card pa-4" outlined>
          <p class="text-center white--text">SOL로 여행</p>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="menu-card white-card pa-4" outlined>
          <p class="text-center">환율조회</p>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-2">
      <v-col cols="4">
        <v-card class="menu-card white-card pa-4" outlined>
          <p class="text-center">환전</p>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="menu-card white-card pa-4" outlined>
          <p class="text-center">목표환율<br/>환전</p>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card class="menu-card white-card pa-4" outlined>
          <p class="text-center">메뉴추가</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <CountryDateForm />
</template>

<script setup>
import CountryDateForm from '@/components/TripReadyView/CountryDateForm.vue'
</script>

<style scoped>
.account-card {
  background-color: #f7f9fc;
  border-radius: 12px;
}

.menu-card {
  border-radius: 12px;
  height: 100%;
  font-size: 0.8rem;
}

.blue-card {
  background-color: #0471E9;
  color: #ffffff;
}

.white-card {
  background-color: #ffffff; 
}

.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 16px;
}

.mt-2 {
  margin-top: 8px;
}

.white--text {
  color: white !important;
}
</style>