import axios from 'axios';
import { useUserStore } from '@/stores/userStore';
// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: 'https://5illjjang.click/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'  // Content-Type 기본값 설정
  } 
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


export default axiosInstance;