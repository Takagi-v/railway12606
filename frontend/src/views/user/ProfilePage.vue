<template>
  <div class="profile-page">
    <!-- 欢迎语块 -->
    <div class="welcome-card">
      <div class="welcome-left">
        <div class="welcome-title">
          <strong>{{ displayName }}</strong>
          {{ greetingSuffix }}
        </div>
        <p class="welcome-desc">欢迎您登录中国铁路客户服务中心网站。</p>
        <p class="welcome-desc">如果您的密码在其他网站也使用，建议您修改本网站密码。</p>
      </div>
      <div class="welcome-right">
        <div class="security">
          <div class="security-title">账户安全</div>
          <ul class="security-list">
            <li>
              <span class="label">手机核验</span>
              <span class="status">已绑定</span>
            </li>
            <li>
              <span class="label">邮箱绑定</span>
              <span class="status">未绑定</span>
            </li>
            <li>
              <span class="label">安全等级</span>
              <span class="status level">中</span>
            </li>
          </ul>
          <div class="security-actions">
            <a href="javascript:;" @click.prevent="go('/user/profile?section=security')">
              账号安全
            </a>
            <a href="javascript:;" @click.prevent="go('/user/profile?section=phone')">手机核验</a>
          </div>
        </div>
      </div>
    </div>

    <!-- 常用入口（与官网风格对齐） -->
    <div class="quick-links">
      <a href="javascript:;" @click.prevent="go('/user/orders')" class="q-item">
        <span class="q-icon"></span>
        火车票订单
      </a>
      <a href="javascript:;" @click.prevent="go('/user/passengers')" class="q-item">
        <span class="q-icon"></span>
        乘车人
      </a>
      <a href="javascript:;" @click.prevent="go('/ticket/schedule')" class="q-item">
        <span class="q-icon"></span>
        时刻表
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = useRouter()
const go = path => router.push(path)

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const displayName = computed(() => {
  const u = user.value || {}
  return u.nickname || u.username || u.name || '用户'
})
const greetingSuffix = computed(() => {
  const h = new Date().getHours()
  if (h < 11) return '先生,上午好！'
  if (h < 13) return '先生,中午好！'
  if (h < 18) return '先生,下午好！'
  return '先生,晚上好！'
})
</script>

<style scoped>
.profile-page {
  padding: 8px;
}

.welcome-card {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  padding: 16px;
}
.welcome-title {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}
.welcome-desc {
  margin: 4px 0;
  color: #666;
}

.security {
  border-left: 1px dashed #eee;
  padding-left: 16px;
}
.security-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}
.security-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.security-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  color: #666;
}
.security-list .status {
  color: #2e64fe;
}
.security-list .level {
  color: #ff7a00;
}
.security-actions {
  margin-top: 8px;
}
.security-actions a {
  color: #2e64fe;
  text-decoration: none;
  margin-right: 12px;
}
.security-actions a:hover {
  text-decoration: underline;
}

.quick-links {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
.q-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  color: #333;
  text-decoration: none;
}
.q-item:hover {
  border-color: #d0d7de;
}
.q-icon {
  width: 18px;
  height: 18px;
  background: url('https://www.12306.cn/index/images/logo.png') center/contain no-repeat;
}
</style>
