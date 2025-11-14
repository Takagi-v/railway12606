<template>
  <a-layout-footer class="app-footer">
    <div class="footer-content">
      <p>© 2025 中国铁路12306 课程项目</p>
      <p class="footer-links">
        <a href="#">关于我们</a>
        <a-divider type="vertical" />
        <a href="#">联系方式</a>
        <a-divider type="vertical" />
        <a href="#">帮助中心</a>
      </p>
    </div>
  </a-layout-footer>
</template>

<style scoped>
.app-footer {
  background: #f0f2f5;
  text-align: center;
  padding: 24px 50px;
  color: rgba(0, 0, 0, 0.45);
}

.footer-content p {
  margin: 5px 0;
}

.footer-links a {
  color: rgba(0, 0, 0, 0.45);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #1890ff;
}
</style>
