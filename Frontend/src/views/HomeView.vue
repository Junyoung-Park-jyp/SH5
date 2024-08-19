<template>
  <v-app>
    <v-container>
      <v-row>
        <!-- 상단 네비게이션 -->
        <v-app-bar app dense>
          <v-spacer></v-spacer>
          <v-btn icon>
            <v-icon>mdi-message-outline</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-bell-outline</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-account-circle-outline</v-icon>
          </v-btn>
        </v-app-bar>
      </v-row>

      <!-- 계좌 정보 및 배너 -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="px-4 py-3">
            <v-row align="center">
              <v-col>
                <v-img src="https://via.placeholder.com/50" class="mr-4" max-width="50"></v-img>
                <div>
                  <h3 class="mb-1">내 계좌</h3>
                  <v-btn text>전체보기</v-btn>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <p>박준영님, 환영합니다.</p>
                <p>본인인증 하신 후 안전한 금융거래를 시작하세요.</p>
                <v-btn class="btn-blue">금융 거래하기</v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>

      <!-- 아이콘 버튼들 -->
      <v-row class="mt-4">
        <v-col cols="4">
          <v-card class="pa-3" outlined>
            <v-icon size="large" color="orange">mdi-chicken</v-icon>
            <p class="text-center">땡겨요</p>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="pa-3" outlined>
            <v-icon size="large" color="pink">mdi-magnify</v-icon>
            <p class="text-center">대출비교/갈아타기</p>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="pa-3" outlined>
            <v-icon size="large" color="blue">mdi-credit-card</v-icon>
            <p class="text-center">SOL트래블</p>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>

</template>
<script setup>
</script>
<style scoped>
.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 16px;
}
</style>
