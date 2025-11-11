<template>
  <div class="p-8 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">熱門商品</h1>

    <!-- 載入資料按鈕 -->
    <button @click="loadData"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition cursor-pointer">
      載入資料
    </button>

    <!-- 載入中提示 -->
    <div v-if="loading" class="mt-4 text-gray-500">載入中...</div>

    <!-- 表格內容 -->
    <div v-if="!loading && products.length" class="mt-6">
      <table class="w-full border-collapse border border-gray-200 text-sm">
        <thead class="bg-gray-100 text-left text-gray-700">
          <tr>
            <th class="p-3 w-16 text-center">#</th>
            <th class="p-3">商品名稱</th>
            <th class="p-3 w-32">分類</th>
            <th class="p-3 w-32 text-right">銷售量</th>
            <th class="p-3 w-32 text-right">成長率</th>
            <th class="p-3 w-32 text-center">庫存狀態</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in products" :key="item.id" class="border-t hover:bg-gray-50 transition">
            <td class="p-3 text-center font-medium text-gray-600">{{ index + 1 }}</td>
            <td class="p-3 font-semibold text-gray-800">{{ item.name }}</td>
            <td class="p-3 text-gray-600">{{ item.category }}</td>
            <td class="p-3 text-right text-gray-800">{{ item.sales }}</td>
            <td class="p-3 text-right font-semibold" :class="item.growth >= 0 ? 'text-green-600' : 'text-red-600'">{{
              item.growth > 0 ? '+' : '' }}{{ item.growth }}%</td>
            <td class="p-3 text-center">
              <span class="px-2 py-1 rounded text-xs font-semibold text-white" :class="{
                'bg-green-600': item.stock === 'normal',
                'bg-yellow-500': item.stock === 'low',
                'bg-red-600': item.stock === 'out'
              }">
                {{ stockText(item.stock) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getTrendingProducts } from "./api";

interface Product {
  id: number;
  name: string;
  category: string;
  sales: number;
  growth: number;
  stock: string;
}

function stockText(status: string) {
  switch (status) {
    case "normal":
      return "正常";
    case "low":
      return "低庫存";
    case "out":
      return "缺貨";
    default:
      return "未知";
  }
}

const products = ref<Product[]>([]);
const loading = ref(false);

async function loadData() {
  loading.value = true;
  try {
    products.value = await getTrendingProducts();
  } catch (error) {
    console.error("API error:", error);
  } finally {
    loading.value = false;
  }
}

onMounted(loadData)
</script>
