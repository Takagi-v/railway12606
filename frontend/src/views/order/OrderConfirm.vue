<template>
  <div class="order-confirm">
    <Header12306 />
    <div class="wrapper">
      <!-- 列车信息 -->
      <div class="order-section train-info-block">
        <div class="section-header">
          <span class="title">列车信息</span>
          <span class="subtitle">（以下余票信息仅供参考）</span>
        </div>
        <div class="train-body">
          <!-- Debug info to ensure visibility -->
          <div v-if="!train.trainNo && !train.date" style="padding: 20px; text-align: center; color: #999;">
            正在加载车次信息...
          </div>
          <div v-else>
             <div class="train-line-1">
            <span class="date"><strong>{{ train.date }}</strong></span>
            <span class="train-no"><strong>{{ train.trainNo }}</strong><span class="small-text">次</span></span>
            <span class="station-group">
              <span class="station-name">{{ train.fromStation || '--' }}</span><span class="small-text">站</span>
              <span class="time">（<strong>{{ train.departTime }}</strong>开）</span>
              <span class="separator">—</span>
              <span class="station-name">{{ train.toStation || '--' }}</span><span class="small-text">站</span>
              <span class="time">（<strong>{{ train.arriveTime }}</strong>到）</span>
            </span>
          </div>
          <div class="train-line-2">
            <div class="seat-item" v-if="train.seatType">
              <span class="seat-name">{{ train.seatType }}</span>
              <span class="seat-price">
                <span class="currency">¥</span>
                <span class="amount">{{ train.price }}</span>
              </span>
              <!-- <span class="seat-count">有票</span> -->
            </div>
            <div class="seat-tip" v-else>
              请重新选择车次以获取票价信息
            </div>
          </div>
          <div class="train-note">
            *显示的价格均为实际活动折扣后票价，供您参考，查看公布票价。具体票价以您确认支付时实际购买的铺别票价为准。
          </div>
          </div>
        </div>
      </div>

      <!-- 乘客信息 -->
      <div class="order-section passenger-info-block">
        <div class="section-header">
          <span class="title">乘客信息</span>
          <span class="subtitle">（填写说明）</span>
          <div class="header-tool">
             <a-input-search
              v-model:value="searchName"
              placeholder="输入乘客姓名"
              style="width: 200px"
              size="small"
              @search="onSearch"
            />
          </div>
        </div>
        <div class="passenger-body">
          <!-- 受让人选择 (Transferee Selection) -->
          <div class="passenger-selection transferee-selection">
            <div class="label">
              <i class="custom-icon-user icon-transferee"></i>
              受让人
            </div>
            <div class="list">
               <label 
                v-for="p in filteredPassengers" 
                :key="'transferee-' + p.id" 
                class="checkbox-item"
              >
                <input 
                  type="checkbox" 
                  :value="p.id" 
                  v-model="selectedTransfereeIds"
                />
                {{ p.name }}
                <!-- <span class="tag" style="color: #666;"></span> -->
              </label>
              <span v-if="filteredPassengers.length === 0" class="no-passenger-tip">
                未找到相关受让人
              </span>
            </div>
          </div>

          <!-- 常用乘车人选择 -->
          <div class="passenger-selection" style="padding-top: 0;">
            <div class="label">
              <i class="custom-icon-user icon-passenger"></i>
              乘车人
            </div>
            <div class="list">
              <label 
                v-for="p in filteredPassengers" 
                :key="p.id" 
                class="checkbox-item"
              >
                <input 
                  type="checkbox" 
                  :value="p.id" 
                  v-model="selectedIds"
                />
                {{ p.name }}
                <span v-if="p.type && p.type !== '成人'" class="tag">{{ p.type }}</span>
              </label>
              <span v-if="filteredPassengers.length === 0" class="no-passenger-tip">
                未找到相关乘车人
              </span>
            </div>
          </div>

          <!-- 已选乘客表格 -->
          <div class="passenger-table-wrapper">
             <table class="passenger-table">
               <thead>
                 <tr>
                   <th class="col-seq">序号</th>
                   <th class="col-ticket">票种</th>
                   <th class="col-seat">席别</th>
                   <th class="col-name">姓名</th>
                   <th class="col-idtype">证件类型</th>
                   <th class="col-idno">证件号码</th>
                   <th class="col-op">操作</th>
                 </tr>
               </thead>
               <tbody>
                 <tr v-for="(id, idx) in effectiveSelectedIds" :key="id">
                   <td class="col-seq">{{ idx + 1 }}</td>
                   <td class="col-ticket">
                     <select 
                        v-model="selectionMap[id].ticketType"
                        class="custom-select"
                      >
                       <option v-for="opt in ticketTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-seat">
                     <select 
                        v-model="selectionMap[id].seatType"
                        class="custom-select"
                      >
                       <option v-for="opt in seatTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-name">
                     {{ getPassengerName(id) }}
                   </td>
                   <td class="col-idtype">
                     <select 
                        v-model="selectionMap[id].idType"
                        class="custom-select"
                      >
                       <option v-for="opt in idTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-idno">
                     {{ getPassengerIdNo(id) }}
                   </td>
                   <td class="col-op">
                     <span class="btn-close" @click="removePassenger(id)">×</span>
                   </td>
                 </tr>
                 <tr v-if="effectiveSelectedIds.length === 0">
                   <td class="col-seq">1</td>
                   <td class="col-ticket">
                     <select class="custom-select" v-model="defaultSelection.ticketType">
                       <option v-for="opt in ticketTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-seat">
                     <select class="custom-select" v-model="defaultSelection.seatType">
                       <option v-for="opt in seatTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-name"></td>
                   <td class="col-idtype">
                     <select class="custom-select" v-model="defaultSelection.idType">
                       <option v-for="opt in idTypeOptions" :key="opt" :value="opt">{{ opt }}</option>
                     </select>
                   </td>
                   <td class="col-idno"></td>
                   <td class="col-op"></td>
                 </tr>
               </tbody>
             </table>
          </div>
          
          <div class="ad-image-wrapper" style="padding: 0 20px 20px; text-align: center;">
            <img src="../../../pics/ins_ad7.png" alt="广告图片" style="max-width: 100%; height: auto; border-radius: 4px;">
          </div>
        </div>
      </div>

      <!-- 提交区域 -->
      <div class="submit-bar">
        <div class="agreement">
          提交订单表示已阅读并同意
          <a href="javascript:;">《国铁集团铁路旅客运输规程》</a>
          <a href="javascript:;">《服务条款》</a>
        </div>
        <div class="btns">
          <button class="btn-back" @click="goBack">上一步</button>
          <button class="btn-submit" :disabled="submitting" @click="submitOrder">提交订单</button>
        </div>
      </div>

      <!-- 温馨提示 -->
      <div class="warm-tips">
        <div class="tips-title">温馨提示：</div>
        <div class="tips-content">
          <p>1. 一张有效身份证件同一乘车日期同一车次只能购买一张车票，高铁动卧列车除外。改签或变更到站后车票的乘车日期在春运期间，如再办理退票将按票面价格20%核收退票费。请合理安排行程，更多改签规则请查看<span class="highlight-blue">《退改说明》</span> 。</p>
          <p>2. 购买儿童票时，乘车儿童有有效身份证件的，请填写本人有效身份证件信息。自2023年1月1日起，每一名持票成年人旅客可免费携带一名未满6周岁且不单独占用席位的儿童乘车，超过一名时，超过人数应购买儿童优惠票。免费儿童可以在购票成功后添加。</p>
          <p>3. 购买残疾军人（伤残警察）优待票的，须在购票后、开车前办理换票手续方可进站乘车。换票时，不符合规定的减价优待条件，没有有效"中华人民共和国残疾军人证"或"中华人民共和国伤残人民警察证"的，不予换票，所购车票按规定办理退票手续。</p>
          <p>4. 一天内3次申请车票成功后取消订单（包含无座票时取消5次计为取消1次），当日将不能在12306继续购票。</p>
          <p class="bold-tips">5. 购买铁路乘意险的注册用户年龄须在18周岁以上，使用非中国居民身份证注册的用户如购买铁路乘意险，须在<span class="highlight-blue">我的12306——个人信息</span> 如实填写“出生日期”。</p>
          <p class="bold-tips">6. 父母为未成年子女投保，须在<span class="highlight-blue">我的乘车人</span> 登记未成年子女的有效身份证件信息。</p>
          <p>7. 未尽事宜详见《铁路旅客运输规程》等有关规定和车站公告。</p>
        </div>
      </div>

    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import { searchTrains } from '@/api/train'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { getPassengers } from '@/api/passenger'
import { createOrder } from '@/api/order'

const router = useRouter()
const route = useRoute()

const train = ref({
  date: '',
  trainNo: '',
  fromStation: '',
  toStation: '',
  departTime: '',
  arriveTime: '',
  seatType: '',
  price: ''
})

const passengers = ref([])
const selectedIds = ref([])
const selectedTransfereeIds = ref([])
const searchName = ref('')
const submitting = ref(false)
const trainId = ref(String(route.query.trainId || ''))

const seatTypeOptions = ['商务座', '一等座', '二等座', '软卧', '硬卧', '硬座', '无座']
const ticketTypeOptions = ['成人票', '学生票', '儿童票']
const idTypeOptions = ['中国居民身份证', '护照', '港澳居民来往内地通行证', '台湾居民来往大陆通行证']

const defaultSelection = ref({
  ticketType: '成人票',
  seatType: '二等座',
  idType: '中国居民身份证'
})

const selectionMap = ref({})

const mapPassenger = p => ({
  id: p.id,
  name: p.name,
  type: p.passenger_type,
  idTypeLabel: p.id_type,
  idNo: p.id_number,
  phoneVerified: p.verified ? 'Y' : 'N'
})

const effectiveSelectedIds = computed(() => {
  return selectedTransfereeIds.value.length > 0 ? selectedTransfereeIds.value : selectedIds.value
})

// Mutual exclusion logic
watch(selectedIds, (newVal) => {
  if (newVal.length > 0) {
    selectedTransfereeIds.value = []
  }
})

watch(selectedTransfereeIds, (newVal) => {
  if (newVal.length > 0) {
    selectedIds.value = []
  }
})

const loadPassengers = async () => {
  try {
    const res = await getPassengers()
    if (res.code === 200) {
      passengers.value = (res.data || []).map(mapPassenger)
      const map = {}
      passengers.value.forEach(p => {
        map[p.id] = { 
          seatType: train.value.seatType || '二等座', 
          ticketType: '成人票',
          idType: p.idTypeLabel || '中国居民身份证'
        }
      })
      selectionMap.value = map
    }
  } catch (e) {
    message.error('乘客信息加载失败')
  }
}

const initTrainInfo = () => {
  const q = route.query || {}
  
  // 处理 trainNo 可能存在的中文前缀（如"去程 G123"）
  let rawTrainNo = q.trainNo || q.code || ''
  if (rawTrainNo.includes(' ')) {
    rawTrainNo = rawTrainNo.split(' ').pop()
  }

  console.log('[OrderConfirm] Query Params:', q)

  train.value = {
    date: q.date || '',
    trainNo: rawTrainNo,
    fromStation: q.fromStation || q.from || '',
    toStation: q.toStation || q.to || '',
    departTime: q.departTime || '',
    arriveTime: q.arriveTime || '',
    seatType: q.seatType || '二等座',
    price: q.price || ''
  }
  console.log('[OrderConfirm] Initialized Train:', train.value)

  // 如果缺少关键信息，使用测试数据（仅在完全无参数时）
  if (!train.value.date && !train.value.trainNo && !train.value.fromStation) {
    train.value = {
      date: '2025-12-11 (周四)',
      trainNo: 'G3073',
      fromStation: '上海虹桥',
      toStation: '广州东',
      departTime: '07:17',
      arriveTime: '15:57',
      seatType: '二等座',
      price: '819.0'
    }
    // 模拟 trainId 用于测试
    if (!trainId.value) trainId.value = '1'
  }

  if (train.value.seatType) {
    defaultSelection.value.seatType = train.value.seatType
  }

  // 如果有车次信息但没有价格或ID，尝试补全
  if (train.value.trainNo && (!train.value.price || !trainId.value)) {
    enrichTrainInfo()
  }
}

const seatTypeKeyMap = {
  '一等座': 'first_class',
  '二等座': 'second_class',
  '软卧': 'soft_sleeper',
  '硬卧': 'hard_sleeper'
}

const enrichTrainInfo = async () => {
  try {
    const params = {
      departure_city: train.value.fromStation,
      arrival_city: train.value.toStation,
      travel_date: train.value.date
    }
    // 如果缺少日期或车站，无法查询
    if (!params.travel_date || !params.departure_city || !params.arrival_city) return

    const resp = await searchTrains(params)
    const rows = Array.isArray(resp?.data) ? resp.data : []
    const match = rows.find(
      item =>
        String(item.train_number) === String(train.value.trainNo) ||
        (String(item.departure_time) === String(train.value.departTime) &&
          String(item.arrival_time) === String(train.value.arriveTime))
    )
    
    if (match) {
      if (!trainId.value) {
        trainId.value = String(match.train_id)
      }
      // 补全价格
      if (!train.value.price) {
        const key = seatTypeKeyMap[train.value.seatType]
        if (key && match[key]) {
          train.value.price = match[key].price
        }
      }
      // 补全其他可能缺失的信息
      if (!train.value.departTime) train.value.departTime = match.departure_time
      if (!train.value.arriveTime) train.value.arriveTime = match.arrival_time
    }
  } catch (e) {
    console.warn('补全车次信息失败', e)
  }
}

const filteredPassengers = computed(() => {
  const kw = searchName.value.trim()
  if (!kw) return passengers.value
  return passengers.value.filter(p => String(p.name).includes(kw))
})

const onSearch = () => {
  // filteredPassengers is computed, no action needed, but maybe trim
}



const goBack = () => {
  router.back()
}

const getPassengerName = (id) => {
  const p = passengers.value.find(x => x.id === id)
  return p ? p.name : ''
}
const getPassengerIdType = (id) => {
  const p = passengers.value.find(x => x.id === id)
  return p ? p.idTypeLabel : ''
}
const getPassengerIdNo = (id) => {
  const p = passengers.value.find(x => x.id === id)
  return p ? p.idNo : ''
}
const removePassenger = (id) => {
  if (selectedTransfereeIds.value.includes(id)) {
    selectedTransfereeIds.value = selectedTransfereeIds.value.filter(x => x !== id)
  } else {
    selectedIds.value = selectedIds.value.filter(x => x !== id)
  }
}

const submitOrder = async () => {
  if (effectiveSelectedIds.value.length === 0) {
    message.error('请选择乘车人或受让人')
    return
  }
  if (!trainId.value) {
    await enrichTrainInfo()
    if (!trainId.value) {
      message.error('无法识别车次，提交失败')
      return
    }
  }

  Modal.confirm({
    title: '请再次确认订单信息',
    content: '请核对乘车人、车次及日期信息，确认无误后点击确定提交订单。',
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      await processOrderSubmission()
    }
  })
}

const processOrderSubmission = async () => {
  const payload = {
    train_id: Number(trainId.value),
    travel_date: train.value.date,
    from_station: train.value.fromStation,
    to_station: train.value.toStation,
    passengers: effectiveSelectedIds.value.map(id => ({
      passenger_id: id,
      ticket_type: normalizeTicketType(selectionMap.value[id]?.ticketType || '成人票'),
      seat_type: selectionMap.value[id]?.seatType || '二等座'
    }))
  }
  submitting.value = true
  try {
    const res = await createOrder(payload)
    if (res.code === 200 || res.code === 201) {
      const orderNo = res.data?.order_number || ''
      Modal.success({
        title: '订单提交成功',
        content: orderNo
          ? '订单号：' + orderNo + '，请在30分钟内完成支付'
          : '订单已创建，请在30分钟内完成支付',
        onOk: () => {
          router.push('/user/orders')
        }
      })
    }
  } catch (e) {
    message.error('提交失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  initTrainInfo()
  loadPassengers()
})

const normalizeTicketType = t => {
  if (t === '成人票' || t === '成人') return '成人'
  if (t === '学生票' || t === '学生') return '学生'
  if (t === '儿童票' || t === '儿童') return '儿童'
  return '成人'
}
</script>

<style scoped>
.order-confirm {
  background: #f5f5f5;
  min-height: 100vh;
  font-family: Arial, "Microsoft YaHei", sans-serif;
}
.wrapper {
  width: 978.67px;
  margin: 0 auto;
  padding: 20px 0 50px;
}

/* Common Section Styles */
.order-section {
  border: 1px solid #3b99fc;
  margin-bottom: 20px;
  border-radius: 10px;
  overflow: hidden; /* Ensures children (like header) respect border-radius */
  background: #fff;
  /* Ensure BFC to contain floats and prevent collapse */
  display: flow-root;
  position: relative;
  z-index: 1;
}
.section-header {
  height: 32px;
  background: #298cce;;
  color: #fff;
  padding: 0 15px;
  display: flex;
  align-items: center;
  position: relative;
}
.section-header .title {
  font-size: 14px;
  color:#E5F8FF;
  margin-right: 10px;
}
.section-header .subtitle {
  font-size: 12px;
  color:#E5F8FF;
  opacity: 0.9;
}
.header-tool {
  margin-left: auto;
}

/* Train Info */
.train-body {
  padding: 10px 20px;
  background: #EEF1F8;
  height: 98px; /* Fixed height as requested */
  min-height: 98px; /* Ensure it respects the height */
  box-sizing: border-box; /* Include padding in height calculation */
  display: block;
  overflow: hidden; /* Prevent content overflow if it exceeds height */
  position: relative;
}
.train-line-1 {
  font-size: 18px;
  color: #333;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px dashed #999;
  display: flex;
  align-items: baseline;
  gap: 15px;
}
.train-line-1 strong {
  font-weight: bold;
}
.station-group {
  display: flex;
  align-items: baseline;
}
.station-name {
  font-size: 18px;
  font-weight: normal;
}
.small-text {
  font-size: 14px;
  font-weight: normal;
}
.station-group .small-text {
  margin-right: 5px;
}
.time {
  font-size: 14px;
  color: #333;
}
.separator {
  margin: 0 10px;
  font-weight: bold;
  color: #333;
}
.train-line-2 {
  margin-bottom: 5px;
}
.seat-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-right: 20px;
  font-size: 12px;
}
.seat-price {
  color: #ff8200;
  font-weight: bold;
}
.seat-price .currency {
  font-size: 12px;
}
.seat-price .amount {
  font-size: 12px;
}
.train-note {
  font-size: 12px;
  color: #3b99fc;
  position: absolute;
  bottom: 6px;
  left: 20px;
}

/* Passenger Info */
.passenger-body {
  padding: 0;
  background: #fff;
}
.passenger-selection {
  padding: 15px 20px;
  border-bottom: 1px dashed #eee;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.passenger-selection .label {
  display: flex;
  align-items: center;
  color: #333;
  font-weight: bold;
  width: 100%;
  padding-top: 0;
}
.custom-icon-user {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 5px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}
.custom-icon-user::before {
  content: none !important;
}
.icon-transferee {
  /* Yellow User Icon SVG */
  background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 512c141.38 0 256-114.62 256-256S653.38 0 512 0 256 114.62 256 256s114.62 256 256 256z m0 64c-170.66 0-512 85.34-512 256v128c0 35.34 28.66 64 64 64h896c35.34 0 64-28.66 64-64v-128c0-170.66-341.34-256-512-256z" fill="%23ff8200"></path></svg>');
}
.icon-passenger {
  /* Blue User Icon SVG */
  background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 512c141.38 0 256-114.62 256-256S653.38 0 512 0 256 114.62 256 256s114.62 256 256 256z m0 64c-170.66 0-512 85.34-512 256v128c0 35.34 28.66 64 64 64h896c35.34 0 64-28.66 64-64v-128c0-170.66-341.34-256-512-256z" fill="%233b99fc"></path></svg>');
}
.passenger-selection .list {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding-left: 25px; /* Align with label text (icon 20px + margin 5px) */
}
.checkbox-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #666;
}
.checkbox-item input {
  margin: 0;
}
.checkbox-item .tag {
  font-size: 12px;
  color: #999;
}
.no-passenger-tip {
  color: #999;
  font-size: 12px;
}

/* Table */
.passenger-table-wrapper {
  padding: 20px 20px 0;
}
.passenger-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #dedede;
}
.passenger-table th {
  background: #f0f0f0;
  color: #666;
  font-weight: normal;
  padding: 8px;
  border: 1px solid #dedede;
  text-align: center;
  font-size: 12px;
}
.passenger-table td {
  padding: 8px;
  border: 1px solid #dedede;
  text-align: center;
  font-size: 14px;
  color: #333;
}
.custom-select {
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 2px;
  width: 100%;
  max-width: 140px;
}
.btn-close {
  display: inline-block;
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  color: #fff;
  background: #ddd;
  border-radius: 50%;
  cursor: pointer;
  font-weight: bold;
}
.btn-close:hover {
  background: #ff4d4f;
}
.empty-row {
  padding: 30px;
  color: #999;
}
.passenger-actions {
  padding: 0 20px 20px;
  text-align: right;
}

/* Submit Bar */
.submit-bar {
  margin-top: 20px;
  text-align: center;
}
.agreement {
  font-size: 12px;
  color: #666;
  margin-bottom: 15px;
  text-align: left;
}
.agreement a {
  color: #3b99fc;
  text-decoration: none;
  margin: 0 5px;
}
.btns {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}
.btn-back {
  width: 90px;
  height: 30px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  color: #666;
}
.btn-back:hover {
  background: #f8f8f8;
}
.btn-submit {
  width: 90px;
  height: 30px;
  background: #ff8200;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  color: #fff;
}
.btn-submit:hover {
  background: #ff9900;
}
.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Warm Tips */
.warm-tips {
  margin-top: 0;
  background: #fffbe5;
  border: 1px solid #fcd693;
  padding: 10px 2px;
  color: #333;
  border-radius: 4px;
  height: 245px;
  overflow-y: auto; /* Add scroll if content exceeds height */
  box-sizing: border-box;
}
.tips-title {
  font-weight: bold;
  font-size: 14px;
  font-family: "SimSun", "宋体", serif;
  margin-bottom: 2px;
  color: #333;
}
.tips-content p {
  width: 968.67px;
  margin: 0;
  font-size: 12px;
  font-family: "SimSun", "宋体", serif;
  line-height: 20px;
  color: #666;
  text-align: left;
}
.highlight-blue {
  color: #3b99fc !important;
}
.bold-tips {
  font-weight: bold !important;
}
</style>
