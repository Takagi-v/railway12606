<template>
  <a-layout-header class="app-header">
    <div class="header-content">
      <div class="logo" @click="router.push('/')">
        <span class="logo-text">中国铁路12306</span>
      </div>

      <div class="nav-menu">
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
                  <UserOutlined /> 个人中心
                </a-menu-item>
                <a-menu-item @click="router.push('/user/passengers')">
                  <TeamOutlined /> 乘客管理
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="handleLogout">
                  <LogoutOutlined /> 退出登录
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
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 999;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 20px;
}

.logo {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}

.nav-menu {
  flex: 1;
  margin-left: 50px;
}

.header-menu {
  border-bottom: none;
  line-height: 64px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-button {
  height: 40px;
}
</style>
