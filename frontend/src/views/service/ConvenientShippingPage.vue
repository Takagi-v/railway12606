<template>
  <div class="service-page">
    <div class="container">
      <div class="header">
        <h1>便民托运</h1>
        <p class="subtitle">为您提供安全、便捷、高效的行李托运服务，让您的出行更加轻松</p>
      </div>
      
      <!-- 成功提示 -->
      <div v-if="showSuccess" class="alert alert-success">
        <i class="icon">✓</i>
        <span>托运申请提交成功！我们将在1小时内联系您确认取件时间和地点。</span>
      </div>

      <!-- 错误提示 -->
      <div v-if="showError" class="alert alert-error">
        <i class="icon">⚠</i>
        <span>{{ errorMessage }}</span>
      </div>

      <div class="service-content">
        <form @submit.prevent="submitForm" class="service-form">
          <div class="section-title">寄件人信息</div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="sender-name">寄件人姓名 <span class="required">*</span></label>
              <input 
                id="sender-name"
                v-model="form.senderName"
                type="text" 
                placeholder="请输入寄件人姓名"
                :class="{ 'error': errors.senderName }"
                @blur="validateField('senderName')"
              />
              <span v-if="errors.senderName" class="error-text">{{ errors.senderName }}</span>
            </div>

            <div class="form-group">
              <label for="sender-phone">联系电话 <span class="required">*</span></label>
              <input 
                id="sender-phone"
                v-model="form.senderPhone"
                type="tel" 
                placeholder="请输入11位手机号码"
                :class="{ 'error': errors.senderPhone }"
                @blur="validateField('senderPhone')"
              />
              <span v-if="errors.senderPhone" class="error-text">{{ errors.senderPhone }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="sender-address">寄件地址 <span class="required">*</span></label>
            <textarea 
              id="sender-address"
              v-model="form.senderAddress"
              placeholder="请输入详细的寄件地址"
              :class="{ 'error': errors.senderAddress }"
              @blur="validateField('senderAddress')"
            ></textarea>
            <span v-if="errors.senderAddress" class="error-text">{{ errors.senderAddress }}</span>
          </div>

          <div class="section-title">收件人信息</div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="receiver-name">收件人姓名 <span class="required">*</span></label>
              <input 
                id="receiver-name"
                v-model="form.receiverName"
                type="text" 
                placeholder="请输入收件人姓名"
                :class="{ 'error': errors.receiverName }"
                @blur="validateField('receiverName')"
              />
              <span v-if="errors.receiverName" class="error-text">{{ errors.receiverName }}</span>
            </div>

            <div class="form-group">
              <label for="receiver-phone">联系电话 <span class="required">*</span></label>
              <input 
                id="receiver-phone"
                v-model="form.receiverPhone"
                type="tel" 
                placeholder="请输入11位手机号码"
                :class="{ 'error': errors.receiverPhone }"
                @blur="validateField('receiverPhone')"
              />
              <span v-if="errors.receiverPhone" class="error-text">{{ errors.receiverPhone }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="receiver-address">收件地址 <span class="required">*</span></label>
            <textarea 
              id="receiver-address"
              v-model="form.receiverAddress"
              placeholder="请输入详细的收件地址"
              :class="{ 'error': errors.receiverAddress }"
              @blur="validateField('receiverAddress')"
            ></textarea>
            <span v-if="errors.receiverAddress" class="error-text">{{ errors.receiverAddress }}</span>
          </div>

          <div class="section-title">物品信息</div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="item-type">物品类型 <span class="required">*</span></label>
              <select 
                id="item-type" 
                v-model="form.itemType"
                :class="{ 'error': errors.itemType }"
                @blur="validateField('itemType')"
              >
                <option value="">请选择物品类型</option>
                <option value="clothing">服装鞋帽</option>
                <option value="books">书籍文件</option>
                <option value="electronics">电子产品</option>
                <option value="food">食品特产</option>
                <option value="daily-use">日用品</option>
                <option value="gifts">礼品工艺品</option>
                <option value="other">其他物品</option>
              </select>
              <span v-if="errors.itemType" class="error-text">{{ errors.itemType }}</span>
            </div>

            <div class="form-group">
              <label for="item-weight">预估重量 <span class="required">*</span></label>
              <select 
                id="item-weight" 
                v-model="form.itemWeight"
                :class="{ 'error': errors.itemWeight }"
                @blur="validateField('itemWeight')"
              >
                <option value="">请选择重量范围</option>
                <option value="0-5">0-5公斤</option>
                <option value="5-10">5-10公斤</option>
                <option value="10-20">10-20公斤</option>
                <option value="20-50">20-50公斤</option>
                <option value="50+">50公斤以上</option>
              </select>
              <span v-if="errors.itemWeight" class="error-text">{{ errors.itemWeight }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="item-description">物品描述</label>
            <textarea 
              id="item-description"
              v-model="form.itemDescription"
              placeholder="请详细描述托运物品的内容、数量等信息"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="pickup-date">期望取件日期 <span class="required">*</span></label>
              <input 
                id="pickup-date"
                v-model="form.pickupDate"
                type="date" 
                :min="minDate"
                :class="{ 'error': errors.pickupDate }"
                @blur="validateField('pickupDate')"
              />
              <span v-if="errors.pickupDate" class="error-text">{{ errors.pickupDate }}</span>
            </div>

            <div class="form-group">
              <label for="pickup-time">期望取件时间 <span class="required">*</span></label>
              <select 
                id="pickup-time" 
                v-model="form.pickupTime"
                :class="{ 'error': errors.pickupTime }"
                @blur="validateField('pickupTime')"
              >
                <option value="">请选择时间段</option>
                <option value="morning">上午 (8:00-12:00)</option>
                <option value="afternoon">下午 (12:00-18:00)</option>
                <option value="evening">晚上 (18:00-21:00)</option>
              </select>
              <span v-if="errors.pickupTime" class="error-text">{{ errors.pickupTime }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="special-requirements">特殊要求</label>
            <textarea 
              id="special-requirements"
              v-model="form.specialRequirements"
              placeholder="如有特殊包装、运输要求等，请在此说明"
            ></textarea>
          </div>

          <div class="price-estimate" v-if="estimatedPrice">
            <h3>预估费用</h3>
            <div class="price-info">
              <span class="price">¥{{ estimatedPrice }}</span>
              <span class="note">（实际费用以现场确认为准）</span>
            </div>
          </div>

          <button 
            type="submit" 
            class="submit-btn"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="loading-spinner"></span>
            {{ isSubmitting ? '提交中...' : '提交托运申请' }}
          </button>
        </form>

        <div class="service-info">
          <h3>服务说明</h3>
          <ul>
            <li>提供上门取件服务，覆盖市区主要区域</li>
            <li>专业包装，确保物品运输安全</li>
            <li>全程跟踪，实时查询物流状态</li>
            <li>支持代收货款服务</li>
            <li>提供保价服务，最高保额10万元</li>
          </ul>
          
          <div class="pricing-info">
            <h4>收费标准</h4>
            <div class="pricing-table">
              <div class="pricing-row">
                <span>0-5公斤</span>
                <span>¥15起</span>
              </div>
              <div class="pricing-row">
                <span>5-10公斤</span>
                <span>¥25起</span>
              </div>
              <div class="pricing-row">
                <span>10-20公斤</span>
                <span>¥35起</span>
              </div>
              <div class="pricing-row">
                <span>20公斤以上</span>
                <span>按重量计费</span>
              </div>
            </div>
          </div>
          
          <div class="contact-info">
            <h4>客服热线</h4>
            <p>如有疑问，请拨打：<strong>400-1234-567</strong></p>
            <p>服务时间：7:00-22:00</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// 响应式数据
const form = ref({
  senderName: '',
  senderPhone: '',
  senderAddress: '',
  receiverName: '',
  receiverPhone: '',
  receiverAddress: '',
  itemType: '',
  itemWeight: '',
  itemDescription: '',
  pickupDate: '',
  pickupTime: '',
  specialRequirements: ''
})

const errors = ref({})
const isSubmitting = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

// 计算最小日期（明天）
const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

// 预估价格计算
const estimatedPrice = computed(() => {
  if (!form.value.itemWeight) return null
  
  const priceMap = {
    '0-5': 15,
    '5-10': 25,
    '10-20': 35,
    '20-50': 50,
    '50+': 80
  }
  
  return priceMap[form.value.itemWeight] || null
})

// 监听重量变化，更新价格
watch(() => form.value.itemWeight, () => {
  // 价格会自动通过computed更新
})

// 表单验证规则
const validateField = (field) => {
  errors.value[field] = ''
  
  switch (field) {
    case 'senderName':
    case 'receiverName':
      if (!form.value[field].trim()) {
        errors.value[field] = '请输入姓名'
      } else if (form.value[field].trim().length < 2) {
        errors.value[field] = '姓名至少需要2个字符'
      }
      break
    
    case 'senderPhone':
    case 'receiverPhone':
      const phoneRegex = /^1[3-9]\d{9}$/
      if (!form.value[field].trim()) {
        errors.value[field] = '请输入联系电话'
      } else if (!phoneRegex.test(form.value[field])) {
        errors.value[field] = '请输入正确的11位手机号码'
      }
      break
    
    case 'senderAddress':
    case 'receiverAddress':
      if (!form.value[field].trim()) {
        errors.value[field] = '请输入地址'
      } else if (form.value[field].trim().length < 10) {
        errors.value[field] = '请输入详细地址（至少10个字符）'
      }
      break
    
    case 'itemType':
      if (!form.value.itemType) {
        errors.value.itemType = '请选择物品类型'
      }
      break
    
    case 'itemWeight':
      if (!form.value.itemWeight) {
        errors.value.itemWeight = '请选择重量范围'
      }
      break
    
    case 'pickupDate':
      if (!form.value.pickupDate) {
        errors.value.pickupDate = '请选择取件日期'
      } else if (new Date(form.value.pickupDate) <= new Date()) {
        errors.value.pickupDate = '取件日期不能早于明天'
      }
      break
    
    case 'pickupTime':
      if (!form.value.pickupTime) {
        errors.value.pickupTime = '请选择取件时间'
      }
      break
  }
}

// 验证整个表单
const validateForm = () => {
  const requiredFields = [
    'senderName', 'senderPhone', 'senderAddress',
    'receiverName', 'receiverPhone', 'receiverAddress',
    'itemType', 'itemWeight', 'pickupDate', 'pickupTime'
  ]
  
  requiredFields.forEach(field => validateField(field))
  
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
      senderName: '',
      senderPhone: '',
      senderAddress: '',
      receiverName: '',
      receiverPhone: '',
      receiverAddress: '',
      itemType: '',
      itemWeight: '',
      itemDescription: '',
      pickupDate: '',
      pickupTime: '',
      specialRequirements: ''
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
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
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
  gap: 30px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 20px 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #667eea;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 50px;
  height: 2px;
  background: #764ba2;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
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
  min-height: 100px;
  resize: vertical;
  font-family: inherit;
}

.error-text {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 4px;
}

/* 价格预估样式 */
.price-estimate {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #667eea;
  margin: 20px 0;
}

.price-estimate h3 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.price-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.price {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
}

.note {
  color: #666;
  font-size: 0.9rem;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 服务信息样式 */
.service-info {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.service-info h3 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.service-info h4 {
  color: #2c3e50;
  margin: 25px 0 15px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.service-info ul {
  list-style: none;
  padding: 0;
  margin: 0 0 25px 0;
}

.service-info li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.service-info li::before {
  content: "•";
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.pricing-info {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.pricing-table {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pricing-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.pricing-row:last-child {
  border-bottom: none;
}

.pricing-row span:first-child {
  color: #555;
}

.pricing-row span:last-child {
  font-weight: 600;
  color: #667eea;
}

.contact-info {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.contact-info p {
  margin: 5px 0;
  color: #555;
  line-height: 1.6;
}

.contact-info strong {
  color: #667eea;
  font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .service-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .service-info {
    position: static;
    order: -1;
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
  
  .service-content {
    padding: 20px;
  }
  
  .alert {
    margin: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .section-title {
    font-size: 1.2rem;
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
  
  .price {
    font-size: 1.5rem;
  }
  
  .price-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
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
  
  .section-title {
    border-bottom-width: 3px;
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
  .alert {
    display: none;
  }
}
</style>