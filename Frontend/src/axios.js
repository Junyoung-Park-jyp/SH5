import axios from 'axios';
import { useUserStore } from '@/stores/userStore';
// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: 'http://52.79.246.151:8000',
  timeout: 5000, 
});

// // 요청 인터셉터 (추가적인 설정이 필요할 경우)
axiosInstance.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    if (userStore.token) {
      config.headers.Authorization = `Token ${userStore.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);


// axiosInstance.interceptors.response.use(
//   response => {
//     return response;
//   },
//   error => {
//     // 예를 들어, 401 에러에 대한 처리
//     // if (error.response.status === 401) {
//     //   // 로그아웃 또는 리프레시 토큰 로직
//     // }
//     return Promise.reject(error);
//   }
// );

export default axiosInstance;