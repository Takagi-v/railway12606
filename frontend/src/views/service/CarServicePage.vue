<template>
  <div class="service-page">
    <div class="container">
      <h1>约车服务</h1>
      <div class="service-content">
        <p>为您提供便捷的接送站约车服务。</p>
        <div class="service-form">
          <div class="form-group">
            <label>出发地：</label>
            <input type="text" placeholder="请输入出发地址" />
          </div>
          <div class="form-group">
            <label>目的地：</label>
            <input type="text" placeholder="请输入目的地址" />
          </div>
          <div class="form-group">
            <label>预约时间：</label>
            <input type="datetime-local" />
          </div>
          <button class="submit-btn">预约约车</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 页面逻辑
</script>

<style scoped>
.service-page {
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
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.service-content p {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
}

.service-form {
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

.submit-btn {
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

.submit-btn:hover {
  background: #2980b9;
}
</style>