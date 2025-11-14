<template>
  <a-layout-header class="app-header">
    <div class="header-content">
      <div class="logo" @click="router.push('/')">
        <span class="logo-text">中国铁路12306</span>
      </div>

      <div class="nav-menu">
<<<<<<< HEAD
        <a-menu mode="horizontal" :selected-keys="selectedKeys" class="header-menu">
          <a-menu-item key="home" @click="router.push('/')">首页</a-menu-item>
          <a-menu-item key="orders" @click="router.push('/user/orders')" v-if="isAuthenticated">
=======
        <a-menu
          mode="horizontal"
          :selected-keys="selectedKeys"
          class="header-menu"
        >
          <a-menu-item key="home" @click="router.push('/')"> 首页 </a-menu-item>
          <a-menu-item
            v-if="isAuthenticated"
            key="orders"
            @click="router.push('/user/orders')"
          >
>>>>>>> origin/feature/user-authentication
            我的订单
          </a-menu-item>
        </a-menu>
      </div>

      <div class="user-section">
        <template v-if="isAuthenticated">
          <a-dropdown>
            <a-button type="text" class="user-button">
              <UserOutlined />
              {{ user?.username || "用户" }}
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu>
                <a-menu-item @click="router.push('/user/profile')">
                  <UserOutlined />
                  个人中心
                </a-menu-item>
                <a-menu-item @click="router.push('/user/passengers')">
                  <TeamOutlined />
                  乘客管理
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="handleLogout">
                  <LogoutOutlined />
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </template>
        <template v-else>
          <a-button type="link" @click="router.push('/login')">登录</a-button>
          <a-button type="primary" @click="router.push('/register')"
            >注册</a-button
          >
        </template>
      </div>
    </div>
  </a-layout-header>
</template>

<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
import {
  UserOutlined,
  DownOutlined,
  TeamOutlined,
  LogoutOutlined,
} from "@ant-design/icons-vue";
import { message } from "ant-design-vue";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const isAuthenticated = computed(() => userStore.isAuthenticated);
const user = computed(() => userStore.user);

const selectedKeys = computed(() => {
  const path = route.path;
  if (path === "/") return ["home"];
  if (path.startsWith("/user/orders")) return ["orders"];
  return [];
});

const handleLogout = () => {
  userStore.logout();
  message.success("退出登录成功");
  router.push("/");
};
</script>

<style scoped>
.app-header {
  background: var(--primary-gradient);
  box-shadow: var(--shadow-medium);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 999;
  border-bottom: none;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 var(--spacing-lg);
}

.logo {
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: transform var(--transition-normal);
}

.logo:hover {
  transform: scale(1.05);
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-color-inverse);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.nav-menu {
  flex: 1;
  margin-left: var(--spacing-xxl);
}

.header-menu {
  border-bottom: none;
  line-height: 64px;
  background: transparent;
}

/* 重写Ant Design菜单样式以适配12306风格 */
.header-menu :deep(.ant-menu-item) {
  color: var(--text-color-inverse);
  border-bottom: 2px solid transparent;
  transition: all var(--transition-normal);
  font-weight: 500;
}

.header-menu :deep(.ant-menu-item:hover) {
  color: var(--text-color-inverse);
  border-bottom-color: rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.1);
}

.header-menu :deep(.ant-menu-item-selected) {
  color: var(--text-color-inverse);
  border-bottom-color: var(--text-color-inverse);
  background: rgba(255, 255, 255, 0.15);
}

.header-menu :deep(.ant-menu-item-selected::after) {
  border-bottom-color: var(--text-color-inverse);
}

.user-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.user-button {
  height: 40px;
  color: var(--text-color-inverse);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--border-radius-medium);
  transition: all var(--transition-normal);
}

.user-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  color: var(--text-color-inverse);
}

/* 登录注册按钮样式 */
.user-section :deep(.ant-btn-link) {
  color: var(--text-color-inverse);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--border-radius-medium);
  padding: 4px 16px;
  height: 32px;
  transition: all var(--transition-normal);
}

.user-section :deep(.ant-btn-link:hover) {
  color: var(--text-color-inverse);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.user-section :deep(.ant-btn-primary) {
  background: var(--accent-color);
  border-color: var(--accent-color);
  border-radius: var(--border-radius-medium);
  height: 32px;
  font-weight: 500;
  transition: all var(--transition-normal);
}

.user-section :deep(.ant-btn-primary:hover) {
  background: var(--accent-color-hover);
  border-color: var(--accent-color-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 102, 0, 0.3);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 var(--spacing-md);
  }
  
  .nav-menu {
    margin-left: var(--spacing-lg);
  }
  
  .logo-text {
    font-size: var(--font-size-lg);
  }
  
  .user-section {
    gap: var(--spacing-xs);
  }
}

@media (max-width: 576px) {
  .nav-menu {
    display: none;
  }
  
  .logo-text {
    font-size: var(--font-size-md);
  }
}
</style>
