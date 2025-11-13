<template>
  <div class="register-page">
    <!-- 顶栏 Header -->
    <header class="register-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo">
            <div class="logo-icon">🚄</div>
            <span class="logo-text">中国铁路12306</span>
          </div>
          <span class="welcome-text">欢迎注册12306</span>
        </div>
        <div class="nav-links">
          <a-button type="link" @click="router.push('/login')">登录</a-button>
          <a-button type="link">帮助</a-button>
        </div>
      </div>
    </header>

    <!-- 蓝色导航条 -->
    <nav class="nav-bar">
      <div class="nav-content">
        <div class="nav-items">
          <div class="nav-item">首页</div>
          <div class="nav-item">车票</div>
          <div class="nav-item">团购服务</div>
          <div class="nav-item">会员服务</div>
          <div class="nav-item">出行指南</div>
          <div class="nav-item">信息查询</div>
        </div>
      </div>
    </nav>

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
                layout="vertical"
                class="register-form"
              >
                <!-- 用户名 -->
                <a-form-item name="username" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      用户名
                    </span>
                  </template>
                  <a-input
                    v-model:value="registerForm.username"
                    placeholder="6~30位字母、数字、'_'、'-'开头"
                    size="large"
                    class="form-input"
                    @blur="clearFieldError('username')"
                  />
                  <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
                </a-form-item>

                <!-- 密码 -->
                <a-form-item name="password" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      密码
                    </span>
                  </template>
                  <a-input-password
                    v-model:value="registerForm.password"
                    placeholder="6-20位，包含字母和数字"
                    size="large"
                    class="form-input"
                    @input="updatePasswordStrength"
                    @blur="clearFieldError('password')"
                  />
                  <!-- 密码强度指示器 -->
                  <div v-if="registerForm.password" class="password-strength">
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
                  <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
                </a-form-item>

                <!-- 再次输入密码 -->
                <a-form-item name="confirmPassword" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      再次输入密码
                    </span>
                  </template>
                  <a-input-password
                    v-model:value="registerForm.confirmPassword"
                    placeholder="请再次输入密码"
                    size="large"
                    class="form-input"
                    @blur="clearFieldError('confirmPassword')"
                  />
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
                  <a-select
                    v-model:value="registerForm.idType"
                    size="large"
                    class="form-input"
                  >
                    <a-select-option value="身份证">身份证</a-select-option>
                    <a-select-option value="护照">护照</a-select-option>
                    <a-select-option value="港澳通行证">港澳通行证</a-select-option>
                    <a-select-option value="台胞证">台胞证</a-select-option>
                  </a-select>
                </a-form-item>

                <!-- 姓名 -->
                <a-form-item name="realName" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      姓名
                    </span>
                  </template>
                  <a-input
                    v-model:value="registerForm.realName"
                    placeholder="与身份证匹配"
                    size="large"
                    class="form-input"
                    @blur="clearFieldError('realName')"
                  />
                  <div v-if="errors.realName" class="error-message">{{ errors.realName }}</div>
                </a-form-item>

                <!-- 证件号码 -->
                <a-form-item name="idNumber" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      证件号码
                    </span>
                  </template>
                  <a-input
                    v-model:value="registerForm.idNumber"
                    placeholder="身份证号码验证格式"
                    size="large"
                    class="form-input"
                    @blur="clearFieldError('idNumber')"
                  />
                  <div v-if="errors.idNumber" class="error-message">{{ errors.idNumber }}</div>
                </a-form-item>

                <!-- 优待（符）类型 -->
                <a-form-item name="userType" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      优待（符）类型
                    </span>
                  </template>
                  <a-select
                    v-model:value="registerForm.userType"
                    size="large"
                    class="form-input"
                  >
                    <a-select-option value="成人">成人</a-select-option>
                    <a-select-option value="学生">学生</a-select-option>
                    <a-select-option value="残疾军人">残疾军人</a-select-option>
                  </a-select>
                </a-form-item>

                <!-- 邮箱 -->
                <a-form-item name="email" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      邮箱
                    </span>
                  </template>
                  <a-input
                    v-model:value="registerForm.email"
                    placeholder="邮箱格式验证"
                    size="large"
                    class="form-input"
                    @blur="clearFieldError('email')"
                  />
                  <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
                </a-form-item>

                <!-- 手机号 -->
                <a-form-item name="phone" class="form-item">
                  <template #label>
                    <span class="required-label">
                      <span class="required-star">*</span>
                      手机号
                    </span>
                  </template>
                  <a-input-group compact class="phone-input-group">
                    <a-form-item-rest>
                      <a-select
                        v-model:value="registerForm.countryCode"
                        size="large"
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
                      placeholder="请填写手机号"
                      size="large"
                      class="phone-input"
                      @blur="clearFieldError('phone')"
                    />
                  </a-input-group>
                  <div v-if="errors.phone" class="error-message">{{ errors.phone }}</div>
                </a-form-item>

                <!-- 服务协议 -->
                <a-form-item name="agreeTerms" class="form-item">
                  <a-checkbox v-model:checked="registerForm.agreeTerms">
                    我已阅读并同意
                    <a href="#" class="terms-link">《用户服务条款》</a>
                    和
                    <a href="#" class="terms-link">《隐私政策》</a>
                  </a-checkbox>
                  <div v-if="errors.agreeTerms" class="error-message">{{ errors.agreeTerms }}</div>
                </a-form-item>

                <!-- 提交按钮 -->
                <a-form-item class="form-item submit-item">
                  <a-button 
                    type="primary" 
                    html-type="submit" 
                    size="large" 
                    block 
                    :loading="loading"
                    class="submit-btn"
                  >
                    下一步
                  </a-button>
                </a-form-item>

                <!-- 登录链接 -->
                <div class="login-link">
                  <span>已有账号？</span>
                  <a-button type="link" @click="router.push('/login')" class="login-btn">
                    立即登录
                  </a-button>
                </div>
              </a-form>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="register-footer">
      <div class="footer-content">
        <!-- 友情链接 -->
        <div class="partner-links">
          <h4>友情链接</h4>
          <div class="partner-logos">
            <div class="partner-item">中国铁路客户服务中心</div>
            <div class="partner-item">中国铁路总公司</div>
            <div class="partner-item">铁路客服中心</div>
          </div>
        </div>

        <!-- 官方二维码 -->
        <div class="official-qr">
          <div class="qr-group">
            <div class="qr-item">
              <div class="qr-mini"></div>
              <span>中国铁路官方微信</span>
            </div>
            <div class="qr-item">
              <div class="qr-mini"></div>
              <span>中国铁路官方微博</span>
            </div>
            <div class="qr-item">
              <div class="qr-mini"></div>
              <span>12306公众号</span>
            </div>
            <div class="qr-item">
              <div class="qr-mini"></div>
              <span>铁路12306</span>
            </div>
          </div>
          <div class="copyright">
            <p>版权所有©中国铁路，未经许可不得转载</p>
            <p>建议使用IE9.0以上浏览器或兼容浏览器</p>
            <p>京公网安备11010802020134号 京ICP备09069690号</p>
          </div>
        </div>
      </div>
    </footer>
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
  font-family: 'Microsoft YaHei', Arial, sans-serif;
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
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-item:hover {
  color: #e6f7ff;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* 主体区域 */
.register-main {
  padding: 40px 20px;
  min-height: calc(100vh - 200px);
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
  width: 100%;
  max-width: 600px;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(90deg, #1890ff 0%, #40a9ff 100%);
  padding: 16px 24px;
  border-bottom: 1px solid #e8e8e8;
}

.card-title {
  color: white;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  text-align: center;
}

.card-body {
  padding: 32px 24px;
}

/* 表单样式 */
.register-form {
  max-width: 100%;
}

.form-item {
  margin-bottom: 20px;
}

.form-item :deep(.ant-form-item-label) {
  padding-bottom: 4px;
}

.required-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: #333;
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
}

.form-input:hover {
  border-color: #40a9ff;
}

.form-input:focus,
.form-input.ant-input-focused {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

/* 手机号输入组 */
.phone-input-group {
  display: flex;
  gap: 8px;
}

.country-code-select {
  width: 140px;
  flex-shrink: 0;
}

.phone-input {
  flex: 1;
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.strength-bar {
  flex: 1;
  height: 4px;
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
}

.submit-btn {
  background: linear-gradient(90deg, #1890ff 0%, #40a9ff 100%);
  border: none;
  border-radius: 6px;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.3);
  transition: all 0.3s;
}

.submit-btn:hover {
  background: linear-gradient(90deg, #40a9ff 0%, #1890ff 100%);
  box-shadow: 0 4px 8px rgba(24, 144, 255, 0.4);
  transform: translateY(-1px);
}

.submit-btn:active {
  transform: translateY(0);
}

/* 登录链接 */
.login-link {
  text-align: center;
  color: #666;
  font-size: 14px;
}

.login-btn {
  color: #1890ff;
  padding: 0;
  font-size: 14px;
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
@media (max-width: 1200px) {
  .main-content {
    padding: 0 20px;
  }
  
  .register-card {
    max-width: 550px;
  }
}

@media (max-width: 1024px) {
  .main-content {
    padding: 0 16px;
  }
  
  .register-card {
    max-width: 500px;
  }
  
  .nav-items {
    gap: 24px;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .official-qr {
    align-items: center;
  }
  
  .copyright {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 8px 16px;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .welcome-text {
    display: none;
  }
  
  .nav-items {
    gap: 16px;
    overflow-x: auto;
    padding-bottom: 4px;
  }
  
  .nav-item {
    white-space: nowrap;
    font-size: 13px;
  }
  
  .register-main {
    padding: 20px 16px;
  }
  
  .register-card {
    margin: 0;
  }
  
  .card-body {
    padding: 24px 16px;
  }
  
  .phone-input-group {
    flex-direction: column;
    gap: 12px;
  }
  
  .country-code-select {
    width: 100%;
  }
  
  .qr-group {
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 8px 12px;
  }
  
  .nav-content {
    padding: 0 12px;
  }
  
  .register-main {
    padding: 16px 12px;
    min-height: calc(100vh - 160px);
  }
  
  .card-body {
    padding: 20px 12px;
  }
  
  .form-item {
    margin-bottom: 16px;
  }
  
  .form-input {
    min-height: 44px; /* 触摸友好的最小高度 */
  }
  
  .submit-btn {
    height: 48px; /* 更大的触摸目标 */
    font-size: 16px;
  }
  
  .submit-item {
    margin-top: 24px;
  }
  
  .qr-group {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .qr-mini {
    width: 50px;
    height: 50px;
  }
  
  /* 改善表单标签在小屏幕上的显示 */
  .required-label {
    font-size: 14px;
  }
  
  /* 优化密码强度指示器 */
  .password-strength {
    margin-top: 8px;
  }
  
  .strength-bar {
    height: 6px;
  }
}

/* 超小屏幕优化 */
@media (max-width: 360px) {
  .register-main {
    padding: 12px 8px;
  }
  
  .card-body {
    padding: 16px 8px;
  }
  
  .card-title {
    font-size: 16px;
  }
  
  .nav-items {
    gap: 12px;
  }
  
  .nav-item {
    font-size: 12px;
    padding: 10px 0;
  }
  
  .qr-group {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  
  .qr-mini {
    width: 45px;
    height: 45px;
  }
}

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

