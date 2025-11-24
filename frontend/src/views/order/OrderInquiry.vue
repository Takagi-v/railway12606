<template>
  <div class="order-inquiry">
    <div class="container">
      <h1>订单查询</h1>
      <div class="inquiry-form">
        <div class="form-group">
          <label>订单号：</label>
          <input type="text" v-model="orderNumber" placeholder="请输入订单号" />
        </div>
        <div class="form-group">
          <label>手机号：</label>
          <input type="text" v-model="phoneNumber" placeholder="请输入手机号" />
        </div>
        <button @click="handleInquiry" class="inquiry-btn">查询订单</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const orderNumber = ref('')
const phoneNumber = ref('')

const handleInquiry = () => {
  console.log('查询订单:', orderNumber.value, phoneNumber.value)
  // 这里可以添加订单查询逻辑
}
</script>

<style scoped>
.order-inquiry {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 50px 0;
}

.container {
  max-width: 600px;
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

.inquiry-form {
  display: flex;
  flex-direction: column;
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

.inquiry-btn {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.inquiry-btn:hover {
  background: #2980b9;
}
</style>
