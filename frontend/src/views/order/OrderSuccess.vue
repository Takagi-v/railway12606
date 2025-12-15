<template>
  <div class="order-success-page">
    <Header12306 />
    <div class="main-content">
      <!-- Success Banner -->
      <div class="success-banner">
        <div class="success-icon-wrapper">
          <CheckCircleFilled class="success-icon" />
        </div>
        <div class="success-info">
          <div class="success-title-line">
            <span class="success-status-text">交易已成功！</span>
            <span class="success-sub-text">感谢您选择铁路出行！您的订单号：<span class="order-no">{{ orderId || 'EC10471229' }}</span></span>
          </div>
          <p class="success-desc">
            {{ passengerName }} 女士/先生可持购票时所使用的有效身份证件用于购票后、列车开车前到车站直接检票乘车。
          </p>
          <p class="success-note">
            消息通知方式进行相关调整，将通过“铁路12306”App客户端为您推送相关消息（需开启接收推送权限）。您也可以扫描关注下方“铁路12306”微信公众号或支付宝生活号二维码，选择通过微信或支付宝接收。
          </p>
        </div>
      </div>

      <!-- Order Info Section -->
      <div class="order-info-section">
        <div class="section-header">
          <h3>订单信息</h3>
        </div>
        <div class="train-info-bar">
          <span class="train-date">{{ trainDate }}</span>
          <span class="train-week">（{{ weekDay }}）</span>
          <span class="train-code">{{ trainCode }} 次</span>
          <span class="train-route">
            <span class="station from">{{ fromStation }}</span>站 （<span class="bold-time">{{ startTime }}</span> 开） — 
            <span class="station to">{{ toStation }}</span>站 （{{ endTime }} 到）
          </span>
        </div>
        
        <a-table 
          :columns="columns" 
          :data-source="passengerList" 
          :pagination="false"
          class="passenger-table"
          row-key="id"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <span class="status-paid">已支付</span>
            </template>
          </template>
        </a-table>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <a-button class="action-btn secondary">餐饮·特产</a-button>
          <a-button class="action-btn secondary" @click="continueBooking">继续购票</a-button>
          <a-button class="action-btn primary" @click="viewOrderDetails">查询订单详情</a-button>
        </div>
      </div>

      <!-- Footer / Warm Tips -->
      <div class="tips-footer">
        <div class="warm-tips">
          <h4>温馨提示</h4>
          <ol>
            <li>如需换票，请尽早携带购票时所使用的乘车人有效身份证件到车站、售票窗口、自动售（取）票机、铁路客票代售点办理。</li>
            <li>请乘车人持购票时使用的有效证件按时乘车。</li>
            <li>投保后可在“我的12306-我的保险”查看电子保单号（登陆<a href="http://www.china-ric.com" target="_blank" class="insurance-link">中国铁路保险www.china-ric.com</a> 查看电子保单）。</li>
            <li>完成微信或支付宝绑定后，购票、改签、退票、购买乘意险、退乘意险的通知消息，将会通过微信或支付宝通知提醒发送给您；手机号码核验、通过手机号码找回密码、列车运行调整的通知仍然通过短信发送给您。</li>
            <li>未尽事宜详见《铁路旅客运输规程》等有关规定和车站公告。</li>
          </ol>
        </div>
        <div class="qr-codes">
          <div class="qr-item">
            <div class="qr-placeholder">
               <!-- Placeholder for WeChat QR -->
               <img :src="requestWechatQrImg" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            <p>使用微信扫一扫，可通过<br>微信接收12306行程通知</p>
          </div>
          <div class="qr-item">
            <div class="qr-placeholder">
               <!-- Placeholder for Alipay QR -->
               <img :src="requestAliQrImg" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            <p>使用支付宝扫一扫，可通过<br>支付宝通知提醒接收<br>12306行程通知</p>
          </div>
        </div>
      </div>
      
      <!-- Ad Banner -->
      <div class="ad-banner">
        <img :src="ad007Img" style="width: 100%; height: auto; display: block;" />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CheckCircleFilled, QrcodeOutlined } from '@ant-design/icons-vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { getOrderDetail } from '@/api/order'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import ad007Img from '../../../pics/ad007.jpg'
import requestWechatQrImg from '../../../pics/requestWechatQr.jpg'
import requestAliQrImg from '../../../pics/requestAliQr.jpg'

dayjs.locale('zh-cn')

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const orderId = ref(route.query.orderId || '')
const passengerName = ref('')
const trainDate = ref('')
const weekDay = ref('')
const trainCode = ref('')
const fromStation = ref('')
const startTime = ref('')
const toStation = ref('')
const endTime = ref('')

const columns = [
  { title: '序号', dataIndex: 'index', key: 'index', width: 60 },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '证件类型', dataIndex: 'idType', key: 'idType' },
  { title: '证件号码', dataIndex: 'idNumber', key: 'idNumber' },
  { title: '票种', dataIndex: 'ticketType', key: 'ticketType' },
  { title: '席别', dataIndex: 'seatType', key: 'seatType' },
  { title: '车厢', dataIndex: 'coach', key: 'coach' },
  { title: '席位号', dataIndex: 'seatNo', key: 'seatNo' },
  { title: '票价（元）', dataIndex: 'price', key: 'price' },
  { title: '订单状态', key: 'status' }
]

const passengerList = ref([])

const continueBooking = () => {
  router.push('/leftTicket/single')
}

const viewOrderDetails = () => {
  if (orderId.value) {
    router.push(`/order/${orderId.value}`)
  } else {
    router.push('/user/orders')
  }
}

const formatSeatNumber = (seatStr) => {
  if (!seatStr) return { coach: '--', seatNo: '--' }
  
  // Example: "04车045号" or "1车01A"
  // Try to split by '车'
  if (seatStr.includes('车')) {
    const parts = seatStr.split('车')
    if (parts.length === 2) {
      return { coach: parts[0], seatNo: parts[1] }
    }
  }

  // Format: "01-001" -> coach: 01, seatNo: 001 or convert to 01A
  if (seatStr.includes('-')) {
    const parts = seatStr.split('-')
    if (parts.length === 2) {
      const carriage = parts[0]
      const seatIdx = parseInt(parts[1], 10)
      
      // Try to convert to new format A/B/C/D/F
      if (!isNaN(seatIdx)) {
          const row = Math.ceil(seatIdx / 5)
          const col = (seatIdx - 1) % 5
          const letters = ['A', 'B', 'C', 'D', 'F']
          const letter = letters[col] || 'A'
          // Return formatted parts: Coach 01, Seat 01A号
          return { 
              coach: carriage, 
              seatNo: `${String(row).padStart(2, '0')}${letter}号` 
          }
      }

      return { coach: parts[0], seatNo: parts[1] + '号' }
    }
  }

  return { coach: '--', seatNo: seatStr }
}

const fetchOrderDetails = async (id) => {
  if (!id) return
  
  loading.value = true
  try {
    const res = await getOrderDetail(id)
    console.log('Order Detail Response:', res)
    // Adjust based on actual API response structure (res.data or res)
    const order = res.data || res
    
    if (!order) {
      console.error('Order data is empty')
      return
    }

    // Set basic info
    orderId.value = order.order_number
    trainCode.value = order.train_number
    
    const getStationName = (val) => {
       if (!val) return ''
       if (typeof val === 'object') return val.station_name || ''
       return val
    }

    fromStation.value = getStationName(order.departure_station)
    toStation.value = getStationName(order.arrival_station)
     
    startTime.value = order.departure_time ? order.departure_time.substring(0, 5) : ''
    endTime.value = order.arrival_time ? order.arrival_time.substring(0, 5) : ''
    
    if (order.travel_date) {
      trainDate.value = dayjs(order.travel_date).format('YYYY-MM-DD')
      weekDay.value = dayjs(order.travel_date).format('dddd')
    }

    // Set passengers
    if (order.passengers && order.passengers.length > 0) {
      // Set main passenger name for banner
      passengerName.value = order.passengers[0].name
      
      passengerList.value = order.passengers.map((p, index) => {
        const { coach, seatNo } = formatSeatNumber(p.seat_number)
        return {
          id: index, // or p.id if available
          index: index + 1,
          name: p.name,
          idType: p.id_type || '居民身份证', // Map enum if needed
          idNumber: p.id_number && p.id_number.length > 7 ? p.id_number.substring(0, 4) + '*'.repeat(p.id_number.length - 7) + p.id_number.substring(p.id_number.length - 3) : p.id_number,
          ticketType: p.ticket_type,
          seatType: p.seat_type,
          coach: coach,
          seatNo: seatNo,
          price: p.price,
          status: 'paid' // Assuming success page means paid
        }
      })
    }
  } catch (error) {
    console.error('Failed to fetch order details:', error)
  } finally {
    loading.value = false
  }
}

watch(
  () => route.query.orderId,
  (newId) => {
    if (newId) {
      orderId.value = newId
      fetchOrderDetails(newId)
    }
  },
  { immediate: true }
)

onMounted(() => {
  // If watch immediate didn't trigger (unlikely, but for safety or SSR hydration)
  // or if we want to ensure it runs on mount if query is already present
  // Actually watch immediate handles it. But we can keep explicit check if needed.
  // The watch immediate will run once on setup.
})
</script>

<style scoped>
.order-success-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  width: 978px;
  margin: 20px auto;
  background: #f5f5f5;
}

/* Success Banner */
.success-banner {
  display: flex;
  width: 978px;
  height: 127px;
  padding: 15px 30px;
  background: #edffcc;
  border: 1px solid #91c0e6;
  margin: 20px 0 0 0;
  box-sizing: border-box;
}

.success-icon-wrapper {
  margin-right: 20px;
}

.success-icon {
  font-size: 48px;
  color: #52c41a;
}

.success-info {
  flex: 1;
  overflow: hidden;
}

.success-title-line {
  margin-bottom: 5px;
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
}

.success-status-text {
  font-size: 20px;
  color: #52c41a;
  font-weight: bold;
  margin-right: 10px;
}

.success-sub-text {
  font-size: 12px;
  color: #666;
}

.order-no {
  color: #ff7a00;
  font-weight: bold;
  font-size: 20px;
}

.success-desc {
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 5px;
}

.success-note {
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 0;
  font-weight: bold;
  max-width: 100%;
}

/* Order Info Section */
.order-info-section {
  border: 1px solid #91c0e6;
  margin: 20px 0 0 0;
  width: 978px;
  box-sizing: border-box;
}

.section-header {
  background: #298cce;
  color: #E5F8FF;
  height: 32px;
  line-height: 32px;
  padding: 0 10px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 4px 4px 0 0;
}

.train-info-bar {
  height: 30px;
  padding: 0 10px;
  background: #fff;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
}

.bold-time {
  font-weight: bold;
}

.train-date, .train-week, .train-code {
  margin-right: 15px;
}

.train-code {
  font-weight: bold;
}

.station {
  color: #333;
}

.station.from {
  font-size: 24px;
  color: #ff0000;
  /* font-weight: bold; */
}

.station.to {
  font-size: 18px;
  color: #000;
}

.passenger-table {
  width: 958px;
  margin: 0 auto;
  border-bottom: 1px solid #298cce;
}

:deep(.ant-table-thead > tr > th) {
  background: #eef1f6;
  font-weight: bold;
  text-align: center;
  padding: 8px 16px;
}
:deep(.ant-table-tbody > tr > td) {
  text-align: center;
  padding: 8px 16px;
}

.status-paid {
  color: #ff7a00;
  font-weight: bold;
}

.action-buttons {
  padding: 10px;
  text-align: center;
  background: #fff;
}

.action-btn {
  margin: 0 10px;
  height: 30px;
  padding: 0 25px;
  font-size: 14px;
  border-radius: 4px;
}

.action-btn.secondary {
  background: #fff;
  border: 1px solid #ddd;
  color: #666;
}

.action-btn.secondary:hover {
  border-color: #ff7a00;
  color: #ff7a00;
}

.action-btn.primary {
  background: #ff7a00;
  border-color: #ff7a00;
  color: #fff;
}

.action-btn.primary:hover {
  background: #ff9033;
  border-color: #ff9033;
}

/* Footer / Tips */
.tips-footer {
  display: flex;
  background: #FFFBE5;
  padding: 5px 10px;
  border-top: 1px dashed #ddd;
  margin: 0;
  width: 978px;
  box-sizing: border-box;
}

.warm-tips {
  flex: 1;
  padding-right: 40px;
}

.warm-tips h4 {
  color: #333;
  /* font-weight: bold; */
  margin-bottom: 5px;
}

.warm-tips ol {
  padding-left: 15px;
  color: #666;
  font-size: 12px;
  line-height: 1.6;
  margin-bottom: 0;
}

.qr-codes {
  display: flex;
  gap: 20px;
}

.qr-item {
  text-align: center;
  font-size: 12px;
  color: #666;
}

.qr-item p {
  margin: 0;
  line-height: 1.4;
}

.qr-placeholder {
  width: 140px;
  height: 140px;
  background: #fff;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2px;
}

.insurance-link {
  color: #0078d7;
  text-decoration: none;
}

/* Ad Banner */
.ad-banner {
  margin: 0 0 20px;
  width: 978px;
}
</style>