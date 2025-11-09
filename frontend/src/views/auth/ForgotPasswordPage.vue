<template>
  <div class="forgot-password-page">
    <!-- 顶部导航栏 -->
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">🚄</div>
          <span class="logo-text">中国铁路12306</span>
          <span class="subtitle">12306 CHINA RAILWAY</span>
        </div>
        <div class="header-nav">
          <a-button type="link" @click="$router.push('/login')">登录</a-button>
          <a-button type="link" @click="$router.push('/register')">注册</a-button>
        </div>
      </div>
    </div>

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
            <i class="icon-face"></i>
            人脸找回
          </div>
          <div 
            class="tab-item" 
            :class="{ active: activeTab === 'phone' }"
            @click="activeTab = 'phone'"
          >
            <i class="icon-phone"></i>
            手机找回
          </div>
          <div 
            class="tab-item" 
            :class="{ active: activeTab === 'email' }"
            @click="activeTab = 'email'"
          >
            <i class="icon-email"></i>
            邮箱找回
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="tab-content">
          <!-- 人脸找回 -->
          <div v-if="activeTab === 'face'" class="face-recovery">
            <div class="qr-content">
              <h3 class="recovery-title">人脸找回</h3>
              <p class="recovery-subtitle">扫描二维码，使用<span class="app-name">12306APP</span>找回密码</p>
              
              <div class="qr-code-container">
                <div class="qr-code">
                  <!-- 二维码SVG -->
                  <svg width="160" height="160" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <!-- 外框 -->
                    <rect x="10" y="10" width="180" height="180" fill="white" stroke="#000" stroke-width="2"/>
                    
                    <!-- 左上角定位点 -->
                    <rect x="20" y="20" width="50" height="50" fill="black"/>
                    <rect x="30" y="30" width="30" height="30" fill="white"/>
                    <rect x="40" y="40" width="10" height="10" fill="black"/>
                    
                    <!-- 右上角定位点 -->
                    <rect x="130" y="20" width="50" height="50" fill="black"/>
                    <rect x="140" y="30" width="30" height="30" fill="white"/>
                    <rect x="150" y="40" width="10" height="10" fill="black"/>
                    
                    <!-- 左下角定位点 -->
                    <rect x="20" y="130" width="50" height="50" fill="black"/>
                    <rect x="30" y="140" width="30" height="30" fill="white"/>
                    <rect x="40" y="150" width="10" height="10" fill="black"/>
                    
                    <!-- 中心logo区域 -->
                    <circle cx="100" cy="100" r="15" fill="#e60012"/>
                    <text x="100" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">🚄</text>
                    
                    <!-- 模拟二维码数据点 -->
                    <rect x="80" y="20" width="5" height="5" fill="black"/>
                    <rect x="90" y="20" width="5" height="5" fill="black"/>
                    <rect x="100" y="20" width="5" height="5" fill="black"/>
                    <rect x="110" y="20" width="5" height="5" fill="black"/>
                    
                    <rect x="20" y="80" width="5" height="5" fill="black"/>
                    <rect x="30" y="80" width="5" height="5" fill="black"/>
                    <rect x="40" y="80" width="5" height="5" fill="black"/>
                    <rect x="50" y="80" width="5" height="5" fill="black"/>
                    
                    <rect x="80" y="80" width="5" height="5" fill="black"/>
                    <rect x="120" y="80" width="5" height="5" fill="black"/>
                    <rect x="130" y="80" width="5" height="5" fill="black"/>
                    <rect x="140" y="80" width="5" height="5" fill="black"/>
                    
                    <rect x="80" y="120" width="5" height="5" fill="black"/>
                    <rect x="90" y="120" width="5" height="5" fill="black"/>
                    <rect x="100" y="120" width="5" height="5" fill="black"/>
                    <rect x="110" y="120" width="5" height="5" fill="black"/>
                    <rect x="120" y="120" width="5" height="5" fill="black"/>
                    
                    <rect x="80" y="160" width="5" height="5" fill="black"/>
                    <rect x="90" y="160" width="5" height="5" fill="black"/>
                    <rect x="100" y="160" width="5" height="5" fill="black"/>
                    <rect x="110" y="160" width="5" height="5" fill="black"/>
                    <rect x="120" y="160" width="5" height="5" fill="black"/>
                    <rect x="130" y="160" width="5" height="5" fill="black"/>
                    <rect x="140" y="160" width="5" height="5" fill="black"/>
                    <rect x="150" y="160" width="5" height="5" fill="black"/>
                    <rect x="160" y="160" width="5" height="5" fill="black"/>
                    <rect x="170" y="160" width="5" height="5" fill="black"/>
                    
                    <!-- 更多数据点 -->
                    <rect x="25" y="95" width="5" height="5" fill="black"/>
                    <rect x="35" y="95" width="5" height="5" fill="black"/>
                    <rect x="45" y="95" width="5" height="5" fill="black"/>
                    <rect x="55" y="95" width="5" height="5" fill="black"/>
                    <rect x="65" y="95" width="5" height="5" fill="black"/>
                    
                    <rect x="135" y="95" width="5" height="5" fill="black"/>
                    <rect x="145" y="95" width="5" height="5" fill="black"/>
                    <rect x="155" y="95" width="5" height="5" fill="black"/>
                    <rect x="165" y="95" width="5" height="5" fill="black"/>
                    <rect x="175" y="95" width="5" height="5" fill="black"/>
                  </svg>
                </div>
              </div>
              
              <div class="qr-instructions">
                <p class="instruction-text">请使用中国铁路12306手机客户端扫描上方二维码</p>
                <p class="instruction-note">扫码后按照APP提示完成身份验证即可找回密码</p>
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
              <a-form :model="phoneForm" layout="vertical" class="recovery-form">
                <a-form-item label="手机号码：" required>
                  <a-input 
                    v-model:value="phoneForm.phone" 
                    placeholder="请输入您的手机号码"
                    size="large"
                    addon-before="+86"
                  />
                  <div class="form-hint">已通过核验的手机号码</div>
                </a-form-item>

                <a-form-item label="证件类型：" required>
                  <a-select 
                    v-model:value="phoneForm.idType" 
                    placeholder="请选择证件类型"
                    size="large"
                  >
                    <a-select-option value="身份证">居民身份证</a-select-option>
                    <a-select-option value="护照">护照</a-select-option>
                    <a-select-option value="港澳通行证">港澳居民来往内地通行证</a-select-option>
                    <a-select-option value="台胞证">台湾居民来往大陆通行证</a-select-option>
                  </a-select>
                  <div class="form-hint">请选择证件类型</div>
                </a-form-item>

                <a-form-item label="证件号码：" required>
                  <a-input 
                    v-model:value="phoneForm.idNumber" 
                    placeholder="请输入证件号码"
                    size="large"
                  />
                  <div class="form-hint">请输入证件号码</div>
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
                手机号未通过核验？<a href="#" class="help-link">试试邮箱找回</a>
              </div>
            </div>
          </div>

          <!-- 邮箱找回 -->
          <div v-if="activeTab === 'email'" class="email-recovery">
            <div class="email-form-content">
              <a-form :model="emailForm" layout="vertical" class="email-recovery-form">
                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      电子邮件：
                    </span>
                  </template>
                  <a-input 
                    v-model:value="emailForm.email" 
                    placeholder="注册时所填的电子邮箱"
                    size="large"
                    class="form-input"
                  />
                </a-form-item>

                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      证件类型：
                    </span>
                  </template>
                  <a-select 
                    v-model:value="emailForm.idType" 
                    placeholder="请选择证件类型"
                    size="large"
                    class="form-input"
                  >
                    <a-select-option value="身份证">居民身份证</a-select-option>
                    <a-select-option value="护照">护照</a-select-option>
                    <a-select-option value="港澳通行证">港澳居民来往内地通行证</a-select-option>
                    <a-select-option value="台胞证">台湾居民来往大陆通行证</a-select-option>
                  </a-select>
                </a-form-item>

                <a-form-item required>
                  <template #label>
                    <span class="form-label">
                      <span class="required-star">*</span>
                      证件号码：
                    </span>
                  </template>
                  <a-input 
                    v-model:value="emailForm.idNumber" 
                    placeholder="请输入证件号码"
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
                    @click="handleEmailSubmit"
                  >
                    提交
                  </a-button>
                </div>
              </a-form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { 
  submitFaceRecovery, 
  submitPhoneRecovery, 
  submitEmailRecovery,
  verifyRecoveryCode,
  setNewPassword
} from '@/api/auth'

const router = useRouter()

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
  if (!validateForm(phoneForm, 'phone')) return
  
  try {
    loading.value = true
    const response = await submitPhoneRecovery(phoneForm)
    
    if (response.code === 200) {
      recoveryToken.value = response.data.token
      message.success('验证码已发送到您的手机')
      phoneStep.value = 2
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
  if (!validateForm(emailForm, 'email')) return
  
  try {
    loading.value = true
    const response = await submitEmailRecovery(emailForm)
    
    if (response.code === 200) {
      recoveryToken.value = response.data.token
      message.success('验证码已发送到您的邮箱')
      emailStep.value = 2
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

// 验证验证码
const handleVerifyCode = async (type) => {
  if (!verificationForm.code) {
    message.error('请输入验证码')
    return
  }
  
  try {
    loading.value = true
    const response = await verifyRecoveryCode({
      token: recoveryToken.value,
      verificationCode: verificationForm.code,
      type
    })
    
    if (response.code === 200) {
      message.success('验证码验证成功')
      if (type === 'face') faceStep.value = 3
      if (type === 'phone') phoneStep.value = 3
      if (type === 'email') emailStep.value = 3
    } else {
      message.error(response.message || '验证码错误')
    }
  } catch (error) {
    console.error('验证码验证失败:', error)
    message.error('验证失败，请重试')
  } finally {
    loading.value = false
  }
}

// 设置新密码
const handleSetNewPassword = async (type) => {
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
      if (type === 'face') faceStep.value = 4
      if (type === 'phone') phoneStep.value = 4
      if (type === 'email') emailStep.value = 4
      
      // 3秒后跳转到登录页面
      setTimeout(() => {
        router.push('/login')
      }, 3000)
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
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 50%, #1e5f99 100%);
  position: relative;
  overflow: hidden;
}

.forgot-password-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><path d="M0,300 Q300,200 600,300 T1200,300 L1200,600 L0,600 Z" fill="rgba(255,255,255,0.1)"/></svg>') no-repeat center;
  background-size: cover;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 60px;
  display: flex;
  align-items: center;
  position: relative;
  z-index: 2;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: #e60012;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.subtitle {
  font-size: 12px;
  color: #666;
  margin-left: 5px;
}

.header-nav {
  display: flex;
  gap: 10px;
}

.main-content {
  padding: 50px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
  position: relative;
  z-index: 1;
}

.forgot-container {
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 800px;
  overflow: hidden;
}

.tab-navigation {
  display: flex;
  border-bottom: 1px solid #e8e8e8;
}

.tab-item {
  flex: 1;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid transparent;
}

.tab-item:hover {
  background: #f5f5f5;
}

.tab-item.active {
  color: #ff6600;
  border-bottom-color: #ff6600;
  background: white;
}

.tab-item i {
  font-size: 24px;
}

.icon-face::before {
  content: "👤";
}

.icon-phone::before {
  content: "📱";
}

.icon-email::before {
  content: "📧";
}

.tab-content {
  padding: 40px;
}

.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 32px;
  height: 32px;
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
  background: #ff6600;
  color: #fff;
}

.step.completed .step-number {
  background: #52c41a;
  color: #fff;
}

.step-text {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
}

.step.active .step-text {
  color: #ff6600;
}

.step-line {
  width: 60px;
  height: 2px;
  background: #f0f0f0;
  margin: 0 10px;
}

.form-content {
  max-width: 400px;
  margin: 0 auto;
}

.recovery-form {
  margin-bottom: 20px;
}

.form-hint {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.form-actions {
  margin-top: 30px;
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: 6px;
  background: #ff6600;
  border: none;
  color: white;
  font-weight: 500;
  transition: all 0.3s;
}

.submit-btn:hover {
  background: #e55a00;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
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
  color: #ff6600;
  text-decoration: none;
  transition: color 0.3s;
}

.help-link:hover {
  color: #e55a00;
  text-decoration: underline;
}

/* 人脸找回二维码样式 */
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

.app-name {
  color: #ff6600;
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
  min-height: 400px;
  padding-top: 60px;
}

.email-form-content {
  padding: 20px 25px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.email-recovery-form {
  max-width: 380px;
  margin: 0 auto;
  width: 100%;
}

.email-recovery-form .ant-form-item {
  margin-bottom: 18px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  
  .qr-code svg {
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