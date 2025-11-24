<template>
  <div class="admin-layout">
    <!-- 管理员导航栏 -->
    <nav class="admin-nav">
      <div class="nav-brand">
        <h2>管理员控制台</h2>
      </div>
      <div class="nav-links">
        <router-link to="/admin/dashboard" class="nav-link">
          <i class="icon-dashboard"></i>
          仪表板
        </router-link>
        <router-link to="/admin/users" class="nav-link">
          <i class="icon-users"></i>
          用户管理
        </router-link>
        <router-link to="/admin/roles" class="nav-link">
          <i class="icon-roles"></i>
          角色管理
        </router-link>
        <router-link to="/admin/permissions" class="nav-link">
          <i class="icon-permissions"></i>
          权限管理
        </router-link>
        <router-link to="/admin/trains" class="nav-link">
          <i class="icon-train"></i>
          车次管理
        </router-link>
        <router-link to="/admin/orders" class="nav-link">
          <i class="icon-orders"></i>
          订单管理
        </router-link>
        <router-link to="/admin/system" class="nav-link">
          <i class="icon-settings"></i>
          系统设置
        </router-link>
      </div>
      <div class="nav-user">
        <span>{{ userStore.user?.real_name || '管理员' }}</span>
        <button class="logout-btn" @click="logout">退出</button>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.admin-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-brand h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 2rem;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.admin-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* 图标样式 */
.nav-link i {
  width: 16px;
  height: 16px;
}

.icon-dashboard::before {
  content: '📊';
}
.icon-users::before {
  content: '👥';
}
.icon-roles::before {
  content: '🎭';
}
.icon-permissions::before {
  content: '🔐';
}
.icon-train::before {
  content: '🚄';
}
.icon-orders::before {
  content: '📋';
}
.icon-settings::before {
  content: '⚙️';
}

@media (max-width: 768px) {
  .admin-nav {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .admin-main {
    padding: 1rem;
  }
}
</style>
