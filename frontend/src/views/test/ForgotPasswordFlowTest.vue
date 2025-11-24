<template>
  <div class="test-page">
    <h2>找回密码流程测试</h2>
    <div class="card">
      <h3>手机找回（调用后端，自动跳转验证码页）</h3>
      <div class="row">
        <a-button type="primary" :loading="loading.phone" @click="startPhone">开始手机找回</a-button>
        <span class="hint">使用示例数据：{{ sample.phone }} / {{ sample.idType }} / {{ sample.idNumber }}</span>
      </div>
    </div>
    <div class="card">
      <h3>邮箱找回（调用后端，自动跳转验证码页）</h3>
      <div class="row">
        <a-button type="primary" :loading="loading.email" @click="startEmail">开始邮箱找回</a-button>
        <span class="hint">使用示例数据：{{ sample.email }} / {{ sample.idType }} / {{ sample.idNumber }}</span>
      </div>
    </div>
    <div class="card">
      <h3>人脸找回（调用后端，自动跳转验证码页）</h3>
      <div class="row">
        <a-button type="primary" :loading="loading.face" @click="startFace">开始人脸找回</a-button>
        <span class="hint">使用示例数据：{{ sample.email }} / {{ sample.idType }} / {{ sample.idNumber }}</span>
      </div>
    </div>
    <div class="card">
      <h3>仅界面跳转（不调用后端）</h3>
      <div class="links">
        <a-button @click="router.push({ path: '/forgot-password', query: { type: 'phone', step: 1 } })">主页：手机找回（第1步）</a-button>
        <a-button @click="router.push({ path: '/forgot-password/verify', query: { type: 'phone' } })">验证码页（无token占位）</a-button>
        <a-button @click="router.push({ path: '/forgot-password/new-password', query: { type: 'phone' } })">设置新密码页（占位）</a-button>
        <a-button @click="router.push({ path: '/forgot-password/done', query: { type: 'phone' } })">完成页</a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { submitPhoneRecovery, submitEmailRecovery, submitFaceRecovery } from '@/api/auth'

const router = useRouter()
const loading = reactive({ phone: false, email: false, face: false })
const sample = reactive({
  phone: '15500000000',
  email: 'test@example.com',
  idType: '身份证',
  idNumber: '11010519491231002X'
})

const startPhone = async () => {
  try {
    loading.phone = true
    const res = await submitPhoneRecovery({ phone: sample.phone, idType: sample.idType, idNumber: sample.idNumber })
    if (res.code === 200) {
      message.success('手机验证码已发送')
      router.push({ path: '/forgot-password/verify', query: { type: 'phone', token: res.data.token } })
    } else {
      message.error(res.message || '提交失败')
    }
  } catch (e) {
    message.error('请求失败')
  } finally {
    loading.phone = false
  }
}

const startEmail = async () => {
  try {
    loading.email = true
    const res = await submitEmailRecovery({ email: sample.email, idType: sample.idType, idNumber: sample.idNumber })
    if (res.code === 200) {
      message.success('邮箱验证码已发送')
      router.push({ path: '/forgot-password/verify', query: { type: 'email', token: res.data.token } })
    } else {
      message.error(res.message || '提交失败')
    }
  } catch (e) {
    message.error('请求失败')
  } finally {
    loading.email = false
  }
}

const startFace = async () => {
  try {
    loading.face = true
    const res = await submitFaceRecovery({ email: sample.email, idType: sample.idType, idNumber: sample.idNumber })
    if (res.code === 200) {
      message.success('人脸验证验证码已生成')
      router.push({ path: '/forgot-password/verify', query: { type: 'face', token: res.data.token } })
    } else {
      message.error(res.message || '提交失败')
    }
  } catch (e) {
    message.error('请求失败')
  } finally {
    loading.face = false
  }
}
</script>

<style scoped>
.test-page { padding: 20px; }
.card { border: 1px solid #e8e8e8; border-radius: 6px; padding: 16px; margin-bottom: 16px; background: #fff; }
.row { display: flex; align-items: center; gap: 12px; }
.hint { color: #999; font-size: 12px; }
.links { display: flex; gap: 12px; flex-wrap: wrap; }
</style>

