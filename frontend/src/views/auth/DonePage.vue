<template>
  <div class="done-page">
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
            <div class="step completed">
              <div class="step-number">2</div>
              <div class="step-text">验证验证码</div>
            </div>
            <div class="step-line"></div>
            <div class="step completed">
              <div class="step-number">3</div>
              <div class="step-text">设置新密码</div>
            </div>
            <div class="step-line"></div>
            <div class="step active">
              <div class="step-number">4</div>
              <div class="step-text">完成</div>
            </div>
          </div>
          <div class="qr-content">
            <h3 class="recovery-title">密码重置成功</h3>
            <p class="recovery-subtitle">即将跳转到登录页面，请使用新密码登录</p>
            <div class="form-actions">
              <a-button type="primary" size="large" class="submit-btn" @click="toLogin">
                前往登录
              </a-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { onMounted } from 'vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'

const router = useRouter()
const route = useRoute()
const type = route.query.type || 'phone'

const toLogin = () => {
  router.push('/login')
}
onMounted(() => {
  setTimeout(() => toLogin(), 3000)
})
</script>

<style scoped>
.done-page {
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
.qr-content {
  text-align: center;
  padding: 30px 20px;
}
.recovery-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}
.recovery-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.4;
}
.form-actions {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}
.submit-btn {
  min-width: 140px;
  height: 44px;
  background: #ff7a00;
  border: none;
  color: #fff;
  border-radius: 6px;
}
</style>
