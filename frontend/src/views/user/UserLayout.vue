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
            @click.prevent="go('/user/profile?group=个人中心')"
          >
            个人中心
          </a>
          <span v-if="breadcrumb.group" class="crumb-sep">&gt;</span>
          <span v-if="breadcrumb.group" class="crumb-text">{{ breadcrumb.group }}</span>
          <span v-if="breadcrumb.item" class="crumb-sep">&gt;</span>
          <span v-if="breadcrumb.item" class="crumb-text">{{ breadcrumb.item }}</span>
        </div>

        <div class="center-box">
          <CenterMenu context="user" @heightChange="onMenuHeightChange" />
          <div class="center-main" ref="mainRef">
            <router-view />
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
const go = path => router.push(path)
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
  if (q.group) return { group: String(q.group || ''), item: '' }
  if (p.startsWith('/user/orders')) return { group: '订单中心', item: '火车票订单' }
  if (p.startsWith('/user/passengers')) {
    const tab = String(q.tab || '')
    return { group: '常用信息管理', item: tab === 'address' ? '地址管理' : '乘车人' }
  }
  if (p.startsWith('/user/profile')) {
    const section = String(q.section || '')
    const itemLabel =
      section === 'security'
        ? '账号安全'
        : section === 'phone'
          ? '手机核验'
          : section === 'close'
            ? '账号注销'
            : '查看个人信息'
    return { group: '个人信息', item: itemLabel }
  }
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
.breadcrumb .current {
  color: #333;
}
.breadcrumb .crumb-link {
  color: #666;
  text-decoration: none;
}
.breadcrumb .crumb-link:hover {
  text-decoration: underline;
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

.ucenter-nav {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  padding: 12px 16px;
}
.nav-group .nav-title {
  font-size: 14px;
  color: #333;
  margin: 0 0 8px;
}
.nav-sub {
  list-style: none;
  padding: 0;
  margin: 0;
}
.nav-sub li a {
  display: inline-block;
  color: var(--primary-color);
  text-decoration: none;
  padding: 2px 0;
}
.nav-sub li a:hover {
  text-decoration: underline;
}

.ucenter-content {
  margin-top: 16px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  min-height: 600px;
  padding: 16px;
}
</style>
