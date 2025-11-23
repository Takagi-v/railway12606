<template>
  <div class="login-form-container">
    <BaseForm
      :form-data="formData"
      :rules="loginRules"
      layout="vertical"
      :loading="loading"
      submit-text="登录"
      show-cancel
      cancel-text="重置"
      @submit="handleSubmit"
      @cancel="handleReset"
    >
      <template #form-items>
        <FormInput
          name="username"
          label="用户名/手机号"
          v-model:value="formData.username"
          placeholder="请输入用户名或手机号"
          prefix="user"
        />

        <FormInput
          name="password"
          label="密码"
          type="password"
          v-model:value="formData.password"
          placeholder="请输入密码"
          prefix="lock"
        />

        <FormInput
          name="captcha"
          label="验证码"
          v-model:value="formData.captcha"
          placeholder="请输入验证码"
          :maxlength="4"
          show-count
        >
          <template #addonAfter>
            <img :src="captchaUrl" alt="验证码" class="captcha-image" @click="refreshCaptcha" />
          </template>
        </FormInput>

        <a-form-item>
          <div class="login-options">
            <a href="#" class="forgot-password">忘记密码？</a>
          </div>
        </a-form-item>
      </template>
    </BaseForm>

    <div class="login-footer">
      <p>
        还没有账号？
        <a href="/register">立即注册</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { message } from 'ant-design-vue'
import BaseForm from '../BaseForm.vue'
import FormInput from '../FormInput.vue'
import { formRules } from '@/utils/formRules.js'

// 表单数据
const formData = reactive({
  username: '',
  password: '',
  captcha: ''
})

// 加载状态
const loading = ref(false)

// 验证码URL
const captchaUrl = ref(
  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmNWY1ZjUiLz48dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzMzMzMzMyIgdGV4dC1hbmNob3I9Im1pZGRsZSI+MTIzNDwvdGV4dD48L3N2Zz4='
)

// 验证规则
const loginRules = formRules.login

// 事件处理
const handleSubmit = async values => {
  loading.value = true
  try {
    console.log('登录数据:', values)
    // 这里应该调用登录API
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟API调用
    message.success('登录成功！')
  } catch (error) {
    message.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  Object.assign(formData, {
    username: '',
    password: '',
    captcha: ''
  })
  message.info('表单已重置')
}

const refreshCaptcha = () => {
  // 生成新的验证码（这里使用随机数字作为示例）
  const randomCode = Math.floor(1000 + Math.random() * 9000)
  const svgCode = `<svg width="100" height="40" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="40" fill="#f5f5f5"/><text x="50" y="25" font-family="Arial" font-size="16" fill="#333333" text-anchor="middle">${randomCode}</text></svg>`
  captchaUrl.value = `data:image/svg+xml;base64,${btoa(svgCode)}`
}
</script>

<style scoped>
.login-form-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 32px;
  background: white;
  border-radius: 8px;
  box-shadow: var(--box-shadow);
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.forgot-password {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

.captcha-image {
  width: 80px;
  height: 32px;
  cursor: pointer;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

.captcha-image:hover {
  opacity: 0.8;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.login-footer p {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.login-footer a {
  color: var(--color-primary);
  text-decoration: none;
}

.login-footer a:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-form-container {
    margin: 16px;
    padding: 24px 16px;
  }

  .login-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
