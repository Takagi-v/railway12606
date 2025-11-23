<template>
  <div class="info-page">
    <div class="container">
      <h1>公告信息</h1>
      <div class="info-content">
        <div class="announcement-list">
          <div class="announcement-item" v-for="item in announcements" :key="item.id">
            <div class="announcement-date">{{ item.date }}</div>
            <div class="announcement-title">{{ item.title }}</div>
            <div class="announcement-summary">{{ item.summary }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const announcements = ref([
  {
    id: 1,
    date: '2024-01-15',
    title: '关于春运期间车票预售期调整的公告',
    summary: '为方便旅客出行，春运期间车票预售期将调整为30天...'
  },
  {
    id: 2,
    date: '2024-01-10',
    title: '铁路12306网站系统维护通知',
    summary: '为提升系统服务质量，将于1月20日进行系统维护...'
  },
  {
    id: 3,
    date: '2024-01-05',
    title: '新增高铁线路开通公告',
    summary: '京沪高铁新增多个站点，为旅客提供更便捷的出行选择...'
  }
])
</script>

<style scoped>
.info-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 50px 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.announcement-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.announcement-item {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}

.announcement-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.announcement-date {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.announcement-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

.announcement-summary {
  color: #666;
  line-height: 1.6;
}
</style>
