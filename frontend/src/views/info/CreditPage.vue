<template>
  <div class="info-page">
    <div class="container">
      <h1>信用信息</h1>
      <div class="info-content">
        <div class="credit-section">
          <h2>铁路旅客信用信息记录管理办法</h2>
          <div class="credit-content">
            <p>
              为加强铁路旅客信用信息管理，推进社会信用体系建设，根据国家有关法律法规，制定本办法。
            </p>

            <h3>第一条 适用范围</h3>
            <p>
              本办法适用于在中华人民共和国境内铁路旅客运输过程中发生的信用信息记录、归集、共享、公开、使用等管理活动。
            </p>

            <h3>第二条 信用信息分类</h3>
            <p>
              铁路旅客信用信息包括身份信息、购票信息、乘车信息等基本信息，以及严重失信行为信息。
            </p>

            <h3>第三条 严重失信行为</h3>
            <ul>
              <li>扰乱铁路站车运输秩序且危及铁路安全、造成严重社会不良影响的</li>
              <li>在动车组列车上吸烟或者在其他列车的禁烟区域吸烟的</li>
              <li>查处的倒卖车票、制贩假票的</li>
              <li>冒用优惠（待）身份证件、使用伪造或无效优惠（待）身份证件购票乘车的</li>
              <li>持伪造、过期等无效车票或冒用挂失补车票乘车的</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

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

.credit-section h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 24px;
}

.credit-section h3 {
  color: #34495e;
  margin: 25px 0 15px 0;
  font-size: 18px;
}

.credit-content p {
  color: #666;
  line-height: 1.8;
  margin-bottom: 15px;
}

.credit-content ul {
  color: #666;
  line-height: 1.8;
  padding-left: 20px;
}

.credit-content li {
  margin-bottom: 8px;
}
</style>
