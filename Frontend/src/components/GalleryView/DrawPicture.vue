<template>
  <div class="main-container">
    <div class="pick">
      <input type="file" @change="onFileChange" />
    </div>
    <div class="create">
      <button class="create-btn" @click="uploadImage">사진 생성</button>
    </div>

    <div v-if="loading">사진 생성 중</div>

    <div v-if="resultImageUrl">
      <v-img :src="resultImageUrl" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const selectedFile = ref(null);
const resultImageUrl = ref(null);

const loading = ref(false);

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadImage = async () => {
  // 이미지가 업로드 되지 않았을 경우
  if (!selectedFile.value) {
    alert("이미지가 업로드 되지 않았습니다.");
    return;
  }

  loading.value = true;
  resultImageUrl.value = null;

  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);
    formData.append("index", 0); // Vintage Comic

    const responsePost = await axios.post(
      "https://www.ailabapi.com/api/image/effects/ai-anime-generator",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          "ailabapi-api-key": import.meta.env.VITE_AILABAPI_API_KEY,
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
              "ailabapi-api-key": import.meta.env.VITE_AILABAPI_API_KEY,
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
  background-color: #ffffff;
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
</style>
