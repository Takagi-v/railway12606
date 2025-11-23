<template>
  <div class="service-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="header">
        <h1>用户反馈</h1>
        <p class="subtitle">您的意见是我们改进服务的动力，感谢您的宝贵建议</p>
      </div>

      <!-- 提示信息 -->
      <div v-if="showAlert" :class="['alert', alertType]">
        <span class="icon">{{ alertType === 'alert-success' ? '✓' : '✗' }}</span>
        <span>{{ alertMessage }}</span>
      </div>

      <div class="content-section">
        <!-- 反馈统计 -->
        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-number">{{ stats.totalFeedback }}</div>
            <div class="stat-label">总反馈数</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.avgRating }}</div>
            <div class="stat-label">平均评分</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.responseRate }}%</div>
            <div class="stat-label">回复率</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.avgResponseTime }}h</div>
            <div class="stat-label">平均回复时间</div>
          </div>
        </div>

        <div class="main-content">
          <!-- 反馈表单 -->
          <div class="feedback-form">
            <h2>提交反馈</h2>

            <form @submit.prevent="submitFeedback">
              <!-- 反馈类型 -->
              <div class="form-group">
                <label>
                  反馈类型
                  <span class="required">*</span>
                </label>
                <div class="feedback-types">
                  <label
                    v-for="type in feedbackTypes"
                    :key="type.value"
                    :class="['type-option', { selected: form.type === type.value }]"
                  >
                    <input
                      type="radio"
                      :value="type.value"
                      v-model="form.type"
                      style="display: none"
                    />
                    <span class="type-icon">{{ type.icon }}</span>
                    <span class="type-label">{{ type.label }}</span>
                  </label>
                </div>
                <div v-if="errors.type" class="error-text">{{ errors.type }}</div>
              </div>

              <!-- 服务评分 -->
              <div class="form-group">
                <label>
                  服务评分
                  <span class="required">*</span>
                </label>
                <div class="rating-section">
                  <div class="stars">
                    <span
                      v-for="star in 5"
                      :key="star"
                      :class="['star', { active: star <= form.rating }]"
                      @click="form.rating = star"
                      @mouseover="hoverRating = star"
                      @mouseleave="hoverRating = 0"
                    >
                      ★
                    </span>
                  </div>
                  <span class="rating-text">{{ getRatingText(form.rating) }}</span>
                </div>
                <div v-if="errors.rating" class="error-text">{{ errors.rating }}</div>
              </div>

              <!-- 联系信息 -->
              <div class="form-row">
                <div class="form-group">
                  <label>
                    姓名
                    <span class="required">*</span>
                  </label>
                  <input
                    type="text"
                    v-model="form.name"
                    :class="{ error: errors.name }"
                    placeholder="请输入您的姓名"
                  />
                  <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
                </div>

                <div class="form-group">
                  <label>
                    联系电话
                    <span class="required">*</span>
                  </label>
                  <input
                    type="tel"
                    v-model="form.phone"
                    :class="{ error: errors.phone }"
                    placeholder="请输入手机号码"
                  />
                  <div v-if="errors.phone" class="error-text">{{ errors.phone }}</div>
                </div>
              </div>

              <div class="form-group">
                <label>电子邮箱</label>
                <input
                  type="email"
                  v-model="form.email"
                  :class="{ error: errors.email }"
                  placeholder="请输入邮箱地址（选填）"
                />
                <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
              </div>

              <!-- 反馈内容 -->
              <div class="form-group">
                <label>
                  反馈内容
                  <span class="required">*</span>
                </label>
                <textarea
                  v-model="form.content"
                  :class="{ error: errors.content }"
                  placeholder="请详细描述您的问题、建议或意见..."
                  rows="6"
                ></textarea>
                <div class="char-count">{{ form.content.length }}/500</div>
                <div v-if="errors.content" class="error-text">{{ errors.content }}</div>
              </div>

              <!-- 相关信息 -->
              <div class="form-row">
                <div class="form-group">
                  <label>相关车次/车站</label>
                  <input
                    type="text"
                    v-model="form.relatedInfo"
                    placeholder="如：G1234次列车、北京南站"
                  />
                </div>

                <div class="form-group">
                  <label>发生时间</label>
                  <input type="datetime-local" v-model="form.occurTime" />
                </div>
              </div>

              <!-- 文件上传 -->
              <div class="form-group">
                <label>相关图片</label>
                <div class="upload-area" @click="triggerFileUpload">
                  <input
                    ref="fileInput"
                    type="file"
                    multiple
                    accept="image/*"
                    @change="handleFileUpload"
                    style="display: none"
                  />
                  <div class="upload-content">
                    <span class="upload-icon">📷</span>
                    <span>点击上传图片（可选）</span>
                    <span class="upload-hint">支持 JPG、PNG 格式，最多3张</span>
                  </div>
                </div>

                <!-- 已上传文件预览 -->
                <div v-if="uploadedFiles.length > 0" class="uploaded-files">
                  <div v-for="(file, index) in uploadedFiles" :key="index" class="file-preview">
                    <img :src="file.preview" :alt="file.name" />
                    <button type="button" @click="removeFile(index)" class="remove-file">×</button>
                  </div>
                </div>
              </div>

              <!-- 隐私协议 -->
              <div class="form-group">
                <label class="checkbox-label">
                  <input
                    type="checkbox"
                    v-model="form.agreePrivacy"
                    :class="{ error: errors.agreePrivacy }"
                  />
                  <span class="checkmark"></span>
                  我已阅读并同意
                  <a href="#" class="privacy-link">隐私政策</a>
                  和服务条款
                </label>
                <div v-if="errors.agreePrivacy" class="error-text">{{ errors.agreePrivacy }}</div>
              </div>

              <!-- 提交按钮 -->
              <button type="submit" :disabled="loading" class="submit-btn">
                <div v-if="loading" class="loading-spinner"></div>
                <span>{{ loading ? '提交中...' : '提交反馈' }}</span>
              </button>
            </form>
          </div>

          <!-- 反馈指南 -->
          <div class="feedback-guide">
            <h3>反馈指南</h3>

            <div class="guide-section">
              <h4>📝 如何写好反馈</h4>
              <ul>
                <li>详细描述问题的具体情况</li>
                <li>提供相关的时间、地点信息</li>
                <li>如有可能，请提供相关图片</li>
                <li>保持客观、理性的表达</li>
              </ul>
            </div>

            <div class="guide-section">
              <h4>⏰ 处理时效</h4>
              <ul>
                <li>一般问题：1-3个工作日</li>
                <li>紧急问题：24小时内</li>
                <li>投诉建议：3-7个工作日</li>
                <li>表扬感谢：及时回复</li>
              </ul>
            </div>

            <div class="guide-section">
              <h4>📞 其他联系方式</h4>
              <div class="contact-methods">
                <div class="contact-item">
                  <span class="contact-icon">📞</span>
                  <div>
                    <div class="contact-title">客服热线</div>
                    <div class="contact-info">12306</div>
                  </div>
                </div>
                <div class="contact-item">
                  <span class="contact-icon">💬</span>
                  <div>
                    <div class="contact-title">在线客服</div>
                    <div class="contact-info">24小时在线</div>
                  </div>
                </div>
                <div class="contact-item">
                  <span class="contact-icon">📧</span>
                  <div>
                    <div class="contact-title">邮箱反馈</div>
                    <div class="contact-info">feedback@12306.cn</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

// 响应式数据
const loading = ref(false)
const showAlert = ref(false)
const alertType = ref('')
const alertMessage = ref('')
const hoverRating = ref(0)
const fileInput = ref(null)
const uploadedFiles = ref([])

// 统计数据
const stats = reactive({
  totalFeedback: 15847,
  avgRating: 4.6,
  responseRate: 98,
  avgResponseTime: 2.5
})

// 反馈类型
const feedbackTypes = [
  { value: 'complaint', label: '投诉', icon: '😞' },
  { value: 'suggestion', label: '建议', icon: '💡' },
  { value: 'praise', label: '表扬', icon: '👍' },
  { value: 'inquiry', label: '咨询', icon: '❓' },
  { value: 'other', label: '其他', icon: '📝' }
]

// 表单数据
const form = reactive({
  type: '',
  rating: 0,
  name: '',
  phone: '',
  email: '',
  content: '',
  relatedInfo: '',
  occurTime: '',
  agreePrivacy: false
})

// 表单验证错误
const errors = reactive({})

// 表单验证规则
const validateForm = () => {
  const newErrors = {}

  if (!form.type) {
    newErrors.type = '请选择反馈类型'
  }

  if (!form.rating) {
    newErrors.rating = '请给出服务评分'
  }

  if (!form.name.trim()) {
    newErrors.name = '请输入姓名'
  }

  if (!form.phone.trim()) {
    newErrors.phone = '请输入联系电话'
  } else if (!/^1[3-9]\d{9}$/.test(form.phone)) {
    newErrors.phone = '请输入正确的手机号码'
  }

  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    newErrors.email = '请输入正确的邮箱地址'
  }

  if (!form.content.trim()) {
    newErrors.content = '请输入反馈内容'
  } else if (form.content.length > 500) {
    newErrors.content = '反馈内容不能超过500字'
  }

  if (!form.agreePrivacy) {
    newErrors.agreePrivacy = '请同意隐私政策和服务条款'
  }

  Object.keys(errors).forEach(key => {
    delete errors[key]
  })
  Object.assign(errors, newErrors)

  return Object.keys(newErrors).length === 0
}

// 获取评分文本
const getRatingText = rating => {
  const texts = ['', '很不满意', '不满意', '一般', '满意', '非常满意']
  return texts[rating] || ''
}

// 文件上传处理
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = event => {
  const files = Array.from(event.target.files)

  if (uploadedFiles.value.length + files.length > 3) {
    showAlertMessage('最多只能上传3张图片', 'alert-error')
    return
  }

  files.forEach(file => {
    if (file.size > 5 * 1024 * 1024) {
      showAlertMessage('图片大小不能超过5MB', 'alert-error')
      return
    }

    const reader = new FileReader()
    reader.onload = e => {
      uploadedFiles.value.push({
        name: file.name,
        preview: e.target.result,
        file: file
      })
    }
    reader.readAsDataURL(file)
  })
}

const removeFile = index => {
  uploadedFiles.value.splice(index, 1)
}

// 显示提示信息
const showAlertMessage = (message, type) => {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
  setTimeout(() => {
    showAlert.value = false
  }, 3000)
}

// 提交反馈
const submitFeedback = async () => {
  if (!validateForm()) {
    showAlertMessage('请检查表单信息', 'alert-error')
    return
  }

  loading.value = true

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))

    // 重置表单
    Object.keys(form).forEach(key => {
      if (typeof form[key] === 'boolean') {
        form[key] = false
      } else if (typeof form[key] === 'number') {
        form[key] = 0
      } else {
        form[key] = ''
      }
    })
    uploadedFiles.value = []

    showAlertMessage('反馈提交成功！我们会尽快处理您的反馈', 'alert-success')

    // 更新统计数据
    stats.totalFeedback++
  } catch (error) {
    showAlertMessage('提交失败，请稍后重试', 'alert-error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.service-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
}

/* 提示框样式 */
.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  margin: 20px 40px;
  border-radius: 8px;
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert .icon {
  font-size: 1.2rem;
  font-weight: bold;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-section {
  padding: 40px;
}

/* 统计卡片样式 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  border: 2px solid #667eea;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  color: #666;
  font-weight: 500;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

/* 表单样式 */
.feedback-form {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
}

.feedback-form h2 {
  margin: 0 0 25px 0;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 25px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.required {
  color: #e74c3c;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input.error,
.form-group textarea.error,
.form-group select.error {
  border-color: #e74c3c;
  background: #fdf2f2;
}

.error-text {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 4px;
}

/* 反馈类型选择 */
.feedback-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
}

.type-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.type-option:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.type-option.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.type-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.type-label {
  font-weight: 500;
  font-size: 0.9rem;
}

/* 评分系统 */
.rating-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stars {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 2rem;
  color: #ddd;
  cursor: pointer;
  transition: color 0.2s ease;
}

.star.active,
.star:hover {
  color: #ffc107;
}

.rating-text {
  font-weight: 500;
  color: #667eea;
}

/* 字符计数 */
.char-count {
  text-align: right;
  font-size: 0.875rem;
  color: #666;
  margin-top: 5px;
}

/* 文件上传 */
.upload-area {
  border: 2px dashed #e1e8ed;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.upload-icon {
  font-size: 2rem;
}

.upload-hint {
  font-size: 0.875rem;
  color: #666;
}

.uploaded-files {
  display: flex;
  gap: 15px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.file-preview {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #e1e8ed;
}

.file-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-file {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 24px;
  height: 24px;
  border: none;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 复选框样式 */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: normal !important;
}

.checkbox-label input[type='checkbox'] {
  width: auto;
  margin: 0;
}

.privacy-link {
  color: #667eea;
  text-decoration: none;
}

.privacy-link:hover {
  text-decoration: underline;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 16px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 52px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 反馈指南样式 */
.feedback-guide {
  background: white;
  padding: 30px;
  border-radius: 12px;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.feedback-guide h3 {
  margin: 0 0 25px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.guide-section {
  margin-bottom: 25px;
}

.guide-section h4 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.guide-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.guide-section li {
  padding: 5px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.guide-section li::before {
  content: '•';
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.contact-icon {
  font-size: 1.5rem;
}

.contact-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.contact-info {
  color: #667eea;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .feedback-guide {
    position: static;
    order: -1;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .service-page {
    padding: 10px;
  }

  .container {
    margin: 0 10px;
    border-radius: 12px;
  }

  .header {
    padding: 30px 20px;
  }

  .header h1 {
    font-size: 2rem;
  }

  .content-section {
    padding: 20px;
  }

  .alert {
    margin: 20px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .feedback-types {
    grid-template-columns: repeat(2, 1fr);
  }

  .stats-section {
    grid-template-columns: 1fr;
  }

  .rating-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .feedback-form,
  .feedback-guide {
    padding: 20px;
  }

  .feedback-types {
    grid-template-columns: 1fr;
  }

  .type-option {
    flex-direction: row;
    justify-content: flex-start;
    padding: 15px;
  }

  .type-icon {
    margin-bottom: 0;
    margin-right: 10px;
  }

  .contact-methods {
    gap: 10px;
  }

  .contact-item {
    padding: 12px;
  }
}

/* 无障碍支持 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .form-group input,
  .form-group textarea,
  .form-group select,
  .type-option,
  .upload-area {
    border-width: 2px;
  }

  .submit-btn {
    border: 2px solid white;
  }
}

/* 打印样式 */
@media print {
  .service-page {
    background: white;
    padding: 0;
  }

  .container {
    box-shadow: none;
    border-radius: 0;
  }

  .header {
    background: white;
    color: black;
  }

  .submit-btn,
  .alert,
  .upload-area {
    display: none;
  }
}
</style>
