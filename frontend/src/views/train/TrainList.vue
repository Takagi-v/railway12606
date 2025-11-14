<template>
  <a-layout class="train-list-layout">
    <app-header />
    <a-layout-content class="train-list-content">
      <div class="content-wrapper">
        <a-card class="search-info" :bordered="false">
          <div class="search-summary">
            <span class="route"
              >{{ query.departure_city }} → {{ query.arrival_city }}</span
            >
            <span class="date">{{ query.travel_date }}</span>
            <a-button type="link" @click="router.push('/')">修改查询</a-button>
          </div>
        </a-card>

        <a-card class="train-list-card">
          <a-empty
            v-if="!loading && trains.length === 0"
            description="暂无车次数据，请稍后再试"
          >
            <a-button type="primary" @click="router.push('/')"
              >返回首页</a-button
            >
          </a-empty>

          <a-spin :spinning="loading">
            <div v-if="trains.length === 0 && loading" class="placeholder-text">
              加载中...
            </div>
            <div v-else-if="trains.length === 0" class="placeholder-text">
              TODO: 车次查询功能待实现
              <br />
              请先在后端实现车次查询接口
            </div>
          </a-spin>
        </a-card>
      </div>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";

const router = useRouter();
const route = useRoute();

const query = ref(route.query);
const trains = ref([]);
const loading = ref(false);

onMounted(() => {
  // TODO: Fetch train data
  console.log("Search params:", query.value);
});
</script>

<style scoped>
.train-list-layout {
  min-height: 100vh;
}

.train-list-content {
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
  padding: 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.search-info {
  margin-bottom: 20px;
}

.search-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 16px;
}

.route {
  font-weight: bold;
  font-size: 18px;
}

.train-list-card {
  min-height: 400px;
}

.placeholder-text {
  text-align: center;
  padding: 100px 20px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 16px;
  line-height: 2;
}
</style>
