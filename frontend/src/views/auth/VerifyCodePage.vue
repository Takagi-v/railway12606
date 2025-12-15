<template>
  <div class="verify-page">
    <Header12306 />

    <div class="main-content">
      <div class="forgot-container">
        <div class="tab-navigation">
          <div class="tab-item" :class="{ active: type === 'face' }">人脸找回</div>
          <div class="tab-item" :class="{ active: type === 'phone' }">手机找回</div>
          <div class="tab-item" :class="{ active: type === 'email' }">邮箱找回</div>
        </div>

        <div class="tab-content">
          <div class="step-indicator">
            <div class="step completed">
              <div class="step-number">1</div>
              <div class="step-text">提交身份信息</div>
            </div>
            <div class="step-line"></div>
            <div class="step active">
              <div class="step-number">2</div>
              <div class="step-text">验证验证码</div>
            </div>
            <div class="step-line"></div>
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-text">设置新密码</div>
            </div>
            <div class="step-line"></div>
            <div class="step">
              <div class="step-number">4</div>
              <div class="step-text">完成</div>
            </div>
          </div>

          <div class="form-content">
            <a-form layout="vertical" class="recovery-form">
              <a-form-item label="验证码：" required>
                <div class="verify-code-input-group">
                  <a-input v-model:value="code" :placeholder="placeholderText" size="large" />
                  <a-button 
                    size="large" 
                    :disabled="!canResend" 
                    @click="handleResend"
                    class="resend-btn"
                  >
                    {{ canResend ? '获取验证码' : `${countdown}s后重发` }}
                  </a-button>
                </div>
              </a-form-item>
              <div class="form-actions">
                <a-button
                  type="primary"
                  size="large"
                  class="submit-btn"
                  :loading="loading"
                  @click="submitVerify"
                >
                  验证
                </a-button>
              </div>
              <div class="help-text">
                <a href="#" class="help-link" @click.prevent="goBack">返回上一步</a>
              </div>
            </a-form>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { verifyRecoveryCode, resendRecoveryCode } from '@/api/auth'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'

const router = useRouter()
const route = useRoute()

const type = route.query.type || 'phone'
const token = route.query.token || ''
const loading = ref(false)
const code = ref('')

const countdown = ref(60)
const canResend = ref(false)
let timer = null

const placeholderText =
  type === 'email' ? '请输入邮箱验证码' : type === 'face' ? '请输入APP验证码' : '请输入短信验证码'

const startCountdown = () => {
  canResend.value = false
  countdown.value = 60
  if (timer) clearInterval(timer)
  timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      canResend.value = true
    }
  }, 1000)
}

onMounted(() => {
  startCountdown()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const handleResend = async () => {
  if (!token) {
    message.error('参数错误，请重新开始流程')
    return
  }
  try {
    const res = await resendRecoveryCode({ token })
    if (res.code === 200) {
      message.success('验证码已重新发送')
      startCountdown()
    } else {
      message.error(res.message || '发送失败')
    }
  } catch (e) {
    message.error('发送失败，请稍后重试')
  }
}

const submitVerify = async () => {
  if (!code.value) {
    message.error('请输入验证码')
    return
  }
  // 若携带token则调用后台验证
  loading.value = true
  try {
    if (token) {
      const res = await verifyRecoveryCode({ token, verificationCode: code.value, type })
      if (res.code === 200) {
        message.success('验证码验证成功')
        router.replace({ path: '/forgot-password/new-password', query: { type, token } })
      } else {
        message.error(res.message || '验证失败')
      }
    } else {
      // 无token时走纯前端占位跳转
      message.success('已提交验证码（占位符）')
      router.replace({ path: '/forgot-password/new-password', query: { type } })
    }
  } catch (e) {
    message.error('验证失败，请重试')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.replace({ path: '/forgot-password', query: { type, step: 1 } })
}
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  background: #ffffff;
  position: relative;
  overflow: hidden;
}
.main-content {
  padding: 28px 20px;
  height: 650px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: relative;
  z-index: 1;
}
.forgot-container {
  background: white;
  border-radius: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 980px;
  overflow: hidden;
}
.tab-navigation {
  display: flex;
  background: #298cce;
}
.tab-item {
  flex: 1;
  padding: 0 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 60px;
  font-size: 14px;
  color: #fff;
  background: transparent;
}
.tab-item:hover {
  background: #3fa2d8;
}
.tab-item.active {
  color: #ffffff;
  background: #66c8e8;
}
.tab-content {
  padding: 36px;
  height: 450px;
  overflow-y: auto;
}
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 28px;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f0f0f0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s;
}
.step.active .step-number {
  background: #298cce;
  color: #fff;
}
.step.completed .step-number {
  background: #52c41a;
  color: #fff;
}
.step-text {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}
.step-line {
  flex: 1;
  height: 2px;
  background: #e6e6e6;
  margin: 0 10px;
}
.form-content {
  max-width: 640px;
  margin: 0 auto;
}
.recovery-form {
  margin-bottom: 20px;
}
.verify-code-input-group {
  display: flex;
  gap: 12px;
}
.resend-btn {
  width: 140px;
  flex-shrink: 0;
}
.form-actions {
  margin-top: 18px;
  text-align: center;
}
.submit-btn {
  width: 100%;
  height: 40px;
  font-size: 15px;
  border-radius: 6px;
  background: #ff7a00;
  border: none;
  color: white;
  font-weight: 500;
}
.help-text {
  text-align: center;
  font-size: 14px;
  color: #666;
}
.help-link {
  color: #1890ff;
  text-decoration: none;
  transition: color 0.3s;
}
.help-link:hover {
  color: #40a9ff;
  text-decoration: underline;
}
</style>
