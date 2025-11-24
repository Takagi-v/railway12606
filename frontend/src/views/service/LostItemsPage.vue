<template>
  <div class="service-page">
    <div class="container">
      <div class="header">
        <h1>遗失物品查找</h1>
        <p class="subtitle">帮助您查找在车站或列车上遗失的物品，我们将尽力协助您找回失物</p>
      </div>

      <!-- 成功提示 -->
      <div v-if="showSuccess" class="alert alert-success">
        <i class="icon">✓</i>
        <span>查找申请提交成功！我们将在48小时内与您联系告知查找结果。</span>
      </div>

      <!-- 错误提示 -->
      <div v-if="showError" class="alert alert-error">
        <i class="icon">⚠</i>
        <span>{{ errorMessage }}</span>
      </div>

      <div class="service-content">
        <form @submit.prevent="submitForm" class="service-form">
          <div class="form-group">
            <label for="contact-name">
              联系人姓名
              <span class="required">*</span>
            </label>
            <input
              id="contact-name"
              v-model="form.contactName"
              type="text"
              placeholder="请输入联系人姓名"
              :class="{ error: errors.contactName }"
              @blur="validateField('contactName')"
            />
            <span v-if="errors.contactName" class="error-text">{{ errors.contactName }}</span>
          </div>

          <div class="form-group">
            <label for="phone">
              联系电话
              <span class="required">*</span>
            </label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              placeholder="请输入11位手机号码"
              :class="{ error: errors.phone }"
              @blur="validateField('phone')"
            />
            <span v-if="errors.phone" class="error-text">{{ errors.phone }}</span>
          </div>

          <div class="form-group">
            <label for="lost-date">
              遗失日期
              <span class="required">*</span>
            </label>
            <input
              id="lost-date"
              v-model="form.lostDate"
              type="date"
              :max="maxDate"
              :class="{ error: errors.lostDate }"
              @blur="validateField('lostDate')"
            />
            <span v-if="errors.lostDate" class="error-text">{{ errors.lostDate }}</span>
          </div>

          <div class="form-group">
            <label for="lost-location">
              遗失地点
              <span class="required">*</span>
            </label>
            <select
              id="lost-location"
              v-model="form.lostLocation"
              :class="{ error: errors.lostLocation }"
              @blur="validateField('lostLocation')"
            >
              <option value="">请选择遗失地点</option>
              <option value="waiting-room">车站候车室</option>
              <option value="platform">站台</option>
              <option value="train-carriage">列车车厢</option>
              <option value="train-toilet">列车卫生间</option>
              <option value="dining-car">餐车</option>
              <option value="station-entrance">车站进出口</option>
              <option value="other">其他地点</option>
            </select>
            <span v-if="errors.lostLocation" class="error-text">{{ errors.lostLocation }}</span>
          </div>

          <div v-if="form.lostLocation === 'other'" class="form-group">
            <label for="other-location">请详细说明遗失地点</label>
            <input
              id="other-location"
              v-model="form.otherLocation"
              type="text"
              placeholder="请详细描述遗失地点"
            />
          </div>

          <div v-if="form.lostLocation === 'train-carriage'" class="form-group">
            <label for="train-number">车次号</label>
            <input
              id="train-number"
              v-model="form.trainNumber"
              type="text"
              placeholder="如：G123、D456等"
            />
          </div>

          <div class="form-group">
            <label for="item-description">
              物品描述
              <span class="required">*</span>
            </label>
            <textarea
              id="item-description"
              v-model="form.itemDescription"
              placeholder="请详细描述遗失物品的特征，如：颜色、大小、品牌、型号等"
              :class="{ error: errors.itemDescription }"
              @blur="validateField('itemDescription')"
            ></textarea>
            <span v-if="errors.itemDescription" class="error-text">
              {{ errors.itemDescription }}
            </span>
          </div>

          <div class="form-group">
            <label for="item-value">物品价值（可选）</label>
            <select id="item-value" v-model="form.itemValue">
              <option value="">请选择物品价值范围</option>
              <option value="low">100元以下</option>
              <option value="medium">100-1000元</option>
              <option value="high">1000-5000元</option>
              <option value="very-high">5000元以上</option>
            </select>
          </div>

          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="loading-spinner"></span>
            {{ isSubmitting ? '提交中...' : '提交查找申请' }}
          </button>
        </form>

        <div class="service-info">
          <h3>查找说明</h3>
          <ul>
            <li>失物查找服务免费提供</li>
            <li>我们将在收到申请后48小时内开始查找</li>
            <li>查找结果将通过电话或短信通知您</li>
            <li>找到物品后，请携带有效身份证件前来认领</li>
            <li>物品保管期限为30天，逾期将按相关规定处理</li>
          </ul>

          <div class="contact-info">
            <h4>紧急联系</h4>
            <p>
              如需紧急查找贵重物品，请直接拨打客服热线：
              <strong>12306</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 响应式数据
const form = ref({
  contactName: '',
  phone: '',
  lostDate: '',
  lostLocation: '',
  otherLocation: '',
  trainNumber: '',
  itemDescription: '',
  itemValue: ''
})

const errors = ref({})
const isSubmitting = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

// 计算最大日期（今天）
const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// 表单验证规则
const validateField = field => {
  errors.value[field] = ''

  switch (field) {
    case 'contactName':
      if (!form.value.contactName.trim()) {
        errors.value.contactName = '请输入联系人姓名'
      } else if (form.value.contactName.trim().length < 2) {
        errors.value.contactName = '姓名至少需要2个字符'
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

    case 'lostDate':
      if (!form.value.lostDate) {
        errors.value.lostDate = '请选择遗失日期'
      } else if (new Date(form.value.lostDate) > new Date()) {
        errors.value.lostDate = '遗失日期不能晚于今天'
      }
      break

    case 'lostLocation':
      if (!form.value.lostLocation) {
        errors.value.lostLocation = '请选择遗失地点'
      }
      break

    case 'itemDescription':
      if (!form.value.itemDescription.trim()) {
        errors.value.itemDescription = '请描述遗失物品'
      } else if (form.value.itemDescription.trim().length < 10) {
        errors.value.itemDescription = '请详细描述物品特征（至少10个字符）'
      }
      break
  }
}

// 验证整个表单
const validateForm = () => {
  validateField('contactName')
  validateField('phone')
  validateField('lostDate')
  validateField('lostLocation')
  validateField('itemDescription')

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
      contactName: '',
      phone: '',
      lostDate: '',
      lostLocation: '',
      otherLocation: '',
      trainNumber: '',
      itemDescription: '',
      itemValue: ''
    }
    errors.value = {}

    // 5秒后隐藏成功提示
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
</script>

<style scoped>
.service-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.container {
  max-width: 900px;
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

.service-content {
  padding: 40px;
  display: grid;
  grid-template-columns: 2fr 1fr;
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
  font-size: 0.95rem;
}

.required {
  color: #e74c3c;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 14px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input.error,
.form-group select.error,
.form-group textarea.error {
  border-color: #e74c3c;
  background: #fdf2f2;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
  display: flex;
  align-items: center;
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

/* 服务信息样式 */
.service-info {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
  height: fit-content;
}

.service-info h3 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.service-info h4 {
  color: #2c3e50;
  margin: 25px 0 10px 0;
  font-size: 1.1rem;
  font-weight: 600;
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
  content: '•';
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-info {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  margin-top: 20px;
}

.contact-info p {
  margin: 0;
  color: #555;
  line-height: 1.6;
}

.contact-info strong {
  color: #667eea;
  font-size: 1.1rem;
}

/* 响应式设计 */
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

  .service-content {
    grid-template-columns: 1fr;
    padding: 20px;
    gap: 30px;
  }

  .alert {
    margin: 20px;
  }

  .service-info {
    order: -1;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .service-content {
    padding: 15px;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 16px; /* 防止iOS缩放 */
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
  .form-group select,
  .form-group textarea {
    border-width: 2px;
  }

  .submit-btn {
    border: 2px solid white;
  }
}
</style>
