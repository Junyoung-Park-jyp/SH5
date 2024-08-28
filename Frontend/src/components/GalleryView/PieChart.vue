<template>
  <div ref="pieChart" style="width: 100%; height: 400px" class="my-chart"></div>
  <div class="explanation">
    <div class="title">활용법</div>
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
    <!-- <div class="one">항공</div>
    <div class="two">숙소</div>
    <div class="three">식비</div>
    <div class="four">교통</div>
    <div class="five">쇼핑</div>
    <div class="six">기타</div>
    <div class="seven">카페</div>
    <div class="eight">관광</div> -->
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
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

export default {
  setup() {
    const pieChart = ref(null);
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

    const calculateCategoryData = () => {
      const payments = paymentStore.getAllPayments;
      const categoryMap = {};

      payments.forEach((payment) => {
        const category = payment.category;
        if (!categoryMap[category]) {
          categoryMap[category] = 0;
        }
        categoryMap[category] += payment.cost;
      });

      // 카테고리별 총 금액을 내림차순으로 정렬
      const sortedCategoryData = Object.entries(categoryMap)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value);

      return sortedCategoryData;
    };

    onMounted(() => {
      const chart = echarts.init(pieChart.value);

      const categoryData = calculateCategoryData();

      const option = {
        // title: {
        //   text: '지출 내역',
        //   left: 'center',
        //   textStyle: {
        //     fontFamily: 'Spoqa Han Sans Neo',
        //     fontSize: 24,
        //   },
        // },
        tooltip: {
          trigger: "item",
          formatter: function (params) {
            const iconUrl = icons[params.name]; // 해당 카테고리의 아이콘 URL 가져오기
            return `
              <div style="display: flex; align-items: center;">
                <img src="${iconUrl}" style="width: 20px; height: 20px; margin-right: 5px;" />
                <strong style="font-size:14px;">${params.name}</strong>
              </div>
              <div style="font-size:16px; color:${
                params.color
              };">${formatWithComma(params.value)}원</div>
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

    return { pieChart };
  },
};
</script>

<style scoped>
.explanation {
  border-top: 1px dashed lightgrey;
  text-align: left;
  width: 100%;
  margin: 0 auto;
  padding: 20px 0 10px 0px;
}

.title {
  margin-bottom: 10px;
  font-weight: 500;
  text-align: center;
}

.content {
  width: 100%;
  margin: 0 auto;
  padding: 5px 0px;
  font-size: 6px;
  /* border: 1px solid black; */
}

.first,
.second {
  /* font-size: 6px; */
  margin-bottom: 10px;
  /* margin-left: 30px; */
}

.idx {
  background-color: #d8e2fc;
  color: #4b72e1;
  padding: 3px 6px;
  margin-right: 5px;
  font-size: xx-small;
}

/*
.one {
  background-color: #becaf4;
}
.two {
  background-color:#a2b4ef;
}
.three {
  background-color:#849ae9;
}
.four {
  background-color: #728de8;
}
.five {
  background-color: #5f7dd6;
}
.six {
  background-color: #4d69b4;
}
.seven {
  background-color: #5a70ae;;
}
.eight {
  background-color: #415795;
} */
</style>
