<template>
  <div class="service-page">
    <div class="container">
      <h1>铁路畅行</h1>
      <div class="service-content">
        <p>铁路畅行会员服务，享受更多出行便利。</p>
        <div class="coming-soon">
          <h2>功能开发中...</h2>
          <p>该功能正在开发中，敬请期待。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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

.coming-soon {
  text-align: center;
  padding: 60px 20px;
}

.coming-soon h2 {
  color: #3498db;
  margin-bottom: 20px;
}

.coming-soon p {
  color: #666;
  font-size: 16px;
}
</style>