<template>
  <div class="schedule-page">
    <div class="container">
      <h1>时刻表查询</h1>
      <div class="search-form">
        <div class="form-row">
          <div class="form-group">
            <label>车次号：</label>
            <input type="text" v-model="trainNumber" placeholder="请输入车次号" />
          </div>
          <div class="form-group">
            <label>出发站：</label>
            <input type="text" v-model="departureStation" placeholder="请输入出发站" />
          </div>
          <div class="form-group">
            <label>到达站：</label>
            <input type="text" v-model="arrivalStation" placeholder="请输入到达站" />
          </div>
        </div>
        <button @click="handleSearch" class="search-btn">查询时刻表</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const trainNumber = ref('')
const departureStation = ref('')
const arrivalStation = ref('')

const handleSearch = () => {
  console.log('查询时刻表:', {
    trainNumber: trainNumber.value,
    departureStation: departureStation.value,
    arrivalStation: arrivalStation.value
  })
  // 这里可以添加时刻表查询逻辑
}
</script>

<style scoped>
.schedule-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 50px 0;
}

.container {
  max-width: 800px;
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

.search-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
}

.form-group input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.search-btn {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
  align-self: center;
}

.search-btn:hover {
  background: #2980b9;
}
</style>
