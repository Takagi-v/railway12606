<template>
  <div class="order-detail">
    <Header12306 />
    <div class="wrapper">
      <div class="breadcrumb">
        <a-breadcrumb>
          <a-breadcrumb-item><router-link to="/user/orders">我的订单</router-link></a-breadcrumb-item>
          <a-breadcrumb-item>订单详情</a-breadcrumb-item>
        </a-breadcrumb>
      </div>

      <a-spin :spinning="loading">
        <div class="detail-card" v-if="order">
          <div class="header">
            <div class="status-row">
              <span class="label">订单状态：</span>
              <span class="status-text" :class="statusClass">{{ order.status }}</span>
            </div>
            <div class="order-no">订单号：{{ order.order_number }}</div>
            <div class="order-time">下单时间：{{ formatTime(order.create_time) }}</div>
          </div>

          <div class="section train-info">
            <div class="section-title">车次信息</div>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">车次：</span>
                <span class="value">{{ order.train_number }}</span>
              </div>
              <div class="info-item">
                <span class="label">出发站：</span>
                <span class="value">{{ order.departure_station }}</span>
              </div>
              <div class="info-item">
                <span class="label">到达站：</span>
                <span class="value">{{ order.arrival_station }}</span>
              </div>
              <div class="info-item">
                <span class="label">乘车日期：</span>
                <span class="value">{{ order.travel_date }}</span>
              </div>
              <div class="info-item">
                <span class="label">出发时间：</span>
                <span class="value">{{ order.departure_time }}</span>
              </div>
              <div class="info-item">
                <span class="label">到达时间：</span>
                <span class="value">{{ order.arrival_time }}</span>
              </div>
            </div>
          </div>

          <div class="section passenger-info">
            <div class="section-title">乘客信息</div>
            <a-table
              :dataSource="order.passengers"
              :columns="columns"
              :pagination="false"
              rowKey="id_number"
              size="middle"
            />
          </div>

          <div class="section price-info">
            <div class="total-price">
              总计：<span class="price">￥{{ order.total_price }}</span>
            </div>
          </div>

          <div class="actions" v-if="order.status === '待支付'">
            <a-button @click="handleCancel" :loading="actionLoading">取消订单</a-button>
            <a-button type="primary" @click="handlePay" :loading="actionLoading">立即支付</a-button>
          </div>
          <div class="actions" v-if="order.status === '已支付' || order.status === '部分退票'">
             <a-button danger @click="handleRefund" :loading="actionLoading">退票</a-button>
          </div>
        </div>
        <div v-else-if="!loading" class="empty-state">
          <a-empty description="未找到订单信息" />
        </div>
      </a-spin>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { getOrderDetail, payOrder, cancelOrder, refundOrder } from '@/api/order'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const actionLoading = ref(false)
const order = ref(null)

const columns = [
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '证件类型', dataIndex: 'id_number', key: 'id_type', customRender: () => '身份证' }, 
  { title: '证件号码', dataIndex: 'id_number', key: 'id_number' },
  { title: '票种', dataIndex: 'ticket_type', key: 'ticket_type' },
  { title: '席别', dataIndex: 'seat_type', key: 'seat_type' },
  { title: '车厢/座位', key: 'seat_number', customRender: ({ record }) => record.seat_number || '待分配' },
  { title: '票价', dataIndex: 'price', key: 'price', customRender: ({ text }) => `￥${text}` },
  { 
    title: '状态', 
    key: 'refund_status', 
    customRender: ({ record }) => {
       if (record.refund_status === '已退票') return '已退票'
       return '正常'
    }
  }
]

const statusClass = computed(() => {
  if (!order.value) return ''
  switch (order.value.status) {
    case '待支付': return 'status-pending'
    case '已支付': return 'status-paid'
    case '已取消': return 'status-canceled'
    case '已退票': return 'status-canceled'
    case '部分退票': return 'status-paid'
    default: return ''
  }
})

const fetchOrder = async () => {
  const id = route.params.id
  if (!id) return
  loading.value = true
  try {
    const res = await getOrderDetail(id)
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (e) {
    message.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

const formatTime = (time) => {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm:ss') : '-'
}

const handlePay = async () => {
  if (!order.value) return
  actionLoading.value = true
  try {
    const res = await payOrder(order.value.id)
    if (res.code === 200) {
      message.success('支付成功')
      await fetchOrder()
    } else {
        message.error(res.message || '支付失败')
    }
  } catch (e) {
    message.error('支付失败')
  } finally {
    actionLoading.value = false
  }
}

const handleCancel = () => {
  Modal.confirm({
    title: '确认取消订单',
    content: '取消后订单信息将被删除，是否确认？',
    okText: '确认取消',
    cancelText: '暂不取消',
    onOk: async () => {
      actionLoading.value = true
      try {
        const res = await cancelOrder(order.value.id)
        if (res.code === 200) {
          message.success('订单已取消')
          router.push('/user/orders')
        } else {
             message.error(res.message || '取消失败')
        }
      } catch (e) {
        message.error('取消失败')
      } finally {
        actionLoading.value = false
      }
    }
  })
}

const handleRefund = () => {
  Modal.confirm({
    title: '确认退票',
    content: '退票将收取5%手续费，确认要退票吗？（将退还所有乘客）',
    okText: '确认退票',
    cancelText: '取消',
    onOk: async () => {
      actionLoading.value = true
      try {
        const res = await refundOrder(order.value.id, { passenger_ids: [] })
        if (res.code === 200) {
          message.success(res.message || '退票成功')
          await fetchOrder()
        } else {
             message.error(res.message || '退票失败')
        }
      } catch (e) {
        message.error('退票失败')
      } finally {
        actionLoading.value = false
      }
    }
  })
}

onMounted(() => {
  fetchOrder()
})
</script>

<style scoped>
.order-detail {
  background: #f5f7fa;
  min-height: 100vh;
}
.wrapper {
  width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
}
.breadcrumb {
  margin-bottom: 20px;
}
.detail-card {
  background: #fff;
  padding: 24px;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.header {
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
}
.status-row {
  font-size: 18px;
  margin-bottom: 10px;
}
.status-text {
  font-weight: bold;
}
.status-pending { color: #faad14; }
.status-paid { color: #52c41a; }
.status-canceled { color: #999; }

.order-no, .order-time {
  color: #666;
  margin-bottom: 5px;
}

.section {
  margin-bottom: 30px;
}
.section-title {
  font-size: 16px;
  font-weight: bold;
  border-left: 4px solid #1890ff;
  padding-left: 10px;
  margin-bottom: 20px;
}
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.info-item {
  display: flex;
}
.label {
  color: #999;
  width: 80px;
}
.value {
  color: #333;
  font-weight: 500;
}
.total-price {
  text-align: right;
  font-size: 16px;
  font-weight: bold;
}
.price {
  color: #ff4d4f;
  font-size: 24px;
}
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}
.empty-state {
  padding: 100px 0;
  background: #fff;
  border-radius: 4px;
}
</style>