<template>
  <a-layout class="login-layout">
    <app-header />
    <a-layout-content class="login-content">
      <a-card class="login-card" title="用户登录">
        <a-form :model="loginForm" :rules="rules" @finish="handleLogin" layout="vertical">
          <a-form-item label="用户名/手机号" name="username">
            <a-input
              v-model:value="loginForm.username"
              placeholder="请输入用户名或手机号"
              size="large"
            >
              <template #prefix>
                <UserOutlined />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item label="密码" name="password">
            <a-input-password
              v-model:value="loginForm.password"
              placeholder="请输入密码"
              size="large"
            >
              <template #prefix>
                <LockOutlined />
              </template>
            </a-input-password>
          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" size="large" block :loading="loading">
              登录
            </a-button>
          </a-form-item>

          <div class="login-footer">
            <span>还没有账号？</span>
            <a-button type="link" @click="router.push('/register')">立即注册</a-button>
          </div>
        </a-form>
      </a-card>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loginForm = ref({
  username: '',
  password: ''
})

const loading = ref(false)

const rules = {
  username: [{ required: true, message: '请输入用户名或手机号' }],
  password: [{ required: true, message: '请输入密码' }]
}

const handleLogin = async () => {
  loading.value = true
  try {
    await userStore.login(loginForm.value)
    message.success('登录成功')

    // Redirect to original page or home
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (error) {
    message.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-layout {
  min-height: 100vh;
}

.login-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 64px - 70px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 50px 20px;
}

.login-card {
  width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.login-footer {
  text-align: center;
  margin-top: 16px;
}
</style>
