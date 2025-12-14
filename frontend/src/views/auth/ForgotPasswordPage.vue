<template>
  <div class="forgot-password-page">
    <Header12306 />

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="forgot-container">
        <!-- 选项卡导航 -->
        <div class="tab-navigation">
          <div
            class="tab-item"
            :class="{ active: activeTab === 'face' }"
            @click="activeTab = 'face'"
          >
            <span class="icon icon">&#xe6dc;</span>
            人脸找回
          </div>
          <div
            class="tab-item"
            :class="{ active: activeTab === 'phone' }"
            @click="activeTab = 'phone'"
          >
            <span class="icon icon">&#xe708;</span>
            手机找回
          </div>
          <div
            class="tab-item"
            :class="{ active: activeTab === 'email' }"
            @click="activeTab = 'email'"
          >
            <span class="icon icon">&#xe6f5;</span>
            邮箱找回
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="tab-content">
          <!-- 人脸找回 -->
          <div v-if="activeTab === 'face'" class="face-recovery">
            

            <div class="qr-content" v-if="faceStep === 1">
              <h3 class="recovery-title">人脸找回</h3>
              <p class="recovery-subtitle">
                扫描二维码，使用
                <span class="app-name">12306APP</span>
                找回密码
              </p>

              <div class="qr-code-container">
                <div class="qr-code">
                  <img :src="qrImage" alt="12306APP二维码" class="qr-img-large" />
                </div>
              </div>
            </div>
          </div>

          <!-- 手机找回 -->
          <div v-if="activeTab === 'phone'" class="phone-recovery">
            <div class="step-indicator">
              <div class="step" :class="{ active: phoneStep >= 1, completed: phoneStep > 1 }">
                <div class="step-number">1</div>
                <div class="step-text">填写账户信息</div>
              </div>
              <div class="step-line"></div>
              <div class="step" :class="{ active: phoneStep >= 2, completed: phoneStep > 2 }">
                <div class="step-number">2</div>
                <div class="step-text">获取验证码</div>
              </div>
              <div class="step-line"></div>
              <div class="step" :class="{ active: phoneStep >= 3, completed: phoneStep > 3 }">
                <div class="step-number">3</div>
                <div class="step-text">设置新密码</div>
              </div>
              <div class="step-line"></div>
              <div class="step" :class="{ active: phoneStep >= 4 }">
                <div class="step-number">4</div>
                <div class="step-text">完成</div>
              </div>
            </div>

            <div class="form-content">
              <a-form
                :model="phoneForm"
                layout="horizontal"
                :label-col="{ span: 6 }"
                :wrapper-col="{ span: 18 }"
                class="recovery-form"
              >
                <a-form-item label="手机号码：" required>
                  <div class="inline-field">
                    <a-select
                      v-model:value="phoneForm.countryCode"
                      placeholder="+86"
                      size="middle"
                      style="width: 90px"
                      class="phone-country-select"
                    >
                      <a-select-option value="+86">+86</a-select-option>
                      <a-select-option value="+852">+852</a-select-option>
                      <a-select-option value="+853">+853</a-select-option>
                      <a-select-option value="+886">+886</a-select-option>
                    </a-select>
                    <a-input v-model:value="phoneForm.phone" size="middle" />
                    <span class="inline-hint">已通过核验的手机号码</span>
                  </div>
                </a-form-item>

                <a-form-item label="证件类型：" required>
                  <div class="inline-field">
                    <a-select
                      v-model:value="phoneForm.idType"
                      placeholder="请选择证件类型"
                      size="middle"
                      style="width: 100%"
                    >
                      <a-select-option value="身份证">居民身份证</a-select-option>
                      <a-select-option value="护照">护照</a-select-option>
                      <a-select-option value="港澳通行证">港澳居民来往内地通行证</a-select-option>
                      <a-select-option value="台胞证">台湾居民来往大陆通行证</a-select-option>
                    </a-select>
                    <span class="inline-hint">请选择证件类型</span>
                  </div>
                </a-form-item>

                <a-form-item label="证件号码：" required>
                  <div class="inline-field">
                    <a-input v-model:value="phoneForm.idNumber" size="middle" />
                    <span class="inline-hint">请输入证件号码</span>
                  </div>
                </a-form-item>

                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handlePhoneSubmit"
                  >
                    提交
                  </a-button>
                </div>
              </a-form>

              <div class="help-text">
                手机号未通过核验？试试
                <a href="#" class="help-link" @click.prevent="activeTab = 'email'">邮箱找回</a>
              </div>
            </div>

            <div class="form-content" v-if="phoneStep === 2">
              <a-form :model="verificationForm" layout="vertical" class="recovery-form">
                <a-form-item label="验证码：" required>
                  <a-input
                    v-model:value="verificationForm.code"
                    placeholder="请输入短信验证码"
                    size="large"
                  />
                </a-form-item>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handleVerifyCode('phone')"
                  >
                    验证
                  </a-button>
                </div>
              </a-form>
            </div>

            <div class="form-content" v-if="phoneStep === 3">
              <a-form :model="passwordForm" layout="vertical" class="recovery-form">
                <a-form-item label="新密码：" required>
                  <a-input
                    v-model:value="passwordForm.newPassword"
                    type="password"
                    placeholder="请输入新密码"
                    size="large"
                  />
                </a-form-item>
                <a-form-item label="确认新密码：" required>
                  <a-input
                    v-model:value="passwordForm.confirmPassword"
                    type="password"
                    placeholder="请再次输入新密码"
                    size="large"
                  />
                </a-form-item>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handleSetNewPassword('phone')"
                  >
                    提交
                  </a-button>
                </div>
              </a-form>
            </div>

            <div class="qr-content" v-if="phoneStep === 4">
              <h3 class="recovery-title">密码重置成功</h3>
              <p class="recovery-subtitle">即将跳转到登录页面，请使用新密码登录</p>
            </div>
          </div>

          <!-- 邮箱找回 -->
          <div v-if="activeTab === 'email'" class="email-recovery">
            <div class="email-form-content">
              <a-form
                :model="emailForm"
                layout="horizontal"
                :label-col="{ span: 6 }"
                :wrapper-col="{ span: 18 }"
                class="email-recovery-form"
              >
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star"></span>
                      电子邮件
                    </span>
                  </template>
                  <div class="inline-field">
                    <a-input v-model:value="emailForm.email" size="middle" class="form-input" />
                    <span class="inline-hint">注册时所填的电子邮箱</span>
                  </div>
                </a-form-item>
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star"></span>
                      证件类型
                    </span>
                  </template>
                  <div class="inline-field">
                    <a-select
                      v-model:value="emailForm.idType"
                      placeholder="请选择证件类型"
                      size="middle"
                      class="form-input"
                    >
                      <a-select-option value="身份证">居民身份证</a-select-option>
                      <a-select-option value="护照">护照</a-select-option>
                      <a-select-option value="港澳通行证">港澳居民来往内地通行证</a-select-option>
                      <a-select-option value="台胞证">台湾居民来往大陆通行证</a-select-option>
                    </a-select>
                    <span class="inline-hint">请选择证件类型</span>
                  </div>
                </a-form-item>
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star"></span>
                      证件号码
                    </span>
                  </template>
                  <div class="inline-field">
                    <a-input v-model:value="emailForm.idNumber" size="middle" class="form-input" />
                    <span class="inline-hint">请输入证件号码</span>
                  </div>
                </a-form-item>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handleEmailSubmit"
                  >
                    提交
                  </a-button>
                </div>
              </a-form>
            </div>

            <div class="form-content" v-if="emailStep === 2">
              <a-form :model="verificationForm" layout="vertical" class="email-recovery-form">
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      验证码：
                    </span>
                  </template>
                  <a-input
                    v-model:value="verificationForm.code"
                    placeholder="请输入邮箱验证码"
                    size="large"
                    class="form-input"
                  />
                </a-form-item>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handleVerifyCode('email')"
                  >
                    验证
                  </a-button>
                </div>
              </a-form>
            </div>

            <div class="form-content" v-if="emailStep === 3">
              <a-form :model="passwordForm" layout="vertical" class="email-recovery-form">
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      新密码：
                    </span>
                  </template>
                  <a-input
                    v-model:value="passwordForm.newPassword"
                    type="password"
                    placeholder="请输入新密码"
                    size="large"
                    class="form-input"
                  />
                </a-form-item>
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      确认新密码：
                    </span>
                  </template>
                  <a-input
                    v-model:value="passwordForm.confirmPassword"
                    type="password"
                    placeholder="请再次输入新密码"
                    size="large"
                    class="form-input"
                  />
                </a-form-item>
                <div class="form-actions">
                  <a-button
                    type="primary"
                    size="large"
                    class="submit-btn"
                    :loading="loading"
                    @click="handleSetNewPassword('email')"
                  >
                    提交
                  </a-button>
                </div>
              </a-form>
            </div>

            <div class="qr-content" v-if="emailStep === 4">
              <h3 class="recovery-title">密码重置成功</h3>
              <p class="recovery-subtitle">即将跳转到登录页面，请使用新密码登录</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import {
  submitFaceRecovery,
  submitPhoneRecovery,
  submitEmailRecovery,
  verifyRecoveryCode,
  setNewPassword
} from '@/api/auth'

const router = useRouter()
const route = useRoute()
const qrImage = new URL('../../../pics/download.png', import.meta.url).href

// 当前激活的选项卡
const activeTab = ref('face')

// 步骤状态
const faceStep = ref(1)
const phoneStep = ref(1)
const emailStep = ref(1)

// 加载状态
const loading = ref(false)

// 恢复令牌
const recoveryToken = ref('')

// 表单数据
const faceForm = reactive({
  email: '',
  idType: '',
  idNumber: ''
})

const phoneForm = reactive({
  countryCode: '+86',
  phone: '',
  idType: '',
  idNumber: ''
})

const emailForm = reactive({
  email: '',
  idType: '',
  idNumber: ''
})

// 验证码表单
const verificationForm = reactive({
  code: ''
})

// 新密码表单
const passwordForm = reactive({
  newPassword: '',
  confirmPassword: ''
})

// 表单验证
const validateForm = (form, type) => {
  if (type === 'face' || type === 'email') {
    if (!form.email) {
      message.error('请输入邮箱地址')
      return false
    }
  }
  if (type === 'phone') {
    if (!form.phone) {
      message.error('请输入手机号码')
      return false
    }
  }
  if (!form.idType) {
    message.error('请选择证件类型')
    return false
  }
  if (!form.idNumber) {
    message.error('请输入证件号码')
    return false
  }
  return true
}

// 处理人脸找回提交
const handleFaceSubmit = async () => {
  if (!validateForm(faceForm, 'face')) return

  try {
    loading.value = true
    const response = await submitFaceRecovery(faceForm)

    if (response.code === 200) {
      recoveryToken.value = response.data.token
      message.success('验证信息已提交，请按照提示完成后续步骤')
      faceStep.value = 2
    } else {
      message.error(response.message || '提交失败，请重试')
    }
  } catch (error) {
    console.error('人脸找回提交失败:', error)
    message.error('提交失败，请重试')
  } finally {
    loading.value = false
  }
}

// 处理手机找回提交
const handlePhoneSubmit = async () => {
  // 自动去除空格
  if (phoneForm.phone) phoneForm.phone = phoneForm.phone.trim()
  if (phoneForm.idNumber) phoneForm.idNumber = phoneForm.idNumber.trim()
  
  if (!validateForm(phoneForm, 'phone')) return

  try {
    loading.value = true
    const response = await submitPhoneRecovery(phoneForm)

    if (response.code === 200) {
      recoveryToken.value = response.data.token
      message.success('验证码已发送到您的手机')
      router.push({
        path: '/forgot-password/verify',
        query: { type: 'phone', token: recoveryToken.value }
      })
    } else {
      message.error(response.message || '提交失败，请重试')
    }
  } catch (error) {
    console.error('手机找回提交失败:', error)
    message.error('提交失败，请重试')
  } finally {
    loading.value = false
  }
}

// 处理邮箱找回提交
const handleEmailSubmit = async () => {
  // 自动去除空格
  if (emailForm.email) emailForm.email = emailForm.email.trim()
  if (emailForm.idNumber) emailForm.idNumber = emailForm.idNumber.trim()

  if (!validateForm(emailForm, 'email')) return

  try {
    loading.value = true
    const response = await submitEmailRecovery(emailForm)

    if (response.code === 200) {
      recoveryToken.value = response.data.token
      message.success('验证码已发送到您的邮箱')
      router.push({
        path: '/forgot-password/verify',
        query: { type: 'email', token: recoveryToken.value }
      })
    } else {
      message.error(response.message || '提交失败，请重试')
    }
  } catch (error) {
    console.error('邮箱找回提交失败:', error)
    message.error('提交失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleVerifyCode = async type => {
  if (!verificationForm.code) {
    message.error('请输入验证码')
    return
  }
  loading.value = true
  setTimeout(() => {
    message.success('已提交验证码（占位符）')
    if (type === 'face') {
      faceStep.value = 3
      router.replace({ path: '/forgot-password', query: { type: 'face', step: 3 } })
    }
    if (type === 'phone') {
      phoneStep.value = 3
      router.replace({ path: '/forgot-password', query: { type: 'phone', step: 3 } })
    }
    if (type === 'email') {
      emailStep.value = 3
      router.replace({ path: '/forgot-password', query: { type: 'email', step: 3 } })
    }
    loading.value = false
  }, 300)
}

// 设置新密码
const handleSetNewPassword = async type => {
  if (!passwordForm.newPassword) {
    message.error('请输入新密码')
    return
  }
  if (!passwordForm.confirmPassword) {
    message.error('请确认新密码')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    message.error('两次输入的密码不一致')
    return
  }

  try {
    loading.value = true
    const response = await setNewPassword({
      token: recoveryToken.value,
      newPassword: passwordForm.newPassword,
      confirmPassword: passwordForm.confirmPassword
    })

    if (response.code === 200) {
      message.success('密码重置成功，请使用新密码登录')
      router.replace({ path: '/forgot-password/done', query: { type } })
    } else {
      message.error(response.message || '密码重置失败')
    }
  } catch (error) {
    console.error('密码重置失败:', error)
    message.error('密码重置失败，请重试')
  } finally {
    loading.value = false
  }
}
const initFromRoute = () => {
  const t = route.query.type
  const s = Number(route.query.step || 1)
  if (t === 'phone' || t === 'email' || t === 'face') activeTab.value = t
  if (activeTab.value === 'phone') phoneStep.value = s
  if (activeTab.value === 'email') emailStep.value = s
  if (activeTab.value === 'face') faceStep.value = s
}
initFromRoute()
watch(
  () => route.query,
  () => initFromRoute(),
  { deep: true }
)

const proceedFaceStep2 = () => {
  router.push({ path: '/forgot-password/verify', query: { type: 'face' } })
}
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  background: #ffffff;
  position: relative;
  overflow: hidden;
}

.forgot-password-page::before {
  display: none;
}

/* Header 已由统一组件替换，无需本地样式 */

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

.tab-item .icon {
  display: inline-block;
  font-size: 18px;
  line-height: 1;
  margin-right: 4px;
  opacity: 0.95;
}

.tab-item:hover .icon {
  transform: scale(1.05);
}

.tab-item.active .icon {
  opacity: 1;
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

.step.active .step-text {
  color: #298cce;
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

.inline-field {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  padding-right: 200px;
}

.inline-field :deep(.ant-input),
.inline-field :deep(.ant-input-affix-wrapper),
.inline-field :deep(.ant-select-selector) {
  flex: 1;
}

.inline-hint {
  font-size: 12px;
  color: #ff7a00;
  white-space: nowrap;
  position: absolute;
  left: calc(100% - 200px);
  width: 200px;
  padding-left: 8px;
  text-align: left;
  top: 50%;
  transform: translateY(-50%);
}

.form-hint {
  font-size: 12px;
  color: #ff7a00;
  margin-top: 4px;
}

.recovery-form :deep(.ant-form-item-label > label) {
  font-size: 13px;
  color: #333;
}
.recovery-form :deep(.ant-form-item) {
  margin-bottom: 16px;
}
.recovery-form :deep(.ant-input),
.recovery-form :deep(.ant-input-affix-wrapper),
.recovery-form :deep(.ant-select-selector) {
  border-radius: 0;
}

.inline-field .phone-country-select :deep(.ant-select-selector) {
  flex: initial;
  width: 100%;
}

.form-actions {
  margin-top: 18px;
  text-align: center;
}

.submit-btn {
  height: 40px;
  min-width: 120px;
  font-size: 15px;
  border-radius: 6px;
  background: #ff7a00;
  border: none;
  color: white;
  font-weight: 500;
  transition: all 0.3s;
}

.submit-btn:hover {
  background: #f26c02;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(242, 108, 2, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn:disabled {
  background: #d9d9d9;
  color: rgba(0, 0, 0, 0.25);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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

/* 人脸找回二维码样式 */
.qr-content {
  text-align: center;
  padding: 30px 20px;
}

.recovery-title {
  font-size: 15px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.recovery-subtitle {
  font-size: 13px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.4;
}

.app-name {
  color: #478dcd;
  font-weight: bold;
}

.qr-code-container {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.qr-code {
  padding: 15px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid #e8e8e8;
}

.qr-img-large {
  width: 160px;
  height: 160px;
  object-fit: contain;
  display: block;
}

.qr-instructions {
  max-width: 350px;
  margin: 0 auto;
}

.instruction-text {
  font-size: 13px;
  color: #333;
  margin-bottom: 6px;
  line-height: 1.4;
}

.instruction-note {
  font-size: 11px;
  color: #999;
  line-height: 1.3;
}

/* 邮箱找回样式 */
.email-recovery {
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 0;
}

.email-form-content {
  padding: 10px 25px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.email-recovery-form {
  max-width: 560px;
  margin: 0 auto;
  width: 100%;
}

.email-recovery-form .ant-form-item {
  margin-bottom: 16px;
}

.email-recovery-form .form-label {
  font-size: 13px;
  color: #333;
  font-weight: normal;
  display: flex;
  align-items: center;
}

.email-recovery-form .required-star {
  color: #ff4d4f;
  margin-right: 3px;
  font-size: 13px;
}

.email-recovery-form .form-input {
  border-radius: 0;
  border: 1px solid #d9d9d9;
}

.email-recovery-form .form-input:hover {
  border-color: #40a9ff;
}

.email-recovery-form .form-input:focus,
.email-recovery-form .form-input.ant-input-focused {
  border-color: #40a9ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.email-recovery-form .ant-select .ant-select-selector {
  border-radius: 0;
  border: 1px solid #d9d9d9;
}

.email-recovery-form .ant-select:hover .ant-select-selector {
  border-color: #40a9ff;
}

.email-recovery-form .ant-select.ant-select-focused .ant-select-selector {
  border-color: #40a9ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.email-recovery-form .form-actions {
  text-align: center;
  margin-top: 24px;
}

.email-recovery-form .submit-btn {
  background: #ff6600;
  border-color: #ff6600;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  height: 36px;
  min-width: 100px;
  transition: all 0.3s ease;
}

.email-recovery-form .submit-btn:hover {
  background: #e55a00;
  border-color: #e55a00;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 102, 0, 0.3);
}

.email-recovery-form .submit-btn:active {
  transform: translateY(0);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }

  .logo-text {
    font-size: 16px;
  }

  .subtitle {
    display: none;
  }

  .main-content {
    padding: 20px 10px;
  }

  .tab-content {
    padding: 20px;
  }

  .step-indicator {
    flex-wrap: wrap;
    gap: 10px;
  }

  .step-line {
    width: 30px;
  }

  .tab-item {
    padding: 15px 10px;
    font-size: 12px;
  }

  /* 二维码移动端适配 */
  .qr-content {
    padding: 15px 10px;
  }

  .recovery-title {
    font-size: 18px;
  }

  .recovery-subtitle {
    font-size: 13px;
    margin-bottom: 20px;
  }

  .qr-img-large {
    width: 140px;
    height: 140px;
  }

  .qr-code {
    padding: 12px;
  }

  /* 邮箱找回移动端适配 */
  .email-recovery {
    padding-top: 40px;
    min-height: 350px;
  }

  .email-form-content {
    padding: 15px 12px;
  }

  .email-recovery-form .ant-form-item {
    margin-bottom: 16px;
  }

  .email-recovery-form .form-actions {
    margin-top: 20px;
  }

  .email-recovery-form .submit-btn {
    width: 100%;
    height: 40px;
  }
}
</style>
