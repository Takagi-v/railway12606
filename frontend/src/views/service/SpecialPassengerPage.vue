<template>
  <div class="service-page">
    <div class="container">
      <div class="header">
        <h1>重点旅客预约</h1>
        <p class="subtitle">为行动不便的旅客提供专门的预约服务，确保您的出行更加便利</p>
      </div>
      
      <!-- 成功提示 -->
      <div v-if="showSuccess" class="alert alert-success">
        <i class="icon">✓</i>
        <span>预约提交成功！我们将在24小时内与您联系确认服务详情。</span>
      </div>

      <!-- 错误提示 -->
      <div v-if="showError" class="alert alert-error">
        <i class="icon">⚠</i>
        <span>{{ errorMessage }}</span>
      </div>

      <div class="service-content">
        <form @submit.prevent="submitForm" class="service-form">
          <div class="form-group">
            <label for="name">姓名 <span class="required">*</span></label>
            <input 
              id="name"
              v-model="form.name"
              type="text" 
              placeholder="请输入真实姓名"
              :class="{ 'error': errors.name }"
              @blur="validateField('name')"
            />
            <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
          </div>

          <div class="form-group">
            <label for="phone">联系电话 <span class="required">*</span></label>
            <input 
              id="phone"
              v-model="form.phone"
              type="tel" 
              placeholder="请输入11位手机号码"
              :class="{ 'error': errors.phone }"
              @blur="validateField('phone')"
            />
            <span v-if="errors.phone" class="error-text">{{ errors.phone }}</span>
          </div>

          <div class="form-group">
            <label for="date">出行日期 <span class="required">*</span></label>
            <input 
              id="date"
              v-model="form.date"
              type="date" 
              :min="minDate"
              :class="{ 'error': errors.date }"
              @blur="validateField('date')"
            />
            <span v-if="errors.date" class="error-text">{{ errors.date }}</span>
          </div>

          <div class="form-group">
            <label for="requirements">特殊需求 <span class="required">*</span></label>
            <textarea 
              id="requirements"
              v-model="form.requirements"
              placeholder="请详细描述您的特殊需求，如：轮椅服务、担架服务、盲人引导等"
              :class="{ 'error': errors.requirements }"
              @blur="validateField('requirements')"
            ></textarea>
            <span v-if="errors.requirements" class="error-text">{{ errors.requirements }}</span>
          </div>

          <div class="form-group">
            <label for="contact-time">联系时间偏好</label>
            <select id="contact-time" v-model="form.contactTime">
              <option value="">请选择方便联系的时间</option>
              <option value="morning">上午 (9:00-12:00)</option>
              <option value="afternoon">下午 (14:00-17:00)</option>
              <option value="evening">晚上 (19:00-21:00)</option>
            </select>
          </div>

          <button 
            type="submit" 
            class="submit-btn"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="loading-spinner"></span>
            {{ isSubmitting ? '提交中...' : '提交预约' }}
          </button>
        </form>

        <div class="service-info">
          <h3>服务说明</h3>
          <ul>
            <li>预约服务免费提供</li>
            <li>请至少提前24小时预约</li>
            <li>我们将在收到预约后24小时内与您联系</li>
            <li>如需紧急服务，请直接拨打客服热线：12306</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const form = ref({
  name: '',
  phone: '',
  date: '',
  requirements: '',
  contactTime: ''
})

const errors = ref({})
const isSubmitting = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

// 计算最小日期（今天）
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// 表单验证规则
const validateField = (field) => {
  errors.value[field] = ''
  
  switch (field) {
    case 'name':
      if (!form.value.name.trim()) {
        errors.value.name = '请输入姓名'
      } else if (form.value.name.trim().length < 2) {
        errors.value.name = '姓名至少需要2个字符'
      }
      break
    
    case 'phone':
      const phoneRegex = /^1[3-9]\d{9}$/
      if (!form.value.phone.trim()) {
        errors.value.phone = '请输入联系电话'
      } else if (!phoneRegex.test(form.value.phone)) {
        errors.value.phone = '请输入正确的11位手机号码'
      }
      break
    
    case 'date':
      if (!form.value.date) {
        errors.value.date = '请选择出行日期'
      } else if (new Date(form.value.date) < new Date()) {
        errors.value.date = '出行日期不能早于今天'
      }
      break
    
    case 'requirements':
      if (!form.value.requirements.trim()) {
        errors.value.requirements = '请描述您的特殊需求'
      } else if (form.value.requirements.trim().length < 10) {
        errors.value.requirements = '请详细描述您的特殊需求（至少10个字符）'
      }
      break
  }
}

// 验证整个表单
const validateForm = () => {
  validateField('name')
  validateField('phone')
  validateField('date')
  validateField('requirements')
  
  return !Object.values(errors.value).some(error => error)
}

// 提交表单
const submitForm = async () => {
  if (!validateForm()) {
    showError.value = true
    errorMessage.value = '请检查并填写所有必填项'
    setTimeout(() => {
      showError.value = false
    }, 3000)
    return
  }

  isSubmitting.value = true
  showError.value = false

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 成功处理
    showSuccess.value = true
    form.value = {
      name: '',
      phone: '',
      date: '',
      requirements: '',
      contactTime: ''
    }
    errors.value = {}
    
    // 3秒后隐藏成功提示
    setTimeout(() => {
      showSuccess.value = false
    }, 5000)
    
  } catch (error) {
    showError.value = true
    errorMessage.value = '提交失败，请稍后重试'
    setTimeout(() => {
      showError.value = false
    }, 3000)
  } finally {
    isSubmitting.value = false
  }
}

// 页面加载时设置默认日期
onMounted(() => {
  // 可以在这里添加页面初始化逻辑
})
</script>

<style scoped>
.service-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.2rem;
  font-weight: 600;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 0;
}

/* 提示框样式 */
.alert {
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  animation: slideIn 0.3s ease-out;
}

.alert-success {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.alert-error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
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

.service-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}

.service-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.required {
  color: #e74c3c;
  margin-left: 4px;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 14px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: #fff;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group input.error,
.form-group textarea.error,
.form-group select.error {
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.form-group textarea {
  min-height: 120px;
  resize: vertical;
  font-family: inherit;
}

.error-text {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 4px;
}

.submit-btn {
  padding: 16px 32px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
  min-width: 160px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #2980b9, #1f5f8b);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.service-info {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.service-info h3 {
  color: #2c3e50;
  margin-bottom: 16px;
  font-size: 1.2rem;
}

.service-info ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.service-info li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.service-info li::before {
  content: "•";
  color: #3498db;
  font-weight: bold;
  position: absolute;
  left: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .service-page {
    padding: 10px;
  }
  
  .container {
    padding: 20px;
    margin: 0 10px;
  }
  
  .header h1 {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    padding: 12px 14px;
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  .submit-btn {
    padding: 14px 24px;
    font-size: 1rem;
    width: 100%;
  }
  
  .service-content {
    gap: 30px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 16px;
    margin: 0 5px;
  }
  
  .header h1 {
    font-size: 1.6rem;
  }
  
  .alert {
    padding: 12px 16px;
    font-size: 0.9rem;
  }
  
  .service-info {
    padding: 20px;
  }
}

/* 无障碍访问优化 */
@media (prefers-reduced-motion: reduce) {
  .alert,
  .submit-btn,
  .loading-spinner {
    animation: none;
    transition: none;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .form-group input,
  .form-group textarea,
  .form-group select {
    border-width: 3px;
  }
  
  .submit-btn {
    border: 2px solid #2c3e50;
  }
}
</style>