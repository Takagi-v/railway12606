<template>
  <div class="user-layout">
    <Header12306 />
    <div class="user-content">
      <div class="wrapper">
        <div class="breadcrumb">
          当前位置：
          <a
            href="javascript:;"
            class="crumb-link"
            @click.prevent="go('/user/profile?section=view')"
          >
            个人中心
          </a>
          <span v-if="breadcrumb.group" class="crumb-sep">&gt;</span>
          <span v-if="breadcrumb.group" class="crumb-text">{{ breadcrumb.group }}</span>
          <span v-if="breadcrumb.item" class="crumb-sep">&gt;</span>
          <span v-if="breadcrumb.item" class="crumb-text">{{ breadcrumb.item }}</span>
        </div>
        <div class="center-box">
          <CenterMenu context="service" @heightChange="onMenuHeightChange" />
          <div class="center-main" ref="mainRef">
            <h1 class="rp-title">功能开发中</h1>
            <div class="rp-body">
              <h2 class="rp-sub">功能开发中...</h2>
              <p class="rp-text">该功能正在开发中，敬请期待。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <LoginFooter />
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import Header12306 from '@/components/Header12306.vue'
import LoginFooter from '@/components/LoginFooter.vue'
import CenterMenu from '@/components/CenterMenu.vue'

const router = useRouter()
const route = useRoute()
const go = path => {
  if (path.includes('/user/profile')) {
    router.push({ path: '/user/profile', query: { section: 'view' } })
    return
  }
  router.push(path)
}
const mainRef = ref(null)
const onMenuHeightChange = h => {
  const base = 600
  const el = mainRef.value
  if (!el) return
  el.style.minHeight = Math.max(h, base) + 'px'
}

const breadcrumb = computed(() => {
  const p = route.path || ''
  const q = route.query || {}
  if (p === '/service/railway-pass' && q.menu) {
    return { group: '订单中心', item: String(q.menu || '') }
  }
  if (p === '/service/railway-pass' && q.group) {
    return { group: String(q.group || ''), item: '' }
  }
  if (p.startsWith('/user/orders')) return { group: '订单中心', item: '火车票订单' }
  if (p.startsWith('/user/passengers')) return { group: '常用信息管理', item: '乘车人' }
  if (p.startsWith('/user/profile')) return { group: '个人信息', item: '查看个人信息' }
  return { group: '', item: '' }
})

onMounted(() => {
  window.addEventListener('resize', () =>
    onMenuHeightChange(mainRef.value ? mainRef.value.offsetHeight : 600)
  )
})
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
}
.wrapper {
  width: 1200px;
  margin: 0 auto;
}
.user-content {
  background: #f7f8fa;
  padding: 16px 0 40px;
}
.breadcrumb {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
}
.breadcrumb .crumb-link {
  color: #666;
  text-decoration: none;
}
.breadcrumb .crumb-sep {
  margin: 0 6px;
  color: #999;
}
.breadcrumb .crumb-text {
  color: #333;
}
.center-box {
  display: flex;
  align-items: flex-start;
  width: 1190px;
  gap: 30px;
}
.center-main {
  flex: 1;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  min-height: 600px;
  padding: 16px;
}
.rp-title {
  margin: 0 0 10px;
  font-size: 20px;
  color: #2c3e50;
}
.rp-sub {
  margin: 12px 0 8px;
  font-size: 16px;
  color: #3498db;
}
.rp-text {
  color: #666;
  font-size: 14px;
}
</style>
