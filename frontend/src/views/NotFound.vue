<template>
  <a-layout class="not-found-layout">
    <app-header />
    <a-layout-content class="not-found-content">
      <a-result
        status="404"
        title="404"
        sub-title="抱歉，您访问的页面不存在"
      >
        <template #extra>
          <a-button type="primary" @click="router.push('/')">
            返回首页
          </a-button>
        </template>
      </a-result>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const router = useRouter()
</script>

<style scoped>
.not-found-layout {
  min-height: 100vh;
}

.not-found-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 64px - 70px);
  background: #f0f2f5;
}
</style>

