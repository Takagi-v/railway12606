<template>
  <div class="form-demo">
    <div class="demo-header">
      <h1>12306 风格表单组件演示</h1>
      <p>展示基于 Ant Design Vue 定制的 12306 风格表单组件</p>
    </div>

    <div class="demo-content">
      <!-- 登录表单演示 -->
      <div class="demo-section">
        <h2>登录表单</h2>
        <div class="demo-card">
          <LoginForm />
        </div>
      </div>

      <!-- 车票搜索表单演示 -->
      <div class="demo-section">
        <h2>车票搜索表单</h2>
        <div class="demo-card">
          <TicketSearchForm />
        </div>
      </div>

      <!-- 基础表单组件演示 -->
      <div class="demo-section">
        <h2>基础表单组件</h2>
        <div class="demo-card">
          <BaseForm
            :form-data="demoFormData"
            :rules="demoRules"
            layout="vertical"
            @submit="handleDemoSubmit"
            @reset="handleDemoReset"
          >
            <template #form-items>
              <!-- 文本输入框 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.username"
                    label="用户名"
                    name="username"
                    placeholder="请输入用户名"
                    :required="true"
                  />
                </a-col>
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.email"
                    label="邮箱"
                    name="email"
                    type="email"
                    placeholder="请输入邮箱地址"
                    :required="true"
                  />
                </a-col>
              </a-row>

              <!-- 密码输入框 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.password"
                    label="密码"
                    name="password"
                    type="password"
                    placeholder="请输入密码"
                    :required="true"
                  />
                </a-col>
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.phone"
                    label="手机号"
                    name="phone"
                    type="tel"
                    placeholder="请输入手机号"
                    :required="true"
                  />
                </a-col>
              </a-row>

              <!-- 选择器 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <FormSelect
                    v-model:value="demoFormData.city"
                    label="城市"
                    name="city"
                    placeholder="请选择城市"
                    :options="cityOptions"
                    :required="true"
                  />
                </a-col>
                <a-col :span="12">
                  <FormSelect
                    v-model:value="demoFormData.hobbies"
                    label="兴趣爱好"
                    name="hobbies"
                    placeholder="请选择兴趣爱好"
                    :options="hobbyOptions"
                    mode="multiple"
                    :max-tag-count="2"
                  />
                </a-col>
              </a-row>

              <!-- 日期选择器 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <FormDatePicker
                    v-model:value="demoFormData.birthday"
                    label="生日"
                    name="birthday"
                    placeholder="请选择生日"
                    :required="true"
                  />
                </a-col>
                <a-col :span="12">
                  <FormDatePicker
                    v-model:value="demoFormData.travelDate"
                    label="出行日期"
                    name="travelDate"
                    type="range"
                    placeholder="请选择出行日期范围"
                  />
                </a-col>
              </a-row>

              <!-- 文本域 -->
              <FormInput
                v-model:value="demoFormData.description"
                label="个人描述"
                name="description"
                type="textarea"
                placeholder="请输入个人描述"
                :rows="4"
              />

              <!-- 数字输入框 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.age"
                    label="年龄"
                    name="age"
                    type="number"
                    placeholder="请输入年龄"
                    :min="1"
                    :max="120"
                  />
                </a-col>
                <a-col :span="12">
                  <FormInput
                    v-model:value="demoFormData.salary"
                    label="期望薪资"
                    name="salary"
                    type="number"
                    placeholder="请输入期望薪资"
                    :min="0"
                    :step="1000"
                    addon-after="元/月"
                  />
                </a-col>
              </a-row>

              <!-- 其他组件演示 -->
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-form-item label="性别" name="gender">
                    <a-radio-group v-model:value="demoFormData.gender" class="radio-railway">
                      <a-radio value="male">男</a-radio>
                      <a-radio value="female">女</a-radio>
                    </a-radio-group>
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item label="接收通知" name="notifications">
                    <a-checkbox-group
                      v-model:value="demoFormData.notifications"
                      class="checkbox-railway"
                    >
                      <a-checkbox value="email">邮件</a-checkbox>
                      <a-checkbox value="sms">短信</a-checkbox>
                      <a-checkbox value="push">推送</a-checkbox>
                    </a-checkbox-group>
                  </a-form-item>
                </a-col>
                <a-col :span="8">
                  <a-form-item label="启用账户" name="enabled">
                    <a-switch v-model:checked="demoFormData.enabled" class="switch-railway" />
                  </a-form-item>
                </a-col>
              </a-row>

              <!-- 滑块和评分 -->
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-form-item label="满意度评分" name="rating">
                    <a-rate v-model:value="demoFormData.rating" class="rate-railway" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="价格范围" name="priceRange">
                    <a-slider
                      v-model:value="demoFormData.priceRange"
                      range
                      :min="0"
                      :max="10000"
                      :step="100"
                      class="slider-railway"
                    />
                  </a-form-item>
                </a-col>
              </a-row>
            </template>

            <template #form-actions>
              <a-space>
                <a-button type="primary" html-type="submit" class="btn-railway-primary">
                  提交表单
                </a-button>
                <a-button html-type="reset">重置表单</a-button>
                <a-button @click="fillDemoData">填充示例数据</a-button>
              </a-space>
            </template>
          </BaseForm>
        </div>
      </div>

      <!-- 主题色彩展示 -->
      <div class="demo-section">
        <h2>主题色彩</h2>
        <div class="demo-card">
          <div class="color-palette">
            <div class="color-item">
              <div class="color-block primary"></div>
              <span>主色调 #4A90E2</span>
            </div>
            <div class="color-item">
              <div class="color-block success"></div>
              <span>成功色 #52C41A</span>
            </div>
            <div class="color-item">
              <div class="color-block warning"></div>
              <span>警告色 #FAAD14</span>
            </div>
            <div class="color-item">
              <div class="color-block error"></div>
              <span>错误色 #FF4D4F</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { message } from 'ant-design-vue'
import BaseForm from '@/components/form/BaseForm.vue'
import FormInput from '@/components/form/FormInput.vue'
import FormSelect from '@/components/form/FormSelect.vue'
import FormDatePicker from '@/components/form/FormDatePicker.vue'
import LoginForm from '@/components/form/examples/LoginForm.vue'
import TicketSearchForm from '@/components/form/examples/TicketSearchForm.vue'

// 演示表单数据
const demoFormData = reactive({
  username: '',
  email: '',
  password: '',
  phone: '',
  city: undefined,
  hobbies: [],
  birthday: null,
  travelDate: null,
  description: '',
  age: undefined,
  salary: undefined,
  gender: 'male',
  notifications: ['email'],
  enabled: true,
  rating: 5,
  priceRange: [2000, 8000]
})

// 演示表单验证规则
const demoRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ],
  city: [{ required: true, message: '请选择城市', trigger: 'change' }],
  birthday: [{ required: true, message: '请选择生日', trigger: 'change' }]
}

// 选项数据
const cityOptions = [
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广州', value: 'guangzhou' },
  { label: '深圳', value: 'shenzhen' },
  { label: '杭州', value: 'hangzhou' },
  { label: '南京', value: 'nanjing' },
  { label: '武汉', value: 'wuhan' },
  { label: '成都', value: 'chengdu' }
]

const hobbyOptions = [
  { label: '阅读', value: 'reading' },
  { label: '旅行', value: 'travel' },
  { label: '摄影', value: 'photography' },
  { label: '音乐', value: 'music' },
  { label: '运动', value: 'sports' },
  { label: '编程', value: 'coding' },
  { label: '绘画', value: 'painting' },
  { label: '烹饪', value: 'cooking' }
]

// 事件处理
const handleDemoSubmit = values => {
  console.log('表单提交数据:', values)
  message.success('表单提交成功！')
}

const handleDemoReset = () => {
  console.log('表单重置')
  message.info('表单已重置')
}

const fillDemoData = () => {
  Object.assign(demoFormData, {
    username: 'demo_user',
    email: 'demo@example.com',
    password: '123456',
    phone: '13800138000',
    city: 'beijing',
    hobbies: ['reading', 'travel'],
    birthday: '1990-01-01',
    description: '这是一个演示用户的个人描述信息。',
    age: 30,
    salary: 15000,
    gender: 'male',
    notifications: ['email', 'sms'],
    enabled: true,
    rating: 4,
    priceRange: [3000, 7000]
  })
  message.success('示例数据已填充！')
}
</script>

<style scoped>
.form-demo {
  min-height: 100vh;
  background: var(--color-bg-layout);
  padding: 24px;
}

.demo-header {
  text-align: center;
  margin-bottom: 48px;
  padding: 48px 0;
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  color: white;
  border-radius: 8px;
}

.demo-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 16px;
}

.demo-header p {
  font-size: 16px;
  opacity: 0.9;
}

.demo-content {
  max-width: 1200px;
  margin: 0 auto;
}

.demo-section {
  margin-bottom: 48px;
}

.demo-section h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--color-primary);
}

.demo-card {
  background: white;
  border-radius: 8px;
  padding: 32px;
  box-shadow: var(--box-shadow);
  border: 1px solid var(--color-border);
}

.color-palette {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.color-block {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.color-block.primary {
  background-color: var(--color-primary);
}

.color-block.success {
  background-color: var(--color-success);
}

.color-block.warning {
  background-color: var(--color-warning);
}

.color-block.error {
  background-color: var(--color-error);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-demo {
    padding: 16px;
  }

  .demo-header {
    padding: 32px 16px;
  }

  .demo-header h1 {
    font-size: 24px;
  }

  .demo-card {
    padding: 24px 16px;
  }

  .color-palette {
    justify-content: center;
  }
}
</style>
