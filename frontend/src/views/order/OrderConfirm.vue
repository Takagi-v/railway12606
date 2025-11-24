<template>
  <div class="order-confirm">
    <Header12306 />
    <div class="wrapper">
      <div class="train-info">
        <div class="train-row">
          <div class="train-date">{{ train.date || '-' }}</div>
          <div class="train-main">
            <span class="train-code">{{ train.trainNo || '-' }}</span>
            <span class="train-stations">
              {{ train.fromStation || '-' }}（{{ train.departTime || '-' }}） →
              {{ train.toStation || '-' }}（{{ train.arriveTime || '-' }}）
            </span>
          </div>
        </div>
        <div class="train-extra" v-if="train.price || train.seatType">
          <span v-if="train.seatType">{{ train.seatType }}</span>
          <span v-if="train.price">￥{{ train.price }}</span>
        </div>
      </div>

      <div class="section passengers">
        <div class="section-hd">乘客信息</div>
        <div class="section-tools">
          <a-input v-model:value="searchName" placeholder="输入乘客姓名" style="width: 240px" />
          <a-button @click="applyFilter">查询</a-button>
        </div>
        <div class="passenger-list">
          <table class="table" cellspacing="0" cellpadding="0">
            <thead>
              <tr>
                <th class="col-select">
                  <input type="checkbox" v-model="allChecked" @change="toggleAll" />
                </th>
                <th class="col-index">序号</th>
                <th class="col-name">姓名</th>
                <th class="col-type">旅客类型</th>
                <th class="col-idtype">证件类型</th>
                <th class="col-idno">证件号码</th>
                <th class="col-seat">席别</th>
                <th class="col-ticket">票种</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in filteredPassengers" :key="p.id">
                <td class="col-select">
                  <input type="checkbox" :value="p.id" v-model="selectedIds" />
                </td>
                <td class="col-index">{{ idx + 1 }}</td>
                <td class="col-name">
                  <i class="icon icon-person"></i>
                  <span class="text">{{ p.name }}</span>
                </td>
                <td class="col-type">{{ p.type }}</td>
                <td class="col-idtype">{{ p.idTypeLabel }}</td>
                <td class="col-idno">{{ p.idNo }}</td>
                <td class="col-seat">
                  <a-select
                    v-model:value="selectionMap[p.id].seatType"
                    :disabled="!selectedIds.includes(p.id)"
                    style="width: 120px"
                  >
                    <a-select-option v-for="opt in seatTypeOptions" :key="opt" :value="opt">
                      {{ opt }}
                    </a-select-option>
                  </a-select>
                </td>
                <td class="col-ticket">
                  <a-select
                    v-model:value="selectionMap[p.id].ticketType"
                    :disabled="!selectedIds.includes(p.id)"
                    style="width: 120px"
                  >
                    <a-select-option v-for="opt in ticketTypeOptions" :key="opt" :value="opt">
                      {{ opt }}
                    </a-select-option>
                  </a-select>
                </td>
              </tr>
              <tr v-if="filteredPassengers.length === 0">
                <td colspan="8" class="empty">暂无乘车人</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="passenger-actions">
          <a-button @click="goPassengers">管理乘车人</a-button>
        </div>
      </div>

      <div class="section notice">
        <div class="section-hd">温馨提示</div>
        <ul class="notice-list">
          <li>一张有效身份证件同一乘车日同一车次只能购买一张车票。</li>
          <li>购票前请确认乘客身份信息准确无误，证件类型与号码需与乘车人一致。</li>
          <li>儿童、学生等特殊票种需符合相关条件并携带有效证件。</li>
          <li>提交订单后请尽快完成支付，以免座位被释放。</li>
          <li>如需改签或退票，请在订单详情中进行相应操作。</li>
          <li>网络高峰期可能影响提交，请耐心等待或稍后再试。</li>
        </ul>
      </div>

      <div class="section actions">
        <div class="actions-bar">
          <a-button @click="goBack">上一步</a-button>
          <a-button type="primary" :disabled="submitting" @click="submitOrder">提交订单</a-button>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import { searchTrains } from '@/api/train'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { getPassengers } from '@/api/passenger'
import { createOrder } from '@/api/order'

const router = useRouter()
const route = useRoute()

const train = computed(() => {
  const q = route.query || {}
  return {
    date: q.date || '',
    trainNo: q.trainNo || q.code || '',
    fromStation: q.fromStation || q.from || '',
    toStation: q.toStation || q.to || '',
    departTime: q.departTime || '',
    arriveTime: q.arriveTime || '',
    seatType: q.seatType || '',
    price: q.price || ''
  }
})

const passengers = ref([])
const selectedIds = ref([])
const allChecked = ref(false)
const searchName = ref('')
const submitting = ref(false)
const trainId = ref(String(route.query.trainId || ''))

const seatTypeOptions = ['商务座', '一等座', '二等座', '软卧', '硬卧', '硬座', '无座']
const ticketTypeOptions = ['成人票', '学生票', '儿童票']

const selectionMap = ref({})

const mapPassenger = p => ({
  id: p.id,
  name: p.name,
  type: p.passenger_type,
  idTypeLabel: p.id_type,
  idNo: p.id_number,
  phoneVerified: p.verified ? 'Y' : 'N'
})

const loadPassengers = async () => {
  try {
    const res = await getPassengers()
    if (res.code === 200) {
      passengers.value = (res.data || []).map(mapPassenger)
      const map = {}
      passengers.value.forEach(p => {
        map[p.id] = { seatType: train.value.seatType || '二等座', ticketType: '成人票' }
      })
      selectionMap.value = map
    }
  } catch (e) {
    message.error('乘客信息加载失败')
  }
}

const filteredPassengers = computed(() => {
  const kw = searchName.value.trim()
  if (!kw) return passengers.value
  return passengers.value.filter(p => String(p.name).includes(kw))
})

const applyFilter = () => {}

const toggleAll = () => {
  if (allChecked.value) {
    selectedIds.value = filteredPassengers.value.map(p => p.id)
  } else {
    selectedIds.value = []
  }
}

const goPassengers = () => {
  router.push('/user/passengers')
}

const goBack = () => {
  router.back()
}

const submitOrder = async () => {
  if (selectedIds.value.length === 0) {
    message.error('请选择乘车人')
    return
  }
  if (!trainId.value) {
    await resolveTrainId()
    if (!trainId.value) {
      message.error('无法识别车次，提交失败')
      return
    }
  }
  const payload = {
    train_id: Number(trainId.value),
    travel_date: train.value.date,
    from_station: train.value.fromStation,
    to_station: train.value.toStation,
    passengers: selectedIds.value.map(id => ({
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
  loadPassengers()
})

const normalizeTicketType = t => {
  if (t === '成人票' || t === '成人') return '成人'
  if (t === '学生票' || t === '学生') return '学生'
  if (t === '儿童票' || t === '儿童') return '儿童'
  return '成人'
}

const resolveTrainId = async () => {
  try {
    const params = {
      departure_city: train.value.fromStation,
      arrival_city: train.value.toStation,
      travel_date: train.value.date
    }
    const resp = await searchTrains(params)
    const rows = Array.isArray(resp?.data) ? resp.data : []
    const match = rows.find(
      item =>
        String(item.train_number) === String(train.value.trainNo) ||
        (String(item.departure_time) === String(train.value.departTime) &&
          String(item.arrival_time) === String(train.value.arriveTime))
    )
    if (match?.train_id) {
      trainId.value = String(match.train_id)
    }
  } catch (e) {
    console.warn(e)
  }
}
</script>

<style scoped>
.order-confirm {
  background: #f5f7fa;
}
.wrapper {
  width: 1200px;
  height: 700px;
  margin: 0 auto;
  padding: 16px 0 24px;
}
.train-info {
  background: #e6f2ff;
  border: 1px solid #acd1f9;
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 16px;
}
.train-row {
  display: flex;
  align-items: center;
  gap: 16px;
}
.train-date {
  color: #333;
  font-weight: 600;
}
.train-main {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #333;
}
.train-code {
  font-weight: 600;
  color: #3b99fc;
}
.train-stations {
  color: #666;
}
.train-extra {
  margin-top: 8px;
  color: #999;
}
.section {
  background: #fff;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  margin-bottom: 16px;
}
.section-hd {
  height: 40px;
  line-height: 40px;
  padding: 0 12px;
  background: #3b99fc;
  color: #fff;
  font-weight: 600;
  border-bottom: 1px solid #acd1f9;
}
.section-tools {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
}
.passenger-list {
  padding: 12px;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table thead th {
  background: #f7fbff;
  color: #333;
  font-weight: 500;
  font-size: 12px;
  padding: 10px 8px;
  border-bottom: 1px solid #eaeaea;
  text-align: center;
}
.table tbody td {
  padding: 10px 8px;
  font-size: 12px;
  color: #333;
  border-bottom: 1px solid #f0f0f0;
  text-align: center;
}
.col-select {
  width: 40px;
}
.col-index {
  width: 60px;
}
.col-name {
  width: 160px;
}
.col-type {
  width: 100px;
}
.col-idtype {
  width: 140px;
}
.col-idno {
  width: 220px;
}
.col-seat {
  width: 140px;
}
.col-ticket {
  width: 140px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 16px 0;
}
.icon-person {
  color: #3b99fc;
  margin-right: 6px;
}
.passenger-actions {
  padding: 12px;
  border-top: 1px solid #f0f0f0;
}
.notice {
  padding-bottom: 10px;
}
.notice-list {
  list-style: decimal;
  padding: 12px 24px;
  color: #666;
}
.actions {
  background: transparent;
  border: none;
}
.actions-bar {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 12px 0;
}
</style>
