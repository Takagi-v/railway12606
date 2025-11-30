<template>
  <div class="done-page">
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">🚄</div>
          <span class="logo-text">中国铁路12306</span>
          <span class="subtitle">12306 CHINA RAILWAY</span>
        </div>
      </div>
    </div>
    <div class="main-content">
      <div class="forgot-container">
        <div class="tab-navigation">
          <div class="tab-item" :class="{ active: type === 'face' }">人脸找回</div>
          <div class="tab-item" :class="{ active: type === 'phone' }">手机找回</div>
          <div class="tab-item" :class="{ active: type === 'email' }">邮箱找回</div>
        </div>
        <div class="tab-content">
          <div class="step-indicator">
            <div class="step completed"><div class="step-number">1</div><div class="step-text">提交身份信息</div></div>
            <div class="step-line"></div>
            <div class="step completed"><div class="step-number">2</div><div class="step-text">验证验证码</div></div>
            <div class="step-line"></div>
            <div class="step completed"><div class="step-number">3</div><div class="step-text">设置新密码</div></div>
            <div class="step-line"></div>
            <div class="step active"><div class="step-number">4</div><div class="step-text">完成</div></div>
          </div>
          <div class="qr-content">
            <h3 class="recovery-title">密码重置成功</h3>
            <p class="recovery-subtitle">即将跳转到登录页面，请使用新密码登录</p>
            <div class="form-actions">
              <a-button type="primary" size="large" class="submit-btn" @click="toLogin">前往登录</a-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()
const route = useRoute()
const type = route.query.type || 'phone'

const toLogin = () => { router.push('/login') }
onMounted(() => { setTimeout(() => toLogin(), 3000) })
</script>

<style scoped>
.done-page { min-height: 100vh; background: linear-gradient(135deg, #4a90e2 0%, #357abd 50%, #1e5f99 100%); position: relative; overflow: hidden; }
.header { background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 60px; display: flex; align-items: center; position: relative; z-index: 2; }
.header-content { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }
.logo { display: flex; align-items: center; gap: 8px; }
.logo-icon { width: 32px; height: 32px; background: #e60012; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px; }
.logo-text { font-size: 18px; font-weight: bold; color: #333; }
.subtitle { font-size: 12px; color: #666; margin-left: 5px; }
.main-content { padding: 50px 20px; display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 60px); position: relative; z-index: 1; }
.forgot-container { background: white; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); width: 100%; max-width: 800px; overflow: hidden; }
.tab-navigation { display: flex; border-bottom: 1px solid #e8e8e8; }
.tab-item { flex: 1; padding: 16px; text-align: center; font-size: 14px; color: #666; border-bottom: 2px solid transparent; }
.tab-item.active { color: #ff6600; border-bottom-color: #ff6600; }
.tab-content { padding: 40px; }
.step-indicator { display: flex; align-items: center; justify-content: center; margin-bottom: 40px; }
.step { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.step-number { width: 32px; height: 32px; border-radius: 50%; background: #f0f0f0; color: #999; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.step.active .step-number { background: #ff6600; color: #fff; }
.step.completed .step-number { background: #52c41a; color: #fff; }
.step-text { font-size: 12px; color: #666; white-space: nowrap; }
.step-line { width: 60px; height: 2px; background: #f0f0f0; margin: 0 10px; }
.qr-content { text-align: center; padding: 30px 20px; }
.recovery-title { font-size: 20px; font-weight: bold; color: #333; margin-bottom: 12px; }
.recovery-subtitle { font-size: 14px; color: #666; margin-bottom: 30px; line-height: 1.4; }
.form-actions { margin-top: 10px; display: flex; justify-content: center; }
.submit-btn { min-width: 140px; height: 44px; background: #ff6600; border: none; color: #fff; border-radius: 6px; }
</style>

