import { ref, watch } from "vue";

// 색상 배열
const colors = [
  "#CA7172",
  "#FBCC98",
  "#D5FB98",
  "#98D1FB",
  "#98B4FB",
  "#B598FB",
  "#FB98F1",
  "#ACACAC",
];

// Composable function to handle member colors
export function useMemberColors(members) {
  const memberColors = ref([]);

  // 로컬 스토리지에서 색상 불러오기
  const loadColors = () => {
    const storedColors = JSON.parse(localStorage.getItem("memberColors"));
    if (storedColors && storedColors.length === members.value.length) {
      memberColors.value = storedColors;
    } else {
      memberColors.value = members.value.map(
        (_, index) => colors[index % colors.length]
      );
    }
  };

  // 로컬 스토리지에 색상 저장
  const saveColors = () => {
    localStorage.setItem("memberColors", JSON.stringify(memberColors.value));
  };

  // 색상을 변경하는 함수
  const changeColor = (index) => {
    const currentColor = memberColors.value[index];
    const currentColorIndex = colors.indexOf(currentColor);
    const nextColorIndex = (currentColorIndex + 1) % colors.length;
    memberColors.value[index] = colors[nextColorIndex];
    saveColors(); // 변경된 색상을 저장
  };

  // Hex 색상을 RGBA로 변환하여 투명도를 조절하는 함수
  const rgbaColor = (hex = "#d3d3d3", alpha = 1) => {
    if (!hex || typeof hex !== "string" || hex.length !== 7) {
      hex = "#d3d3d3"; // 기본값 설정
    }
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  };

  // 멤버 목록이 변경될 때마다 색상 배열 업데이트
  watch(
    members,
    (newMembers) => {
      if (newMembers.length > 0) {
        loadColors();
      }
    },
    { immediate: true }
  );

  return {
    memberColors,
    changeColor,
    rgbaColor,
  };
}