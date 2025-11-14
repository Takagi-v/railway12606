<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>管理员仪表板</h1>
      <p>欢迎回来，{{ userStore.user?.real_name || "管理员" }}！</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>用户总数</h3>
          <p class="stat-number">1,234</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🚄</div>
        <div class="stat-content">
          <h3>车次总数</h3>
          <p class="stat-number">56</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <h3>今日订单</h3>
          <p class="stat-number">89</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>今日收入</h3>
          <p class="stat-number">¥12,345</p>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="content-section">
        <h2>快速操作</h2>
        <div class="quick-actions">
          <router-link to="/admin/users" class="action-btn">
            <i class="icon">👥</i>
            <span>用户管理</span>
          </router-link>
          <router-link to="/admin/trains" class="action-btn">
            <i class="icon">🚄</i>
            <span>车次管理</span>
          </router-link>
          <router-link to="/admin/orders" class="action-btn">
            <i class="icon">📋</i>
            <span>订单管理</span>
          </router-link>
          <router-link to="/permission-test" class="action-btn">
            <i class="icon">🔐</i>
            <span>权限测试</span>
          </router-link>
        </div>
      </div>

      <div class="content-section">
        <h2>系统状态</h2>
        <div class="system-status">
          <div class="status-item">
            <span class="status-label">数据库连接</span>
            <span class="status-value online">正常</span>
          </div>
          <div class="status-item">
            <span class="status-label">缓存服务</span>
            <span class="status-value online">正常</span>
          </div>
          <div class="status-item">
            <span class="status-label">支付服务</span>
            <span class="status-value online">正常</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #666;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-content h3 {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-number {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.content-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.3rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-align: center;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
}

.action-btn .icon {
  font-size: 1.5rem;
}

.action-btn span {
  font-size: 0.9rem;
  font-weight: 500;
}

.system-status {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.status-label {
  color: #666;
  font-weight: 500;
}

.status-value {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-value.online {
  background: #d4edda;
  color: #155724;
}

@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
