import axios from 'axios';

// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    // 'Authorization': `Bearer ${token}`
  },
  timeout: 10000, 
});

// 요청 인터셉터 (추가적인 설정이 필요할 경우)
axiosInstance.interceptors.request.use(
  config => {
    // const token = store.getters['auth/token'];
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`;
    // }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 예를 들어, 401 에러에 대한 처리
    // if (error.response.status === 401) {
    //   // 로그아웃 또는 리프레시 토큰 로직
    // }
    return Promise.reject(error);
  }
);

export default axiosInstance;