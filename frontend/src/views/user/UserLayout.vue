<template>
  <a-layout class="user-layout">
    <app-header />
    <a-layout-content class="user-content">
      <div class="content-wrapper">
        <a-layout>
          <a-layout-sider width="200" theme="light">
            <a-menu
              v-model:selected-keys="selectedKeys"
              mode="inline"
              style="height: 100%"
            >
              <a-menu-item key="profile" @click="router.push('/user/profile')">
                <UserOutlined /> 个人信息
              </a-menu-item>
              <a-menu-item key="passengers" @click="router.push('/user/passengers')">
                <TeamOutlined /> 乘客管理
              </a-menu-item>
              <a-menu-item key="orders" @click="router.push('/user/orders')">
                <FileTextOutlined /> 订单管理
              </a-menu-item>
            </a-menu>
          </a-layout-sider>
          <a-layout-content class="user-main-content">
            <router-view />
          </a-layout-content>
        </a-layout>
      </div>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { UserOutlined, TeamOutlined, FileTextOutlined } from '@ant-design/icons-vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const router = useRouter()
const route = useRoute()

const selectedKeys = ref(['profile'])

watch(
  () => route.path,
  (path) => {
    if (path.includes('/user/profile')) {
      selectedKeys.value = ['profile']
    } else if (path.includes('/user/passengers')) {
      selectedKeys.value = ['passengers']
    } else if (path.includes('/user/orders')) {
      selectedKeys.value = ['orders']
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
}

.user-content {
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
  padding: 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  min-height: 600px;
}

.user-main-content {
  padding: 24px;
  background: white;
}
</style>

