<template>
  <a-layout class="order-detail-layout">
    <app-header />
    <a-layout-content class="order-detail-content">
      <div class="content-wrapper">
        <a-card title="订单详情">
          <a-empty description="订单详情功能待实现">
            <a-button type="primary" @click="router.push('/user/orders')">返回订单列表</a-button>
          </a-empty>
        </a-card>
      </div>
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
.order-detail-layout {
  min-height: 100vh;
}

.order-detail-content {
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
  padding: 20px;
}

.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
}
</style>

