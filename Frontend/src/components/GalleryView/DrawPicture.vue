<template>
  <div class="main-container">
    <div v-if="loading">
      <v-progress-circular v-if="loading" indeterminate :size="50" :width="8" color="#4b72e1"
        class="mb-5"></v-progress-circular>
      <div class="create-text">사진 생성 중입니다</div>
    </div>

    <div v-if="resultImageUrl" class="mb-5">
      <v-img :src="resultImageUrl" />
    </div>

    <div v-if="!loading && !saveImageFlag" class="pick mt-0 mb-3">
      <!-- <input type="file" @change="onFileChange" accept="image/*" /> -->

      <div class="file-container">
        <label class="file-input">
          <input type="file" @change="onFileChange" accept="image/*" />
          <span>{{ selectedFileName }}</span>
          <v-icon class="upload-icon" icon="mdi-upload"></v-icon>
        </label>
      </div>

    </div>
    <div v-if="!loading && !resultImageUrl && !saveImageFlag" class="create">
      <button class="create-btn" @click="uploadImage">사진 생성</button>
    </div>
    <div v-if="!loading && resultImageUrl && !saveImageFlag" class="create">
      <button class="create-btn" @click="saveImage">사진 저장</button>
    </div>
    <div v-if="saveImageFlag">
      저장이 완료되었습니다.
    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";

import { useStateStore } from "@/stores/stateStore";
import { useTripStore } from "@/stores/tripStore";
import { useErrorStore } from "@/stores/errorStore";

import axiosInstance from '@/axios';

const route = useRoute();

const tripId = route.params.id

const selectedFile = ref(null);
const selectedFileName = ref(null);
const resultImageUrl = ref(null);

const loading = ref(false);

const saveImageFlag = ref(false)

const stateStore = useStateStore()
const tripStore = useTripStore()
const errorStore = useErrorStore()

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  selectedFileName.value = event.target.files[0].name;
};

const uploadImage = async () => {
  // 이미지가 업로드 되지 않았을 경우
  if (!selectedFile.value) {
    errorStore.showError("이미지가 업로드 되지 않았습니다")
    return
  }

  loading.value = true;
  resultImageUrl.value = null;

  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);
    formData.append("index", 0); // Vintage Comic
    console.log("API_KEY 되냐", stateStore.apiKey);
    const responsePost = await axios.post(
      "https://www.ailabapi.com/api/image/effects/ai-anime-generator",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          // "ailabapi-api-key": process.env.VUE_APP_AILAB_API_KEY,
          "ailabapi-api-key": stateStore.apiKey,
        },
      }
    );

    const taskId = responsePost.data.task_id;
    await getResult(taskId);
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const getResult = async (taskId) => {
  return new Promise((resolve) => {
    const intervalId = setInterval(async () => {
      try {
        const responseGet = await axios.get(
          "https://www.ailabapi.com/api/common/query-async-task-result",
          {
            headers: {
              // "ailabapi-api-key": import.meta.env.VITE_AILABAPI_API_KEY,
              "ailabapi-api-key": stateStore.apiKey,
            },
            params: {
              task_id: taskId,
            },
          }
        );

        const taskStatus = responseGet.data.task_status;

        // 이미지 생성 완료
        if (taskStatus === 2) {
          resultImageUrl.value = responseGet.data.data.result_url;
          clearInterval(intervalId);
          resolve();
        } else if (taskStatus === 1) {
          console.log("Task is still processing.");
        } else {
          clearInterval(intervalId);
          resolve();
        }
      } catch (err) {
        clearInterval(intervalId);
        console.error(err);
        resolve();
      }
    }, 5000);
  });
};

const saveImage = async () => {
  try {
    await axiosInstance.post('/trips/save_image/', {
      trip_id: tripId,
      image_url: resultImageUrl.value
    });
  } catch (error) {
    console.error('saveImage 실패: ', error);
  } finally {
    await Promise.all([
      tripStore.getTrip(tripId),
    ]);
    saveImageFlag.value = true
    console.log('Image 저장 완료')
  }
}
</script>

<style scoped>
.main-container {
  width: 100%;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  text-align: center;
  margin: 10px auto;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
  background-color: #ffffff !important;
  /* border: 1px solid black; */
}

.pick {
  width: 90%;
  margin: 20px auto 0px auto;
  padding: 10px 10px;
  /* border: 1px solid blue; */
}

.create {
  width: 90%;
  text-align: center;
  margin: 0 auto;
  padding: 10px 0;
  /* border: 1px solid green; */
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
  font-weight: 500;
  text-align: center;
}

img {
  max-width: 100%;
  height: auto;
}

.create-text {
  font-size: large !important;
  font-weight: bold;
}

/* 파일 업로드 */
.file-container {
  display: inline-block;
  width: 90%;
}

.file-input {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f5f5f5;
  position: relative;
}

.file-input input[type="file"] {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
}

.file-input span {
  flex: 1;
  margin-right: 10px;
}

.upload-icon {
  color: #888;
}
</style>
