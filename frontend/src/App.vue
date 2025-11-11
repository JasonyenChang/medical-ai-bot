<template>
  <div class="p-8 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">家庭醫師</h1>

    <input type="text" placeholder="輸入你的疑難雜症"
      class="w-3/4 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder:text-gray-400"
      v-model="inputQuestion" />

    <button @click="askDoctor"
      class="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700 transition cursor-pointer ml-2">
      問醫生
    </button>
    <div class="py-4">
      {{ doctorAnswer }}
    </div>

    <!-- 載入中提示 -->
    <div v-if="loading" class="mt-4 text-gray-500">載入中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { askDoctorQuestionStream } from "./api";

const loading = ref(false);

const doctorAnswer = ref<string>("");
const inputQuestion = ref("");

async function askDoctor() {
  if (!inputQuestion.value.trim()) return;

  loading.value = true;
  doctorAnswer.value = "";

  try {
    await askDoctorQuestionStream(inputQuestion.value, async (chunk) => {
      loading.value = false;
      doctorAnswer.value += chunk; // ✅ 每段即時追加
    });
  } catch (error) {
    console.error("API error:", error);
  } finally {
    inputQuestion.value = "";
  }
}

</script>
