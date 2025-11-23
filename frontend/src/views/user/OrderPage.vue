<template>
  <div class="order-page">
    <div class="subway-order">
      <div class="toolbar">
        <div class="tabs">
          <a
            href="javascript:;"
            :class="{ active: activeTab === 'pending' }"
            @click="setTab('pending')"
          >
            未完成订单
          </a>
          <a
            href="javascript:;"
            :class="{ active: activeTab === 'upcoming' }"
            @click="setTab('upcoming')"
          >
            未出行订单
          </a>
          <a
            href="javascript:;"
            :class="{ active: activeTab === 'history' }"
            @click="setTab('history')"
          >
            历史订单
          </a>
        </div>
        <div class="filters">
          <select v-model="filterRange">
            <option value="30">近30天</option>
            <option value="180">近半年</option>
          </select>
          <input
            v-model="keyword"
            type="text"
            class="search"
            placeholder="按订单号/车次/站点搜索"
            @keyup.enter="applyFilters"
          />
          <button class="btn" @click="applyFilters">查询</button>
        </div>
      </div>
    </div>

    <div v-if="orders.length" class="order-list">
      <div v-for="o in orders" :key="o.id" class="order-item">
        <div class="order-head">
          <div class="order-no">订单号：{{ o.order_number }}</div>
          <div class="order-time">创建时间：{{ formatDateTime(o.create_time) }}</div>
        </div>
        <div class="order-main">
          <div class="order-route">
            <span class="train">{{ o.train_number }}</span>
            <span class="stations">{{ o.departure_station }} → {{ o.arrival_station }}</span>
            <span class="time">{{ formatDate(o.travel_date) }} {{ o.departure_time }}</span>
          </div>
          <div class="order-meta">
            <span :class="['status', statusClass(o.status)]">{{ o.status }}</span>
            <span class="price">¥{{ formatPrice(o.total_price) }}</span>
            <span class="count">{{ o.passenger_count }}人</span>
          </div>
          <div class="order-actions">
            <a v-if="o.status === '待支付'" href="javascript:;" @click="onPay(o.id)">立即支付</a>
            <a v-if="o.status === '待支付'" href="javascript:;" @click="onCancel(o.id)">取消订单</a>
            <a v-if="o.status === '已支付'" href="javascript:;" @click="onRefund(o.id)">退票</a>
            <router-link :to="`/order/${o.id}`">订单详情</router-link>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="order-empty">
      <img
        class="order-empty-img"
        src="https://kyfw.12306.cn/otn/images/center/empty.png"
        alt="暂无订单"
      />
      <p>您没有{{ emptyText }}的订单哦～</p>
      <p>
        您可以通过
        <a href="javascript:;" @click="goLeftTicket">车票预订</a>
        功能，来制定出行计划。
      </p>
    </div>

    <div class="warm-notice">
      <h4>温馨提示</h4>
      <ul>
        <li>席位已锁定，请在指定时间内完成网上支付。</li>
        <li>逾期未支付，系统将取消本次交易。</li>
        <li>在完成支付或取消本订单之前，您将无法购买其他车票。</li>
        <li>未尽事宜详见相关规定和车站公告。</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { message } from 'ant-design-vue'
import { getOrders, payOrder, cancelOrder, refundOrder } from '@/api/order'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('pending')
const orders = ref([])
const loading = ref(false)
const keyword = ref('')
const filterRange = ref('30')
const useMock = ref(false)
const mockOrders = ref([
  {
    id: 99901,
    order_number: 'MOCK20251123001',
    train_number: 'G1234',
    departure_station: '北京南',
    arrival_station: '上海虹桥',
    travel_date: new Date(new Date().setDate(new Date().getDate() + 7)).toISOString().slice(0, 10),
    departure_time: '08:00',
    total_price: '350.00',
    status: '待支付',
    passenger_count: 1,
    create_time: new Date().toISOString()
  }
])

const emptyText = computed(() => {
  if (activeTab.value === 'pending') return '未完成'
  if (activeTab.value === 'upcoming') return '未出行'
  return '历史'
})

const setTab = key => {
  if (activeTab.value !== key) {
    activeTab.value = key
  }
}

const fetchOrders = async () => {
  loading.value = true
  try {
    let statusParam = undefined
    if (activeTab.value === 'pending') statusParam = '待支付'
    if (activeTab.value === 'upcoming') statusParam = '已支付'
    if (activeTab.value === 'history') statusParam = '已取消'
    const res = await getOrders(statusParam ? { status: statusParam } : {})
    orders.value = Array.isArray(res.data) ? res.data : []
    if (!orders.value.length) {
      if (useMock.value) {
        orders.value = mockOrders.value
      }
    }
  } catch (e) {
    orders.value = useMock.value ? mockOrders.value : []
  } finally {
    loading.value = false
  }
}

watch(activeTab, fetchOrders, { immediate: true })

const formatPrice = p => {
  try {
    const n = typeof p === 'string' ? Number(p) : p
    return (n || 0).toFixed(2)
  } catch {
    return '0.00'
  }
}

const formatDate = d => {
  if (!d) return ''
  if (typeof d === 'string') return d
  try {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  } catch {
    return ''
  }
}

const formatDateTime = dt => {
  if (!dt) return ''
  try {
    const d = typeof dt === 'string' ? new Date(dt) : dt
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const h = String(d.getHours()).padStart(2, '0')
    const min = String(d.getMinutes()).padStart(2, '0')
    const s = String(d.getSeconds()).padStart(2, '0')
    return `${y}-${m}-${day} ${h}:${min}:${s}`
  } catch {
    return ''
  }
}

const applyFilters = () => {
  let list = [...orders.value]
  if (keyword.value.trim()) {
    const kw = keyword.value.trim()
    list = list.filter(
      o =>
        String(o.order_number).includes(kw) ||
        String(o.train_number).includes(kw) ||
        String(o.departure_station).includes(kw) ||
        String(o.arrival_station).includes(kw)
    )
  }
  orders.value = list
}

const statusClass = s => {
  if (s === '待支付') return 'status-pending'
  if (s === '已支付') return 'status-paid'
  if (s === '已取消') return 'status-cancel'
  if (s === '已退票' || s === '部分退票') return 'status-refund'
  return ''
}

const goLeftTicket = () => {
  router.push('/trains')
}

const onPay = async id => {
  try {
    await payOrder(id)
    message.success('支付请求已发起')
    fetchOrders()
  } catch (e) {
    message.error('支付失败或功能未开通')
  }
}

const onCancel = async id => {
  try {
    await cancelOrder(id)
    message.success('取消请求已发起')
    fetchOrders()
  } catch (e) {
    message.error('取消失败或功能未开通')
  }
}

const onRefund = async id => {
  try {
    await refundOrder(id, { passenger_ids: [] })
    message.success('退票请求已发起')
    fetchOrders()
  } catch (e) {
    message.error('退票失败或功能未开通')
  }
}
</script>

<style scoped>
.order-page {
  padding: 0 12px;
  font-family: Arial, Helvetica, 'Microsoft YaHei', sans-serif;
}
.subway-order {
  margin-top: 10px;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #f8f8f8;
  border: 1px solid #e5e5e5;
}
.tabs a {
  margin-right: 28px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
}
.tabs a.active {
  color: var(--primary-color);
  font-weight: 600;
  border-bottom: 2px solid var(--primary-color);
}
.filters {
  display: flex;
  gap: 8px;
}
.filters .search {
  width: 240px;
  height: 30px;
  border: 1px solid #e5e5e5;
  border-radius: 2px;
  padding: 0 8px;
}
.filters select {
  height: 30px;
  border: 1px solid #e5e5e5;
  border-radius: 2px;
  padding: 0 6px;
  background: #fff;
  color: #333;
}
.filters .btn {
  height: 30px;
  padding: 0 12px;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 2px;
  cursor: pointer;
}
.order-list {
  margin-top: 14px;
}
.order-item {
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 2px;
  margin-bottom: 12px;
}
.order-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #fafafa;
  border-bottom: 1px solid #e5e5e5;
  font-size: 12px;
  color: #666;
}
.order-main {
  display: grid;
  grid-template-columns: 1.6fr 0.8fr auto;
  gap: 16px;
  align-items: center;
  padding: 10px 16px;
}
.order-route {
  display: flex;
  gap: 12px;
  align-items: center;
}
.order-route .train {
  font-weight: 600;
  color: #333;
  font-size: 16px;
}
.order-route .stations {
  color: #333;
  font-size: 14px;
}
.order-route .time {
  color: #999;
  font-size: 13px;
}
.order-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}
.order-meta .status {
  color: #666;
  font-size: 13px;
}
.status-pending {
  color: #f59e0b;
}
.status-paid {
  color: #16a34a;
}
.status-cancel {
  color: #ef4444;
}
.status-refund {
  color: #3b82f6;
}
.order-meta .price {
  color: #333;
  font-weight: 600;
  font-size: 15px;
}
.order-actions {
  display: flex;
  gap: 12px;
}
.order-actions a,
.order-actions a:visited {
  color: var(--primary-color);
  text-decoration: none;
}
.order-actions a:hover {
  text-decoration: underline;
}
.order-empty {
  background: #f9fbff;
  border: 1px solid #d8e8ff;
  border-radius: 4px;
  padding: 16px;
  margin-top: 16px;
  color: #666;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.order-empty p {
  margin: 0 0 8px;
}
.order-empty a {
  color: var(--primary-color);
  text-decoration: none;
}
.order-empty a:hover {
  text-decoration: underline;
}
.order-empty-img {
  width: 140px;
  height: auto;
  margin-bottom: 10px;
}
.warm-notice {
  margin-top: 16px;
  background: #fff7ed;
  border: 1px solid #ffe1c2;
  border-radius: 4px;
  padding: 14px 16px;
}
.warm-notice h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #ff7f00;
}
.warm-notice ul {
  margin: 0;
  padding-left: 18px;
  color: #666;
}
.warm-notice li {
  line-height: 1.8;
}
</style>
