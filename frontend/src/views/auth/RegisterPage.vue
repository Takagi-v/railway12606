<template>
  <div class="register-page">
    

    

    <!-- 主体区域 -->
    <main class="register-main">
      <div class="main-content">
        <div class="register-container">
          <!-- 注册卡片 -->
          <div class="register-card">
            <div class="card-header">
              <h2 class="card-title">账户信息</h2>
            </div>
            
            <div class="card-body">
              <a-form
                ref="formRef"
                :model="registerForm"
                :rules="rules"
                @finish="handleRegister"
                layout="horizontal"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 19 }"
                class="register-form"
              >
                <!-- 用户名 -->
                <a-form-item name="username" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      用户名
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input
                      v-model:value="registerForm.username"
                      placeholder="用户名设置成功后不可修改"
                      size="middle"
                      class="form-input"
                      @blur="clearFieldError('username')"
                    />
                    <span class="field-hint username-hint">6-30位字母、数字或“_”字母开头</span>
                  </div>
                  <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
                </a-form-item>

                <!-- 密码 -->
                <a-form-item name="password" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      密码
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input-password
                      v-model:value="registerForm.password"
                      placeholder="6-20位，包含字母和数字"
                      size="middle"
                      class="form-input"
                      @input="updatePasswordStrength"
                      @blur="clearFieldError('password')"
                    />
                    <span v-if="!registerForm.password" class="field-hint password-hint">6-20位，包含字母和数字</span>
                    <div v-if="registerForm.password" class="password-strength inline">
                      <div class="strength-bar">
                        <div 
                          class="strength-fill" 
                          :class="passwordStrength.level"
                          :style="{ width: passwordStrength.width }"
                        ></div>
                      </div>
                      <span class="strength-text" :class="passwordStrength.level">
                        {{ passwordStrength.text }}
                      </span>
                    </div>
                  </div>
                  <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
                </a-form-item>

                <!-- 再次输入密码 -->
                <a-form-item name="confirmPassword" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      再次输入密码
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input-password
                      v-model:value="registerForm.confirmPassword"
                      placeholder="请再次输入密码"
                      size="middle"
                      class="form-input"
                      @blur="clearFieldError('confirmPassword')"
                    />
                  </div>
                  <div v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</div>
                </a-form-item>

                <!-- 证件类型 -->
                <a-form-item name="idType" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      证件类型
                    </span>
                  </template>
                  <div class="field-row">
                    <a-select
                      v-model:value="registerForm.idType"
                      size="middle"
                      class="form-input"
                    >
                      <a-select-option value="身份证">居民身份证</a-select-option>
                      <a-select-option value="护照">护照</a-select-option>
                      <a-select-option value="港澳通行证">港澳通行证</a-select-option>
                      <a-select-option value="台胞证">台胞证</a-select-option>
                    </a-select>
                  </div>
                </a-form-item>

                <!-- 姓名 -->
                <a-form-item name="realName" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      姓名
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input
                      v-model:value="registerForm.realName"
                      placeholder="请输入姓名"
                      size="middle"
                      class="form-input"
                      @blur="clearFieldError('realName')"
                    />
                    <span class="field-hint">姓名填写规则（用于身份核验，请正确填写）</span>
                  </div>
                  <div v-if="errors.realName" class="error-message">{{ errors.realName }}</div>
                </a-form-item>

                <!-- 证件号码 -->
                <a-form-item name="idNumber" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      证件号码
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input
                      v-model:value="registerForm.idNumber"
                      placeholder="请输入您的证件号码"
                      size="middle"
                      class="form-input"
                      @blur="clearFieldError('idNumber')"
                    />
                    <span class="field-hint">（用于身份核验，请正确填写）</span>
                  </div>
                  <div v-if="errors.idNumber" class="error-message">{{ errors.idNumber }}</div>
                </a-form-item>

                <!-- 优待（符）类型 -->
                <a-form-item name="userType" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      优惠（待）类型
                    </span>
                  </template>
                  <div class="field-row">
                    <a-select
                      v-model:value="registerForm.userType"
                      size="middle"
                      class="form-input"
                    >
                      <a-select-option value="成人">成人</a-select-option>
                      <a-select-option value="学生">学生</a-select-option>
                      <a-select-option value="残疾军人">残疾军人</a-select-option>
                    </a-select>
                  </div>
                </a-form-item>
                <div class="form-divider"></div>

                <!-- 邮箱 -->
                <a-form-item name="email" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      邮箱
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input
                      v-model:value="registerForm.email"
                      placeholder="请正确填写邮箱地址"
                      size="middle"
                      class="form-input"
                      @blur="clearFieldError('email')"
                    />
                  </div>
                  <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
                </a-form-item>

                <!-- 手机号 -->
                <a-form-item name="phone" class="form-item full-width">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star"></span>
                      手机号
                    </span>
                  </template>
                  <div class="field-row">
                    <a-input-group compact class="phone-input-group">
                      <a-form-item-rest>
                        <a-select
                          v-model:value="registerForm.countryCode"
                          size="middle"
                          class="country-code-select"
                        >
                          <a-select-option value="+86">+86 中国</a-select-option>
                          <a-select-option value="+852">+852 香港</a-select-option>
                          <a-select-option value="+853">+853 澳门</a-select-option>
                          <a-select-option value="+886">+886 台湾</a-select-option>
                        </a-select>
                      </a-form-item-rest>
                      <a-input
                        v-model:value="registerForm.phone"
                        placeholder="手机号"
                        size="middle"
                        class="phone-input"
                        @blur="clearFieldError('phone')"
                      />
                    </a-input-group>
                    <span class="field-hint">请正确填写手机号，稍后将向该手机号发送短信验证码</span>
                  </div>
                  <div v-if="errors.phone" class="error-message">{{ errors.phone }}</div>
                </a-form-item>

                <!-- 服务协议 -->
                <a-form-item name="agreeTerms" class="form-item full-width">
                  <a-checkbox v-model:checked="registerForm.agreeTerms">
                    我已阅读并同意
                    <a href="#" class="terms-link">《用户服务条款》</a>
                    和
                    <a href="#" class="terms-link">《隐私政策》</a>
                  </a-checkbox>
                  <div v-if="errors.agreeTerms" class="error-message">{{ errors.agreeTerms }}</div>
                </a-form-item>

                <!-- 提交按钮 -->
                <a-form-item class="form-item submit-item full-width">
                  <a-button 
                    type="primary" 
                    html-type="submit" 
                    size="middle" 
                    block 
                    :loading="loading"
                    class="submit-btn"
                  >
                    下一步
                  </a-button>
                </a-form-item>

                </a-form>
            </div>
          </div>
        </div>
      </div>
    </main>

    
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const formRef = ref()

// 表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  idType: '身份证',
  realName: '',
  idNumber: '',
  userType: '成人',
  email: '',
  countryCode: '+86',
  phone: '',
  agreeTerms: false
})

// 错误信息
const errors = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  realName: '',
  idNumber: '',
  email: '',
  phone: '',
  agreeTerms: ''
})

// 密码强度计算
const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return { level: '', width: '0%', text: '' }

  let score = 0
  let feedback = []

  // 长度检查
  if (password.length >= 8) score += 25
  else if (password.length >= 6) score += 15
  else feedback.push('至少6位')

  // 包含小写字母
  if (/[a-z]/.test(password)) score += 25
  else feedback.push('包含小写字母')

  // 包含大写字母
  if (/[A-Z]/.test(password)) score += 25
  else feedback.push('包含大写字母')

  // 包含数字
  if (/\d/.test(password)) score += 25
  else feedback.push('包含数字')

  // 包含特殊字符
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 10

  let level, text, width
  if (score < 30) {
    level = 'weak'
    text = '弱'
    width = '25%'
  } else if (score < 60) {
    level = 'medium'
    text = '中'
    width = '50%'
  } else if (score < 90) {
    level = 'strong'
    text = '强'
    width = '75%'
  } else {
    level = 'very-strong'
    text = '很强'
    width = '100%'
  }

  return { level, width, text }
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 6, max: 30, message: '用户名长度为6-30位', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_-][a-zA-Z0-9_-]*$/, message: '用户名只能以字母、数字、下划线或横线开头，包含字母、数字、下划线和横线', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20位', trigger: 'blur' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*\d).+$/, message: '密码必须包含字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        if (value !== registerForm.password) {
          return Promise.reject('两次输入的密码不一致')
        }
        return Promise.resolve()
      },
      trigger: 'blur'
    }
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { pattern: /^[\u4e00-\u9fa5·]{2,20}$/, message: '请输入2-20位中文姓名', trigger: 'blur' }
  ],
  idNumber: [
    { required: true, message: '请输入证件号码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        if (registerForm.idType === '身份证') {
          const idPattern = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
          if (!idPattern.test(value)) {
            return Promise.reject('请输入正确的身份证号码')
          }
        }
        return Promise.resolve()
      },
      trigger: 'blur'
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  agreeTerms: [
    {
      validator: (rule, value) => {
        if (!value) {
          return Promise.reject('请阅读并同意服务条款')
        }
        return Promise.resolve()
      },
      trigger: 'change'
    }
  ]
}

// 清除字段错误
const clearFieldError = (field) => {
  errors[field] = ''
}

// 更新密码强度
const updatePasswordStrength = () => {
  // 密码强度会通过computed自动更新
}

// 表单提交
const handleRegister = async (values) => {
  try {
    loading.value = true
    
    // 验证服务条款
    if (!registerForm.agreeTerms) {
      errors.agreeTerms = '请阅读并同意服务条款'
      return
    }

    // 构建注册数据
    const registerData = {
      username: registerForm.username,
      password: registerForm.password,
      realName: registerForm.realName,
      idType: registerForm.idType,
      idNumber: registerForm.idNumber,
      userType: registerForm.userType,
      email: registerForm.email,
      phone: registerForm.phone,
      agreeTerms: registerForm.agreeTerms
    }

    await userStore.register({
      ...registerData,
      real_name: registerData.realName,
      id_type: registerData.idType,
      id_number: registerData.idNumber,
      user_type: registerData.userType
    })
    
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
/* 整体页面布局 */
.register-page {
  min-height: 100vh;
  background: #f5f5f5;
  font-family: "Tahoma", "SimSun", "宋体", serif;
  font-size: 12px;
}

.register-page :deep([class^="ant-"]:not(.anticon)) {
  font-size: 12px;
  font-family: "Tahoma", "SimSun", "宋体", serif;
}

/* 顶部Header */
.register-header {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
  color: #1890ff;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.welcome-text {
  color: #666;
  font-size: 14px;
}

.nav-links {
  display: flex;
  gap: 16px;
}

.nav-links .ant-btn-link {
  color: #666;
  padding: 4px 8px;
}

.nav-links .ant-btn-link:hover {
  color: #1890ff;
}

/* 蓝色导航条 */
.nav-bar {
  background: linear-gradient(90deg, #1890ff 0%, #40a9ff 100%);
  padding: 0;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-items {
  display: flex;
  gap: 40px;
}

.nav-item {
  color: white;
  padding: 12px 0;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-item:hover {
  color: #e6f7ff;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* 主体区域 */
.register-main {
  padding: 0;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.register-container {
  display: flex;
  justify-content: center;
}

/* 注册卡片 */
.register-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 978px;
  height: auto;
}

.card-header {
  background: #1678be;
  height: 32px;
  padding: 0 16px;
  border-bottom: 2px solid #0558cb;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.card-title {
  color: #E5F8FF;
  font-size: 12px;
  font-weight: 600;
  margin: 0;
  text-align: left;
}

.card-body {
  padding: 16px 24px;

  display: flex;
  justify-content: center;
  align-items: center;
}

/* 表单样式 */
.register-form {
  max-width: 100%;
  display: block;
  width: 900px;
  margin: 0 auto;
}

.form-item {
  margin-bottom: 5px;
  margin-left: 150px; 
  /* text-align: center;  */
}

.form-item.full-width :deep(.ant-form-item-control-wrapper) {
  width: 100% !important;
}

.form-item[name="agreeTerms"] {
  margin-left: 0 !important;
}

.form-item[name="agreeTerms"] :deep(.ant-checkbox-wrapper) {
  white-space: nowrap !important;
  font-size: 12px;
  font-family: "Tahoma", "SimSun", "宋体", serif;
}

.form-item[name="agreeTerms"] a.terms-link {
  white-space: nowrap;
  font-size: 12px;
  font-family: "Tahoma", "SimSun", "宋体", serif;
}

.form-item :deep(.ant-form-item-label) {
  padding-bottom: 2px;
  padding-right: 0;
  text-align: right;
  display: flex;
  font-size: 12px;
  /* margin-left: 50px; */
  align-items: center;
  height: 30px;
  background: transparent;
}

.required-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: #333;
  font-size: 12px;
  line-height: 30px;
}

.required-star {
  color: #ff4d4f;
  margin-right: 4px;
  font-size: 14px;
}

.form-input {
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  transition: all 0.3s;
  font-size: 12px;
  font-family: "Tahoma", "SimSun", "宋体", serif;
  width: 201px;
}

.form-input:hover {
  border-color: #40a9ff;
}

.form-input:focus,
.form-input.ant-input-focused {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.form-item :deep(.ant-input),
.form-item :deep(.ant-input-password .ant-input) {
  height: 30px;
  font-size: 12px;
}

/* 密码输入（带后缀）容器尺寸强制为 201×30 */
.form-item :deep(.ant-input-affix-wrapper.form-input) {
  width: 201px;
  height: 30px;
  padding: 0 8px;
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  position: relative;
  z-index: 1;
}

.form-item :deep(.ant-input-affix-wrapper .ant-input) {
  height: 30px;
  line-height: 30px;
  border: none;
}

.form-item :deep(.ant-input-affix-wrapper.form-input:hover) {
  border-color: #40a9ff;
}

.form-item :deep(.ant-input-affix-wrapper.form-input.ant-input-affix-wrapper-focused) {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.form-item :deep(.ant-input-affix-wrapper .ant-input-suffix) {
  display: flex;
  align-items: center;
}

.form-item :deep(.ant-select-selector) {
  height: 30px;
  padding: 0 8px;
}

.form-item :deep(.ant-select-selector .ant-select-selection-item) {
  line-height: 30px;
  font-size: 12px;
}

/* 手机号输入组 */
.phone-input-group {
  display: flex;
  gap: 6px;
  width: 201px;
}

.country-code-select {
  width: 110px;
  flex-shrink: 0;
}

.phone-input {
  flex: 1;
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  height: 30px;
}

.strength-bar {
  flex: 1;
  height: 2px;
  background: #f0f0f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #ff4d4f;
}

.strength-fill.medium {
  background: #faad14;
}

.strength-fill.strong {
  background: #52c41a;
}

.strength-fill.very-strong {
  background: #1890ff;
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
  min-width: 24px;
  line-height: 30px;
}

.strength-text.weak {
  color: #ff4d4f;
}

.strength-text.medium {
  color: #faad14;
}

.strength-text.strong {
  color: #52c41a;
}

.strength-text.very-strong {
  color: #1890ff;
}

/* 错误信息 */
.error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
  line-height: 1.4;
}

/* 服务协议 */
.terms-link {
  color: #1890ff;
  text-decoration: none;
}

.terms-link:hover {
  color: #40a9ff;
  text-decoration: underline;
}

/* 提交按钮 */
.submit-item {
  margin-top: 32px;
  margin-bottom: 16px;
  text-align: center; /* 按钮居中 */
}

.submit-btn {
  width: 122px;
  height: 30px;
  background: #FFA500;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(255, 165, 0, 0.3);
  transition: all 0.3s;
}

.submit-btn:hover {
  background: #FFC107; /* 悬停时颜色变浅 */
  box-shadow: 0 4px 8px rgba(255, 165, 0, 0.4);
  transform: translateY(-1px);
}

.submit-btn:active {
  transform: translateY(0);
}

/* 登录链接 */
.login-link {
  text-align: center;
  color: #666;
  font-size: 12px;
}

.login-btn {
  color: #1890ff;
  padding: 0;
  font-size: 12px;
}

.login-btn:hover {
  color: #40a9ff;
}

/* 页脚 */
.register-footer {
  background: #f8f9fa;
  border-top: 1px solid #e8e8e8;
  padding: 40px 20px 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

.partner-links h4 {
  color: #333;
  font-size: 16px;
  margin-bottom: 16px;
  font-weight: 600;
}

.partner-logos {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.partner-item {
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s;
}

.partner-item:hover {
  color: #1890ff;
}

.official-qr {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 20px;
}

.qr-group {
  display: flex;
  gap: 20px;
}

.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.qr-mini {
  width: 60px;
  height: 60px;
  background: #f0f0f0;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #999;
}

.qr-mini::before {
  content: '二维码';
}

.qr-item span {
  font-size: 12px;
  color: #666;
  text-align: center;
}

.copyright {
  text-align: right;
  color: #999;
  font-size: 12px;
  line-height: 1.6;
}

.copyright p {
  margin: 0;
}

/* 响应式设计 */
 

 

 

 

/* 超小屏幕优化 */
 

/* 表单验证状态 */
.form-item :deep(.ant-form-item-has-error .ant-input),
.form-item :deep(.ant-form-item-has-error .ant-select-selector) {
  border-color: #ff4d4f;
}

.form-item :deep(.ant-form-item-has-error .ant-input:focus),
.form-item :deep(.ant-form-item-has-error .ant-select-focused .ant-select-selector) {
  border-color: #ff4d4f;
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.2);
}

/* 加载状态 */
.submit-btn.ant-btn-loading {
  background: #f5f5f5;
  border-color: #d9d9d9;
  color: #999;
}

.submit-btn {
  height: 30px;
  font-size: 12px;
}

/* 选择框样式 */
.form-input.ant-select .ant-select-selector {
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  transition: all 0.3s;
}

.form-input.ant-select:hover .ant-select-selector {
  border-color: #40a9ff;
}

.form-input.ant-select.ant-select-focused .ant-select-selector {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}
</style>
<style scoped>
.full-width {
  grid-column: 1 / -1;
}
.form-item.full-width :deep(.ant-checkbox-wrapper) {
  margin-left: 105px;
}
.login-link {
  font-size: 12px;
  display: flex;
  align-items: center;
}
.form-item :deep(.ant-form-item-control) {
  overflow: visible;
}

.field-row {
  display: grid;
  grid-template-columns: 201px auto;
  align-items: center;
  column-gap: 12px;
  position: relative;
  z-index: 0;
}

.field-hint {
  color: #fa8c16;
  font-size: 12px;
  line-height: 30px;
  background: transparent;
}

.password-hint {
  padding: 0 6px;
  border-radius: 2px;
}

.username-hint {
  color: #FF7F00;
}

.password-strength.inline {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 使表单在卡片内水平垂直居中 */
.register-form {
  margin: 0 auto;
}
</style>

.form-divider {
  height: 0;
  border-top: 1px dashed #d9d9d9;
  margin: 12px 0;
}

