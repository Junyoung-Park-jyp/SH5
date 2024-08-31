<template>
  <div>
    <!-- 아이콘 -->
    <div class="info">
      <v-icon @click="showExplanation = true" class="info-icon" icon="mdi-information" size="22px"
        color="gray"></v-icon>
    </div>

    <!-- 파이 차트 -->
    <div ref="pieChart" style="width: 100%; height: 400px" class="my-chart"></div>

    <!-- 모달 -->
    <v-dialog v-model="showExplanation" max-width="500px" class="explanation">
      <v-card>
        <v-card-title class="headline">활용법</v-card-title>
        <v-card-text>
          <div class="content">
            <div class="first">
              <span class="idx">1</span>
              원형 차트를 클릭하여 지출 금액을 확인하세요
            </div>
            <div class="second">
              <span class="idx">2</span>
              하단 범례를 클릭하여 카테고리를 추가/제거하세요
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn class="ok-btn" text @click="showExplanation = false">확인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineEmits } from "vue";
import * as echarts from "echarts";
import { usePaymentStore } from "@/stores/paymentStore";
import { formatWithComma } from "@/stores/currencyStore";

// 이미지 파일을 import로 가져오기
import airplaneIcon from "@/assets/img/category/airplane.png";
import hotelIcon from "@/assets/img/category/hotel.png";
import vehicleIcon from "@/assets/img/category/vehicle.png";
import foodIcon from "@/assets/img/category/food.png";
import cafeIcon from "@/assets/img/category/cafe.png";
import shoppingIcon from "@/assets/img/category/shopping.png";
import tourIcon from "@/assets/img/category/tour.png";
import etcIcon from "@/assets/img/category/etc.png";

import DOREMI from "@/assets/img/mbti/DOREMI.png";
import LAY from "@/assets/img/mbti/LAY.png";
import LULULALA from "@/assets/img/mbti/LULULALA.png";
import MOLI from "@/assets/img/mbti/MOLI.png";
import PLI from "@/assets/img/mbti/PLI.png";
import RINO from "@/assets/img/mbti/RINO.png";
import SHOO from "@/assets/img/mbti/SHOO.png";
import SOL from "@/assets/img/mbti/SOL.png";

// emit 정의
const emit = defineEmits(['updateMostCharacter']);

// Refs
const pieChart = ref(null);
const showExplanation = ref(false);
const mostCategory = ref(null);

// Store 사용
const paymentStore = usePaymentStore();

// 카테고리별 아이콘 경로
const icons = {
  항공: airplaneIcon,
  숙소: hotelIcon,
  교통: vehicleIcon,
  식비: foodIcon,
  카페: cafeIcon,
  쇼핑: shoppingIcon,
  관광: tourIcon,
  기타: etcIcon,
};

// 카테고리별 캐릭터 이미지 경로
const mbtiCharacters = {
  교통: SOL,
  카페: MOLI,
  기타: RINO,
  숙소: SHOO,
  식비: DOREMI,
  항공: LULULALA,
  관광: PLI,
  쇼핑: LAY,
};

// // 가장 많이 사용된 카테고리에 해당하는 캐릭터 이미지를 가져오는 계산 속성
// const mostCharacterImage = computed(() => {
//   return mostCategory.value ? mbtiCharacters[mostCategory.value] : null;
// });

// 카테고리 데이터 계산 함수
const calculateCategoryData = () => {
  const payments = paymentStore.getAllPayments();
  const categoryMap = {};
  payments.forEach((payment) => {
    const category = payment.category;
    if (!categoryMap[category]) {
      categoryMap[category] = 0;
    }
    categoryMap[category] += payment.amount;
  });

  // 카테고리별 총 금액을 내림차순으로 정렬
  const sortedCategoryData = Object.entries(categoryMap)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);

  return sortedCategoryData;
};

// onMounted 훅에서 차트 생성
onMounted(() => {
  const chart = echarts.init(pieChart.value);

  const categoryData = calculateCategoryData();

  // 지출 내역이 가장 많은 카테고리
  mostCategory.value = categoryData[0].name;

  const character = mostCategory.value ? mbtiCharacters[mostCategory.value] : null;
  emit('updateMostCharacter', character); // 부모 컴포넌트로 이벤트 emit

  const option = {
    tooltip: {
      trigger: "item",
      formatter: function (params) {
        const iconUrl = icons[params.name]; // 해당 카테고리의 아이콘 URL 가져오기
        return `
          <div style="display: flex; align-items: center;">
            <img src="${iconUrl}" style="width: 20px; height: 20px; margin-right: 5px;" />
            <strong style="font-size:14px;">${params.name}</strong>
          </div>
          <div style="font-size:16px; color:${params.color};">${formatWithComma(params.value)}원</div>
          <div style="font-size:12px;">${params.percent}%</div>
        `;
      },
      textStyle: {
        fontFamily: "Spoqa Han Sans Neo", // 툴팁 글씨체 지정
      },
    },
    legend: {
      orient: "horizontal",
      left: "center",
      bottom: "3%", // legend의 위치를 아래로 조정
      itemGap: 20, // 항목 사이의 간격을 조정하여 4개씩 표시되도록 함
      width: "92%", // 4개씩 보기 좋게 배치되도록 넓이를 조정
      textStyle: {
        fontFamily: "Spoqa Han Sans Neo", // legend 글씨체 지정
        fontSize: 14,
      },
    },
    color: [
      "#becaf4",
      "#a2b4ef",
      "#849ae9",
      "#728de8",
      "#5f7dd6",
      "#4d69b4",
      "#5a70ae",
      "#415795",
    ],
    series: [
      {
        name: "지출",
        type: "pie",
        radius: "55%",
        center: ["50%", "40%"], // 차트를 정가운데에 위치
        data: categoryData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
        label: {
          formatter: function (params) {
            // params.percent의 정수 부분만 사용
            const percentage = Math.floor(params.percent);
            return `{nameStyle|${params.name}}\n{percentStyle|${percentage}%}`;
          },
          rich: {
            nameStyle: {
              fontSize: 12,
              fontFamily: "Spoqa Han Sans Neo",
              fontWeight: "bold",
              color: "#333",
            },
            percentStyle: {
              fontSize: 12,
              fontFamily: "Spoqa Han Sans Neo",
              color: "#999",
            },
          },
        },
      },
    ],
  };

  chart.setOption(option);
});
</script>

<style scoped>
.info {
  width: 100%;
  display: flex;
  justify-content: end;
  align-items: center;
}

.explanation {
  border-top: 1px dashed lightgrey;
  text-align: left;
  width: 100%;
  margin: 0 auto;
  padding: 20px 0 10px 0px;
}

.headline {
  margin-bottom: 10px;
  font-weight: 500;
  text-align: center;
  margin-top: 20px;
}

.content {
  width: 100%;
  margin: 0 auto;
  padding: 5px 0px 5px 0px;
}

div.content>div.first,
div.content>div.second {
  font-size: 13px !important;
  margin-bottom: 10px;
}

div.content>div.first>span.idx,
div.content>div.second>span.idx {
  background-color: #d8e2fc;
  color: #4b72e1;
  padding: 3px 6px;
  margin-right: 3px;
  font-size: 13px;
}

.ok-btn {
  color: #4b72e1;
}

.mbti-character {
  /* margin-top: 20px; */
  /* display: flex;
  justify-content: start;
  align-items: center; */
}

.mbti-character img {
  max-width: 30%;
}
</style>