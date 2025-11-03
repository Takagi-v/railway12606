<template>
  <a-layout class="register-layout">
    <app-header />
    <a-layout-content class="register-content">
      <a-card class="register-card" title="用户注册">
        <a-form :model="registerForm" :rules="rules" @finish="handleRegister" layout="vertical">
          <a-form-item label="用户类型" name="user_type">
            <a-radio-group v-model:value="registerForm.user_type">
              <a-radio value="成人">成人</a-radio>
              <a-radio value="学生">学生</a-radio>
            </a-radio-group>
          </a-form-item>

          <a-form-item label="登录名" name="username">
            <a-input v-model:value="registerForm.username" placeholder="6-30位字母或数字" />
          </a-form-item>

          <a-form-item label="真实姓名" name="real_name">
            <a-input v-model:value="registerForm.real_name" placeholder="请输入真实姓名" />
          </a-form-item>

          <a-form-item label="证件类型" name="id_type">
            <a-select v-model:value="registerForm.id_type">
              <a-select-option value="居民身份证">居民身份证</a-select-option>
              <a-select-option value="护照">护照</a-select-option>
            </a-select>
          </a-form-item>

          <a-form-item label="证件号码" name="id_number">
            <a-input v-model:value="registerForm.id_number" placeholder="请输入证件号码" />
          </a-form-item>

          <a-form-item label="手机号" name="phone">
            <a-input v-model:value="registerForm.phone" placeholder="请输入11位手机号" />
          </a-form-item>

          <a-form-item label="邮箱" name="email">
            <a-input v-model:value="registerForm.email" placeholder="请输入邮箱" />
          </a-form-item>

          <a-form-item label="密码" name="password">
            <a-input-password
              v-model:value="registerForm.password"
              placeholder="6-20位，包含字母和数字"
            />
          </a-form-item>

          <a-form-item label="确认密码" name="confirmPassword">
            <a-input-password
              v-model:value="registerForm.confirmPassword"
              placeholder="请再次输入密码"
            />
          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" size="large" block :loading="loading">
              注册
            </a-button>
          </a-form-item>

          <div class="register-footer">
            <span>已有账号？</span>
            <a-button type="link" @click="router.push('/login')">立即登录</a-button>
          </div>
        </a-form>
      </a-card>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const router = useRouter()
const userStore = useUserStore()

const registerForm = ref({
  username: '',
  real_name: '',
  id_type: '居民身份证',
  id_number: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
  user_type: '成人'
})

const loading = ref(false)

const validateConfirmPassword = (rule, value) => {
  if (value !== registerForm.value.password) {
    return Promise.reject('两次密码输入不一致')
  }
  return Promise.resolve()
}

const rules = {
  username: [
    { required: true, message: '请输入用户名' },
    { pattern: /^[a-zA-Z0-9]{6,30}$/, message: '用户名为6-30位字母或数字' }
  ],
  realName: [{ required: true, message: '请输入真实姓名' }],
  idType: [{ required: true, message: '请选择证件类型' }],
  idNumber: [{ required: true, message: '请输入证件号码' }],
  phone: [
    { required: true, message: '请输入手机号' },
    { pattern: /^1\d{10}$/, message: '请输入有效的手机号' }
  ],
  email: [
    { required: true, message: '请输入邮箱' },
    { type: 'email', message: '请输入有效的邮箱地址' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*\d).{6,20}$/, message: '密码需6-20位，且包含字母和数字' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码' },
    { validator: validateConfirmPassword }
  ],
  userType: [{ required: true, message: '请选择用户类型' }]
}

const handleRegister = async () => {
  loading.value = true
  try {
    const { confirmPassword, ...data } = registerForm.value
    await userStore.register(data)

    message.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    message.error(error.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-layout {
  min-height: 100vh;
}

.register-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 64px - 70px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 50px 20px;
}

.register-card {
  width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.register-footer {
  text-align: center;
  margin-top: 16px;
}
</style>
