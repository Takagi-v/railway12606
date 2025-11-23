<template>
  <div class="service-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="header">
        <h1>候补购票</h1>
        <p class="subtitle">
          当您需要的车票暂时售完时，可提交候补订单，我们将在有退票时自动为您购买
        </p>
      </div>

      <!-- 提示信息 -->
      <div v-if="showAlert" :class="['alert', alertType]">
        <span class="icon">{{ alertType === 'alert-success' ? '✓' : '✗' }}</span>
        <span>{{ alertMessage }}</span>
      </div>

      <div class="content-section">
        <!-- 功能导航 -->
        <div class="nav-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['tab-btn', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>
          </button>
        </div>

        <!-- 候补购票表单 -->
        <div v-if="activeTab === 'submit'" class="tab-content">
          <div class="main-content">
            <div class="waitlist-form">
              <h2>提交候补订单</h2>

              <form @submit.prevent="submitWaitlist">
                <!-- 行程信息 -->
                <div class="section-title">
                  <span class="icon">🚄</span>
                  <span>行程信息</span>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>
                      出发城市
                      <span class="required">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.departure"
                      :class="{ error: errors.departure }"
                      placeholder="请输入出发城市"
                      @input="searchStations('departure', $event.target.value)"
                    />
                    <div v-if="departureStations.length > 0" class="suggestions">
                      <div
                        v-for="station in departureStations"
                        :key="station"
                        class="suggestion-item"
                        @click="selectStation('departure', station)"
                      >
                        {{ station }}
                      </div>
                    </div>
                    <div v-if="errors.departure" class="error-text">{{ errors.departure }}</div>
                  </div>

                  <div class="form-group">
                    <label>
                      到达城市
                      <span class="required">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.arrival"
                      :class="{ error: errors.arrival }"
                      placeholder="请输入到达城市"
                      @input="searchStations('arrival', $event.target.value)"
                    />
                    <div v-if="arrivalStations.length > 0" class="suggestions">
                      <div
                        v-for="station in arrivalStations"
                        :key="station"
                        class="suggestion-item"
                        @click="selectStation('arrival', station)"
                      >
                        {{ station }}
                      </div>
                    </div>
                    <div v-if="errors.arrival" class="error-text">{{ errors.arrival }}</div>
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>
                      出发日期
                      <span class="required">*</span>
                    </label>
                    <input
                      type="date"
                      v-model="form.date"
                      :class="{ error: errors.date }"
                      :min="minDate"
                      :max="maxDate"
                    />
                    <div v-if="errors.date" class="error-text">{{ errors.date }}</div>
                  </div>

                  <div class="form-group">
                    <label>车次类型</label>
                    <select v-model="form.trainType">
                      <option value="">不限</option>
                      <option value="G">高速动车组(G)</option>
                      <option value="D">动车组(D)</option>
                      <option value="C">城际动车组(C)</option>
                      <option value="Z">直达特快(Z)</option>
                      <option value="T">特快(T)</option>
                      <option value="K">快速(K)</option>
                    </select>
                  </div>
                </div>

                <!-- 座席选择 -->
                <div class="section-title">
                  <span class="icon">💺</span>
                  <span>座席选择</span>
                </div>

                <div class="seat-types">
                  <label
                    v-for="seat in seatTypes"
                    :key="seat.value"
                    :class="['seat-option', { selected: form.seatTypes.includes(seat.value) }]"
                  >
                    <input
                      type="checkbox"
                      :value="seat.value"
                      v-model="form.seatTypes"
                      style="display: none"
                    />
                    <span class="seat-icon">{{ seat.icon }}</span>
                    <div class="seat-info">
                      <div class="seat-name">{{ seat.label }}</div>
                      <div class="seat-price">约 ¥{{ seat.price }}</div>
                    </div>
                  </label>
                </div>
                <div v-if="errors.seatTypes" class="error-text">{{ errors.seatTypes }}</div>

                <!-- 乘客信息 -->
                <div class="section-title">
                  <span class="icon">👥</span>
                  <span>乘客信息</span>
                </div>

                <div class="passengers-section">
                  <div
                    v-for="(passenger, index) in form.passengers"
                    :key="index"
                    class="passenger-card"
                  >
                    <div class="passenger-header">
                      <span class="passenger-title">乘客 {{ index + 1 }}</span>
                      <button
                        v-if="form.passengers.length > 1"
                        type="button"
                        @click="removePassenger(index)"
                        class="remove-passenger"
                      >
                        删除
                      </button>
                    </div>

                    <div class="form-row">
                      <div class="form-group">
                        <label>
                          姓名
                          <span class="required">*</span>
                        </label>
                        <input
                          type="text"
                          v-model="passenger.name"
                          :class="{ error: errors[`passenger_${index}_name`] }"
                          placeholder="请输入乘客姓名"
                        />
                        <div v-if="errors[`passenger_${index}_name`]" class="error-text">
                          {{ errors[`passenger_${index}_name`] }}
                        </div>
                      </div>

                      <div class="form-group">
                        <label>
                          证件类型
                          <span class="required">*</span>
                        </label>
                        <select v-model="passenger.idType">
                          <option value="身份证">身份证</option>
                          <option value="护照">护照</option>
                          <option value="港澳通行证">港澳通行证</option>
                          <option value="台湾通行证">台湾通行证</option>
                        </select>
                      </div>

                      <div class="form-group">
                        <label>
                          证件号码
                          <span class="required">*</span>
                        </label>
                        <input
                          type="text"
                          v-model="passenger.idNumber"
                          :class="{ error: errors[`passenger_${index}_idNumber`] }"
                          placeholder="请输入证件号码"
                        />
                        <div v-if="errors[`passenger_${index}_idNumber`]" class="error-text">
                          {{ errors[`passenger_${index}_idNumber`] }}
                        </div>
                      </div>
                    </div>

                    <div class="form-row">
                      <div class="form-group">
                        <label>
                          手机号码
                          <span class="required">*</span>
                        </label>
                        <input
                          type="tel"
                          v-model="passenger.phone"
                          :class="{ error: errors[`passenger_${index}_phone`] }"
                          placeholder="请输入手机号码"
                        />
                        <div v-if="errors[`passenger_${index}_phone`]" class="error-text">
                          {{ errors[`passenger_${index}_phone`] }}
                        </div>
                      </div>

                      <div class="form-group">
                        <label>乘客类型</label>
                        <select v-model="passenger.type">
                          <option value="成人">成人</option>
                          <option value="儿童">儿童</option>
                          <option value="学生">学生</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    @click="addPassenger"
                    class="add-passenger-btn"
                    :disabled="form.passengers.length >= 5"
                  >
                    <span class="icon">+</span>
                    <span>添加乘客 (最多5人)</span>
                  </button>
                </div>

                <!-- 候补设置 -->
                <div class="section-title">
                  <span class="icon">⚙️</span>
                  <span>候补设置</span>
                </div>

                <div class="waitlist-settings">
                  <div class="form-group">
                    <label>候补截止时间</label>
                    <select v-model="form.deadline">
                      <option value="1">开车前1小时</option>
                      <option value="2">开车前2小时</option>
                      <option value="6">开车前6小时</option>
                      <option value="12">开车前12小时</option>
                      <option value="24">开车前1天</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label>自动支付</label>
                    <div class="auto-pay-options">
                      <label class="radio-option">
                        <input type="radio" value="true" v-model="form.autoPay" />
                        <span class="radio-mark"></span>
                        <span>开启（推荐）</span>
                      </label>
                      <label class="radio-option">
                        <input type="radio" value="false" v-model="form.autoPay" />
                        <span class="radio-mark"></span>
                        <span>关闭</span>
                      </label>
                    </div>
                    <div class="auto-pay-note">开启后，候补成功将自动扣款，无需手动支付</div>
                  </div>
                </div>

                <!-- 提交按钮 -->
                <button type="submit" :disabled="loading" class="submit-btn">
                  <div v-if="loading" class="loading-spinner"></div>
                  <span>{{ loading ? '提交中...' : '提交候补订单' }}</span>
                </button>
              </form>
            </div>

            <!-- 候补说明 -->
            <div class="waitlist-guide">
              <h3>候补购票说明</h3>

              <div class="guide-section">
                <h4>📋 什么是候补购票</h4>
                <p>
                  当您需要购买的车票售完时，可以提交候补订单。如有退票、改签释放车票，系统将自动为您购买。
                </p>
              </div>

              <div class="guide-section">
                <h4>⏰ 候补时间</h4>
                <ul>
                  <li>候补订单提交后立即生效</li>
                  <li>系统24小时自动监控票源</li>
                  <li>候补截止时间可自定义设置</li>
                  <li>成功后将发送短信通知</li>
                </ul>
              </div>

              <div class="guide-section">
                <h4>💰 费用说明</h4>
                <ul>
                  <li>候补订单提交免费</li>
                  <li>候补成功后按票面价格收费</li>
                  <li>候补失败不收取任何费用</li>
                  <li>支持多种支付方式</li>
                </ul>
              </div>

              <div class="guide-section">
                <h4>📱 状态查询</h4>
                <p>可在"我的订单"中查看候补状态，或关注12306微信公众号接收实时通知。</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 我的候补 -->
        <div v-if="activeTab === 'orders'" class="tab-content">
          <div class="orders-section">
            <div class="orders-header">
              <h2>我的候补订单</h2>
              <div class="filter-options">
                <select v-model="orderFilter">
                  <option value="all">全部状态</option>
                  <option value="waiting">候补中</option>
                  <option value="success">候补成功</option>
                  <option value="failed">候补失败</option>
                  <option value="cancelled">已取消</option>
                </select>
              </div>
            </div>

            <div v-if="filteredOrders.length === 0" class="empty-state">
              <div class="empty-icon">📋</div>
              <div class="empty-text">暂无候补订单</div>
              <button @click="activeTab = 'submit'" class="empty-action">立即提交候补</button>
            </div>

            <div v-else class="orders-list">
              <div v-for="order in filteredOrders" :key="order.id" class="order-card">
                <div class="order-header">
                  <div class="order-info">
                    <span class="order-number">订单号：{{ order.orderNumber }}</span>
                    <span :class="['order-status', order.status]">
                      {{ getStatusText(order.status) }}
                    </span>
                  </div>
                  <div class="order-actions">
                    <button
                      v-if="order.status === 'waiting'"
                      @click="cancelOrder(order.id)"
                      class="cancel-btn"
                    >
                      取消候补
                    </button>
                    <button
                      v-if="order.status === 'success'"
                      @click="payOrder(order.id)"
                      class="pay-btn"
                    >
                      立即支付
                    </button>
                  </div>
                </div>

                <div class="order-content">
                  <div class="route-info">
                    <div class="route-stations">
                      <span class="departure">{{ order.departure }}</span>
                      <span class="arrow">→</span>
                      <span class="arrival">{{ order.arrival }}</span>
                    </div>
                    <div class="route-date">{{ order.date }}</div>
                  </div>

                  <div class="order-details">
                    <div class="detail-item">
                      <span class="label">座席类型：</span>
                      <span class="value">{{ order.seatTypes.join('、') }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">乘客数量：</span>
                      <span class="value">{{ order.passengerCount }}人</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">提交时间：</span>
                      <span class="value">{{ order.submitTime }}</span>
                    </div>
                    <div v-if="order.successTime" class="detail-item">
                      <span class="label">候补成功时间：</span>
                      <span class="value">{{ order.successTime }}</span>
                    </div>
                  </div>

                  <div v-if="order.progress" class="progress-section">
                    <div class="progress-title">候补进度</div>
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: order.progress + '%' }"></div>
                    </div>
                    <div class="progress-text">
                      {{ order.progress }}% - {{ order.progressText }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 候补规则 -->
        <div v-if="activeTab === 'rules'" class="tab-content">
          <div class="rules-section">
            <h2>候补购票规则</h2>

            <div class="rule-category">
              <h3>📝 基本规则</h3>
              <div class="rule-list">
                <div class="rule-item">
                  <div class="rule-title">候补条件</div>
                  <div class="rule-content">
                    <p>• 仅支持发售车票的车次</p>
                    <p>• 每个用户最多可提交5个候补订单</p>
                    <p>• 每个订单最多可添加5名乘客</p>
                    <p>• 候补订单不可修改，如需变更请取消后重新提交</p>
                  </div>
                </div>

                <div class="rule-item">
                  <div class="rule-title">候补时间</div>
                  <div class="rule-content">
                    <p>• 候补订单提交后立即生效</p>
                    <p>• 系统将在您设定的截止时间前持续监控</p>
                    <p>• 开车前30分钟停止候补服务</p>
                    <p>• 候补成功后需在30分钟内完成支付</p>
                  </div>
                </div>

                <div class="rule-item">
                  <div class="rule-title">成功率说明</div>
                  <div class="rule-content">
                    <p>• 候补成功率与车次热门程度相关</p>
                    <p>• 工作日成功率通常高于节假日</p>
                    <p>• 建议选择多个座席类型提高成功率</p>
                    <p>• 提交时间越早，成功概率越高</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="rule-category">
              <h3>💰 费用规则</h3>
              <div class="rule-list">
                <div class="rule-item">
                  <div class="rule-title">收费标准</div>
                  <div class="rule-content">
                    <p>• 候补订单提交完全免费</p>
                    <p>• 候补成功后按实际票价收费</p>
                    <p>• 不收取任何额外手续费</p>
                    <p>• 候补失败不产生任何费用</p>
                  </div>
                </div>

                <div class="rule-item">
                  <div class="rule-title">支付方式</div>
                  <div class="rule-content">
                    <p>• 支持银行卡、支付宝、微信支付</p>
                    <p>• 可开启自动支付功能</p>
                    <p>• 自动支付失败将保留30分钟手动支付时间</p>
                    <p>• 超时未支付订单将自动取消</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="rule-category">
              <h3>📋 退改规则</h3>
              <div class="rule-list">
                <div class="rule-item">
                  <div class="rule-title">候补取消</div>
                  <div class="rule-content">
                    <p>• 候补中的订单可随时免费取消</p>
                    <p>• 候补成功后不可取消，按正常退票规则处理</p>
                    <p>• 取消后可重新提交候补订单</p>
                  </div>
                </div>

                <div class="rule-item">
                  <div class="rule-title">退票改签</div>
                  <div class="rule-content">
                    <p>• 候补成功的车票按正常退改签规则执行</p>
                    <p>• 退票费用按铁路部门规定收取</p>
                    <p>• 改签需在有余票的情况下办理</p>
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
import { ref, reactive, computed, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const showAlert = ref(false)
const alertType = ref('')
const alertMessage = ref('')
const activeTab = ref('submit')
const orderFilter = ref('all')
const departureStations = ref([])
const arrivalStations = ref([])

// 导航标签
const tabs = [
  { key: 'submit', label: '提交候补', icon: '📝' },
  { key: 'orders', label: '我的候补', icon: '📋' },
  { key: 'rules', label: '候补规则', icon: '📖' }
]

// 座席类型
const seatTypes = [
  { value: 'business', label: '商务座', icon: '🥇', price: 1748 },
  { value: 'first', label: '一等座', icon: '🥈', price: 933 },
  { value: 'second', label: '二等座', icon: '🥉', price: 553 },
  { value: 'hard_sleeper', label: '硬卧', icon: '🛏️', price: 401 },
  { value: 'soft_sleeper', label: '软卧', icon: '🛌', price: 633 },
  { value: 'hard_seat', label: '硬座', icon: '💺', price: 232 }
]

// 常用车站
const commonStations = [
  '北京南',
  '北京西',
  '上海虹桥',
  '上海',
  '广州南',
  '深圳北',
  '杭州东',
  '南京南',
  '武汉',
  '成都东',
  '重庆北',
  '西安北',
  '郑州东',
  '长沙南',
  '济南西',
  '青岛',
  '厦门北',
  '福州南'
]

// 表单数据
const form = reactive({
  departure: '',
  arrival: '',
  date: '',
  trainType: '',
  seatTypes: ['second'],
  passengers: [
    {
      name: '',
      idType: '身份证',
      idNumber: '',
      phone: '',
      type: '成人'
    }
  ],
  deadline: '2',
  autoPay: 'true'
})

// 表单验证错误
const errors = reactive({})

// 候补订单数据
const waitlistOrders = ref([
  {
    id: 1,
    orderNumber: 'WL202412250001',
    departure: '北京南',
    arrival: '上海虹桥',
    date: '2024-12-28',
    seatTypes: ['二等座', '一等座'],
    passengerCount: 2,
    status: 'waiting',
    submitTime: '2024-12-25 14:30:00',
    progress: 65,
    progressText: '正在候补中，已有部分退票'
  },
  {
    id: 2,
    orderNumber: 'WL202412240002',
    departure: '广州南',
    arrival: '深圳北',
    date: '2024-12-26',
    seatTypes: ['二等座'],
    passengerCount: 1,
    status: 'success',
    submitTime: '2024-12-24 09:15:00',
    successTime: '2024-12-24 16:45:00'
  }
])

// 计算属性
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const maxDate = computed(() => {
  const maxDate = new Date()
  maxDate.setDate(maxDate.getDate() + 30)
  return maxDate.toISOString().split('T')[0]
})

const filteredOrders = computed(() => {
  if (orderFilter.value === 'all') {
    return waitlistOrders.value
  }
  return waitlistOrders.value.filter(order => order.status === orderFilter.value)
})

// 车站搜索
const searchStations = (type, query) => {
  if (!query) {
    if (type === 'departure') {
      departureStations.value = []
    } else {
      arrivalStations.value = []
    }
    return
  }

  const filtered = commonStations.filter(station => station.includes(query)).slice(0, 5)

  if (type === 'departure') {
    departureStations.value = filtered
  } else {
    arrivalStations.value = filtered
  }
}

const selectStation = (type, station) => {
  if (type === 'departure') {
    form.departure = station
    departureStations.value = []
  } else {
    form.arrival = station
    arrivalStations.value = []
  }
}

// 乘客管理
const addPassenger = () => {
  if (form.passengers.length < 5) {
    form.passengers.push({
      name: '',
      idType: '身份证',
      idNumber: '',
      phone: '',
      type: '成人'
    })
  }
}

const removePassenger = index => {
  form.passengers.splice(index, 1)
}

// 表单验证
const validateForm = () => {
  const newErrors = {}

  if (!form.departure.trim()) {
    newErrors.departure = '请选择出发城市'
  }

  if (!form.arrival.trim()) {
    newErrors.arrival = '请选择到达城市'
  }

  if (form.departure === form.arrival) {
    newErrors.arrival = '出发城市和到达城市不能相同'
  }

  if (!form.date) {
    newErrors.date = '请选择出发日期'
  }

  if (form.seatTypes.length === 0) {
    newErrors.seatTypes = '请至少选择一种座席类型'
  }

  // 验证乘客信息
  form.passengers.forEach((passenger, index) => {
    if (!passenger.name.trim()) {
      newErrors[`passenger_${index}_name`] = '请输入乘客姓名'
    }

    if (!passenger.idNumber.trim()) {
      newErrors[`passenger_${index}_idNumber`] = '请输入证件号码'
    } else if (passenger.idType === '身份证' && !/^\d{17}[\dX]$/.test(passenger.idNumber)) {
      newErrors[`passenger_${index}_idNumber`] = '请输入正确的身份证号码'
    }

    if (!passenger.phone.trim()) {
      newErrors[`passenger_${index}_phone`] = '请输入手机号码'
    } else if (!/^1[3-9]\d{9}$/.test(passenger.phone)) {
      newErrors[`passenger_${index}_phone`] = '请输入正确的手机号码'
    }
  })

  Object.keys(errors).forEach(key => {
    delete errors[key]
  })
  Object.assign(errors, newErrors)

  return Object.keys(newErrors).length === 0
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

// 提交候补订单
const submitWaitlist = async () => {
  if (!validateForm()) {
    showAlertMessage('请检查表单信息', 'alert-error')
    return
  }

  loading.value = true

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))

    // 生成新订单
    const newOrder = {
      id: Date.now(),
      orderNumber: `WL${new Date().getFullYear()}${String(new Date().getMonth() + 1).padStart(2, '0')}${String(new Date().getDate()).padStart(2, '0')}${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      departure: form.departure,
      arrival: form.arrival,
      date: form.date,
      seatTypes: form.seatTypes
        .map(type => seatTypes.find(s => s.value === type)?.label)
        .filter(Boolean),
      passengerCount: form.passengers.length,
      status: 'waiting',
      submitTime: new Date().toLocaleString('zh-CN'),
      progress: 0,
      progressText: '候补订单已提交，正在排队中'
    }

    waitlistOrders.value.unshift(newOrder)

    // 重置表单
    Object.assign(form, {
      departure: '',
      arrival: '',
      date: '',
      trainType: '',
      seatTypes: ['second'],
      passengers: [
        {
          name: '',
          idType: '身份证',
          idNumber: '',
          phone: '',
          type: '成人'
        }
      ],
      deadline: '2',
      autoPay: 'true'
    })

    showAlertMessage('候补订单提交成功！请在"我的候补"中查看进度', 'alert-success')
    activeTab.value = 'orders'
  } catch (error) {
    showAlertMessage('提交失败，请稍后重试', 'alert-error')
  } finally {
    loading.value = false
  }
}

// 获取状态文本
const getStatusText = status => {
  const statusMap = {
    waiting: '候补中',
    success: '候补成功',
    failed: '候补失败',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

// 取消订单
const cancelOrder = async orderId => {
  if (!confirm('确定要取消这个候补订单吗？')) {
    return
  }

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    const order = waitlistOrders.value.find(o => o.id === orderId)
    if (order) {
      order.status = 'cancelled'
    }

    showAlertMessage('候补订单已取消', 'alert-success')
  } catch (error) {
    showAlertMessage('取消失败，请稍后重试', 'alert-error')
  }
}

// 支付订单
const payOrder = orderId => {
  showAlertMessage('跳转到支付页面...', 'alert-success')
  // 这里可以跳转到支付页面
}

onMounted(() => {
  // 页面加载完成后的初始化操作
})
</script>

<style scoped>
.service-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.container {
  max-width: 1400px;
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

/* 导航标签样式 */
.nav-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 30px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tab-btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: #f8f9fa;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.tab-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.tab-icon {
  font-size: 1.2rem;
}

.tab-content {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

/* 表单样式 */
.waitlist-form {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
}

.waitlist-form h2 {
  margin: 0 0 25px 0;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 30px 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #e1e8ed;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.section-title .icon {
  font-size: 1.3rem;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
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

/* 搜索建议 */
.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #e1e8ed;
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.suggestion-item:hover {
  background: #f8f9fa;
}

/* 座席选择样式 */
.seat-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.seat-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.seat-option:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.seat-option.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.seat-icon {
  font-size: 1.5rem;
}

.seat-info {
  flex: 1;
}

.seat-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.seat-price {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* 乘客信息样式 */
.passengers-section {
  margin-bottom: 20px;
}

.passenger-card {
  background: white;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
}

.passenger-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e1e8ed;
}

.passenger-title {
  font-weight: 600;
  color: #2c3e50;
}

.remove-passenger {
  padding: 6px 12px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.remove-passenger:hover {
  background: #c82333;
}

.add-passenger-btn {
  width: 100%;
  padding: 16px;
  border: 2px dashed #667eea;
  background: transparent;
  color: #667eea;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.add-passenger-btn:hover:not(:disabled) {
  background: #f8f9ff;
  border-color: #5a67d8;
}

.add-passenger-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 候补设置样式 */
.waitlist-settings {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.auto-pay-options {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-option input[type='radio'] {
  width: auto;
  margin: 0;
}

.auto-pay-note {
  font-size: 0.875rem;
  color: #666;
  font-style: italic;
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
  margin-top: 30px;
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

/* 候补指南样式 */
.waitlist-guide {
  background: white;
  padding: 30px;
  border-radius: 12px;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.waitlist-guide h3 {
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

.guide-section p {
  color: #555;
  line-height: 1.6;
  margin: 0 0 10px 0;
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

/* 订单列表样式 */
.orders-section {
  max-width: 1000px;
  margin: 0 auto;
}

.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.orders-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
}

.filter-options select {
  padding: 10px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 14px;
  background: white;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.empty-action {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.empty-action:hover {
  background: #5a67d8;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background: white;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 25px;
  transition: all 0.3s ease;
}

.order-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e1e8ed;
}

.order-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.order-number {
  font-weight: 600;
  color: #2c3e50;
}

.order-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.order-status.waiting {
  background: #fff3cd;
  color: #856404;
}

.order-status.success {
  background: #d4edda;
  color: #155724;
}

.order-status.failed {
  background: #f8d7da;
  color: #721c24;
}

.order-status.cancelled {
  background: #e2e3e5;
  color: #383d41;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.cancel-btn,
.pay-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}

.pay-btn {
  background: #28a745;
  color: white;
}

.pay-btn:hover {
  background: #218838;
}

.order-content {
  display: grid;
  gap: 20px;
}

.route-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route-stations {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.arrow {
  color: #667eea;
  font-size: 1.5rem;
}

.route-date {
  color: #666;
  font-weight: 500;
}

.order-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.detail-item {
  display: flex;
  gap: 8px;
}

.detail-item .label {
  color: #666;
  min-width: 80px;
}

.detail-item .value {
  color: #2c3e50;
  font-weight: 500;
}

.progress-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.progress-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e1e8ed;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  color: #666;
}

/* 规则页面样式 */
.rules-section {
  max-width: 900px;
  margin: 0 auto;
}

.rules-section h2 {
  margin: 0 0 30px 0;
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  text-align: center;
}

.rule-category {
  margin-bottom: 40px;
}

.rule-category h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.rule-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rule-item {
  background: white;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 25px;
}

.rule-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
}

.rule-content p {
  margin: 8px 0;
  color: #555;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .waitlist-guide {
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

  .content-section {
    padding: 20px;
  }

  .alert {
    margin: 20px;
  }

  .nav-tabs {
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .seat-types {
    grid-template-columns: 1fr;
  }

  .waitlist-settings {
    grid-template-columns: 1fr;
  }

  .orders-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .order-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .order-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .route-info {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .order-details {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .waitlist-form,
  .waitlist-guide {
    padding: 20px;
  }

  .passenger-card {
    padding: 15px;
  }

  .auto-pay-options {
    flex-direction: column;
    gap: 10px;
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
  .seat-option,
  .passenger-card,
  .order-card {
    border-width: 2px;
  }

  .submit-btn,
  .tab-btn.active {
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
  .nav-tabs,
  .order-actions {
    display: none;
  }
}
</style>
