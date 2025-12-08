<template>
  <div class="order-page-content">
    <!-- Tabs -->
    <div class="panel-tab">
      <ul class="tab-list">
        <li :class="{ active: activeTab === 'pending' }" @click="setTab('pending')">
          <a href="javascript:;">未完成订单</a>
        </li>
        <li :class="{ active: activeTab === 'upcoming' }" @click="setTab('upcoming')">
          <a href="javascript:;">未出行订单</a>
        </li>
        <li :class="{ active: activeTab === 'history' }" @click="setTab('history')">
          <a href="javascript:;">历史订单</a>
        </li>
      </ul>
    </div>

    <!-- Filter Bar (Visible for Upcoming/History) -->
    <div class="order-query" v-if="activeTab !== 'pending'">
      <div class="query-form">
        <div class="query-item">
          <span class="label">按订票日期查询</span>
          <input type="date" v-model="startDate" class="input-date" />
          <span class="sep">-</span>
          <input type="date" v-model="endDate" class="input-date" />
        </div>
        <div class="query-item">
          <input
            type="text"
            v-model="keyword"
            class="input-keyword"
            placeholder="订单号/车次/姓名"
          />
          <button class="btn-query" @click="fetchOrders">查询</button>
        </div>
      </div>
    </div>

    <!-- Order List -->
    <div class="order-panel-box" v-if="orders.length">
      <!-- Header Row -->
      <div class="order-list-head">
        <span class="col-train">车次信息</span>
        <span class="col-passenger">旅客信息</span>
        <span class="col-seat">席位信息</span>
        <span class="col-price">票价</span>
        <span class="col-state">车票状态</span>
      </div>

      <!-- Orders -->
      <div v-for="order in orders" :key="order.id" class="order-item">
        <div class="order-item-hd">
          <a 
            href="javascript:;" 
            class="fold-btn" 
            :class="{ 'folded': order.folded }"
            @click="order.folded = !order.folded"
          >
             <!-- Icon set via CSS background -->
          </a>
          <span class="order-date">订票日期：{{ formatDate(order.create_time) }}</span>
          <span class="order-no" v-if="order.order_number">订单号：{{ order.order_number }}</span>
        </div>
        
        <!-- Body (collapsible) -->
        <div class="order-item-bd" v-show="!order.folded">
          <div class="train-info">
            <div class="train-name">
              <strong>{{ order.departure_station }}</strong>
              <span class="train-arrow">→</span>
              <strong>{{ order.arrival_station }}</strong>
              <span class="train-code">{{ order.train_number }}</span>
            </div>
            <div class="train-time">
              {{ formatDate(order.travel_date) }} {{ order.departure_time }} 开
            </div>
          </div>

          <!-- Passengers Loop -->
          <div class="passengers-info">
             <!-- If backend provides detailed passenger info, iterate here. For now, using order.passenger_count or mock -->
             <div class="passenger-row" v-for="(p, idx) in (order.passengers || mockPassengers(order))" :key="idx">
                <div class="p-name">
                  <div>{{ p.name }}</div>
                  <div class="id-type">{{ p.id_type || '居民身份证' }}</div>
                </div>
                <div class="p-seat">
                   <div>{{ p.seat_type || '二等座' }}</div>
                   <div>{{ p.seat_no || '02车09F号' }}</div>
                </div>
                <div class="p-price">
                   <div>{{ p.ticket_type || '成人票' }}</div>
                   <div class="price-val">{{ p.price || order.total_price }}元</div>
                </div>
                <div class="p-status">
                   <div v-if="p.refund_status === '已退票'">已退票</div>
                   <div v-else>
                     {{ order.status === '部分退票' ? '已支付' : order.status }}
                   </div>
                   <a 
                     href="javascript:;" 
                     v-if="(order.status === '已支付' || order.status === '部分退票') && p.refund_status !== '已退票'" 
                     class="link-btn" 
                     @click="handleRefundClick(order, p)"
                   >退票</a>
                </div>
             </div>
          </div>
        </div>
        
        <!-- Actions Footer -->
        <div class="order-item-ft" v-if="order.status === '待支付'" v-show="!order.folded">
           <div class="ft-right">
             <button class="btn-cancel" @click="onCancel(order.id)">取消订单</button>
             <button class="btn-pay" @click="onPay(order.id)">去支付</button>
           </div>
        </div>
        <div class="order-item-ft" v-else v-show="!order.folded">
           <div class="ft-right">
             <router-link :to="`/order/${order.id}`" class="btn-detail">订单详情</router-link>
             
             <template v-if="order.status === '已支付'">
               <a href="javascript:;" class="btn-common">添加免费乘车儿童</a>
               <a href="javascript:;" class="btn-common">购/赠/退保险</a>
               <a href="javascript:;" class="btn-common">改签</a>
               <a href="javascript:;" class="btn-common">变更到站</a>
               <a href="javascript:;" class="btn-common">餐饮·特产</a>
             </template>
           </div>
        </div>
      </div>
      
      <!-- Pagination (Mock) -->
      <div class="pagination">
        <span>共 1 页</span>
        <span class="current">1</span>
        <span>到</span>
        <input type="text" value="1" class="page-input" />
        <span>页</span>
        <button class="btn-ok">确定</button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="order-empty">
      <div class="empty-pic">
        <!-- Use local or remote empty image -->
         <img src="https://kyfw.12306.cn/otn/images/center/empty.png" alt="暂无订单" />
      </div>
      <div class="empty-txt">
        <p>您没有{{ emptyText }}的订单哦～</p>
        <p>
          您可以通过
          <router-link to="/leftTicket/single">车票预订</router-link>
          功能，来制定出行计划。
        </p>
      </div>
    </div>

    <!-- Warm Tips -->
    <div class="warm-tips-box">
      <div class="tips-tit">温馨提示</div>
      <div class="tips-con">
        <template v-if="activeTab === 'pending'">
          <p>1. 席位已锁定，请在指定时间内完成网上支付。</p>
          <p>2. 逾期未支付，系统将取消本次交易。</p>
          <p>3. 在完成支付或取消本订单之前，您将无法购买其他车票。</p>
          <p>4. 未尽事宜详见《国铁集团铁路旅客运输规程》《广深港高速铁路跨境旅客运输组织规则》《中老铁路跨境旅客联运组织规则》等有关规定和车站公告。</p>
        </template>
        <template v-else>
           <p>1. 订单信息保存期限为30日。</p>
           <p>2. 在12306.cn网站改签和退票，改签应不晚于票面日期当日24:00，变更到站不晚于开车前48小时，退票应不晚于开车前。</p>
           <p>3. 在本网站办理退票，只能逐次单张办理。</p>
           <p>4. 车票改签、变更到站均只能办理一次。已经改签或变更到站的车票不再办理改签；对已改签车票、团体票暂不提供“变更到站”服务。</p>
           <p>5. 退票、改签、变更到站后，如有应退票款，按购票时所使用的在线支付工具相关规定，将在规定时间内退还至原在线支付工具账户，请及时查询。</p>
           <p>6. 投保、退保或查看电子保单状态，请点击“我的保险”或“购/赠/退保险”。</p>
           <p>7. 按“除有效期有其他规定的车票外，车票当日当次有效。旅客自行中途上车、下车的，未乘区间的票款不予退还。”</p>
        </template>
      </div>
    </div>


    <!-- Refund Modal -->
    <div v-if="refundModalVisible" class="modal-backdrop" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999;"></div>
    <div v-if="refundModalVisible" role="alertdialog" tabindex="-1" aria-label="提示框" class="modal" style="display: block; position: fixed; width: 540px; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000;">
      <a href="javascript:;" title="关闭" class="modal-close" @click="refundModalVisible = false"><i class="icon icon-close"></i></a>
      <div class="modal-hd">
        <div class="modal-tit">退票申请</div>
      </div>
      <div class="modal-bd">
        <div class="message">
          <div class="msg-ico"><i class="icon icon-doubt"></i></div>
          <div class="msg-con">
            <h2 class="msg-tit" tabindex="0">您确认要退票吗？</h2>
            <div class="msg-info">如有订餐饮或特产，请按规定到网站自行办理退订。</div>
          </div>
        </div>
        <div class="order-cancel-tips">
          <ul class="order-cancel-count">
            <li>共计退款：<span class="txt-price txt-lg">{{ currentRefundTicket?.price }}元</span></li>
            <li>手续费用：<span class="txt-price txt-lg">0元</span><span class="txt-light">（当前时间退票不收取手续费）</span></li>
            <li>车票票价：<span class="txt-price txt-lg">{{ currentRefundTicket?.price }}元</span></li>
            <li>应退票款：<span class="txt-price txt-lg">{{ currentRefundTicket?.price }}元</span></li>
          </ul>
          <div class="order-cancel-txt"><i class="icon icon-plaint-fill mr"></i>实际核收退票费及应退票款将按最终交易时间计算。</div>
          <div class="order-cancel-txt"><i class="icon icon-plaint-fill mr"></i>如你需要办理该次列车前续、后续退票业务，请于退票车次票面开车时间前办理。<div class="txt-second"></div></div>
        </div>
      </div>
      <div class="modal-ft">
        <a href="javascript:;" class="btn cancel" @click="refundModalVisible = false">取消</a>
        <a href="javascript:;" class="btn btn-primary ok" @click="confirmRefund">确定</a>
      </div>
      <div class="modal-ft-tips">
        <p>1. 使用现金购买或已领取报销凭证的电子票，线上完成退票后，请持相关证件（购票证件、报销凭证）至车站窗口完成退款。如您同时购买了“乘意险”，可在车站窗口退款时一并办理。</p>
        <p>2. 退票费按如下规则核收：票面乘车站开车时间前8天（含）以上不收取退票费，48小时以上的按票价5%计，24小时以上、不足48小时的按票价10%计，不足24小时的按票价20%计。上述计算的尾数以5角为单位，尾数小于2.5角的舍去、2.5角（含）以上且小于7.5角的计为5角、7.5角（含）以上的进为1元。退票费最低按2元计收。更多退票规则请查看<a class="txt-primary" href="https://mobile.12306.cn/otsmobile/h5/otsbussiness/info/orderWarmTips.html" target="_blank">《退改说明》</a>。</p>
        <p>3. 应退款项按银行规定时限退还至购票时所使用的网上支付工具账户，请注意查询，如有疑问请致电12306 人工客服查询。</p>
        <p>4. 跨境旅客旅行须知详见铁路跨境旅客相关运输组织规则和车站公告。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { getOrders, payOrder, cancelOrder, refundOrder } from '@/api/order'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'

const router = useRouter()
const activeTab = ref('pending')
const orders = ref([])
const loading = ref(false)
const keyword = ref('')
const startDate = ref(dayjs().subtract(30, 'day').format('YYYY-MM-DD'))
const endDate = ref(dayjs().format('YYYY-MM-DD'))

// Refund Modal State
const refundModalVisible = ref(false)
const currentRefundTicket = ref(null)

const setTab = (tab) => {
  activeTab.value = tab
}

const emptyText = computed(() => {
  if (activeTab.value === 'pending') return '未完成'
  if (activeTab.value === 'upcoming') return '未出行'
  return '历史'
})

const formatDate = (d) => {
  if (!d) return ''
  return dayjs(d).format('YYYY-MM-DD')
}

// Mock logic for passengers if not in API response
const mockPassengers = (order) => {
  // Try to parse order_passengers if available, otherwise mock
  if (order.order_passengers && order.order_passengers.length) {
     return order.order_passengers.map(p => ({
         passenger_id: p.passenger_id || 12345,
         name: p.passenger_name || '张三',
         id_type: '居民身份证',
         seat_type: p.seat_type || '二等座',
         seat_no: '02车09F号', // Mock seat no
         ticket_type: p.ticket_type || '成人票',
         price: p.price || order.total_price
     }))
  }
  return [{
    passenger_id: 12345,
    name: '乌梁海奥都',
    id_type: '居民身份证',
    seat_type: '二等座',
    seat_no: '02车09F号',
    ticket_type: '成人票',
    price: order.total_price
  }]
}

const fetchOrders = async () => {
  loading.value = true
  try {
    let statusParam = undefined
    if (activeTab.value === 'pending') statusParam = '待支付'
    if (activeTab.value === 'upcoming') statusParam = ['已支付', '部分退票', '已退票']
    if (activeTab.value === 'history') statusParam = '已取消' // Or handle completed
    
    // Note: Backend API might differ, adjusting to match common patterns
    const res = await getOrders({ status: statusParam })
    if (res.data) {
      orders.value = res.data.map(o => ({ ...o, folded: false }))
    } else {
      orders.value = []
    }
  } catch (e) {
    console.error(e)
    orders.value = []
  } finally {
    loading.value = false
  }
}

const onCancel = (id) => {
  Modal.confirm({
    title: '确认取消',
    content: '您确定要取消该订单吗？',
    onOk: async () => {
      try {
        await cancelOrder(id)
        message.success('订单已取消')
        fetchOrders()
      } catch (e) {
        message.error('取消失败')
      }
    }
  })
}

const onPay = (id) => {
  // Redirect to pay or show pay modal
  // For now, just call API to mark paid (simulated) or redirect
  // Assuming payOrder API exists
  Modal.confirm({
      title: '支付',
      content: '确认支付该订单？',
      onOk: async () => {
          try {
              await payOrder(id)
              message.success('支付成功')
              fetchOrders()
          } catch(e) {
              message.error('支付失败')
          }
      }
  })
}

const handleRefundClick = (order, passenger) => {
  currentRefundTicket.value = {
    orderId: order.id,
    passengerId: passenger.passenger_id,
    passengerName: passenger.name,
    price: passenger.price,
  }
  refundModalVisible.value = true
}

const confirmRefund = async () => {
  if (!currentRefundTicket.value) return
  try {
    await refundOrder(currentRefundTicket.value.orderId, {
       passenger_ids: [currentRefundTicket.value.passengerId]
    })
    message.success('退票成功')
    refundModalVisible.value = false
    fetchOrders()
  } catch(e) {
    message.error(e.response?.data?.message || '退票失败')
  }
}

watch(activeTab, fetchOrders, { immediate: true })
</script>

<style scoped>
@import '@/assets/12306-order/center.css';
@import '@/assets/12306-order/ticket_index_v70004.css';
/* @import '@/assets/12306-order/iconfont.css'; */ /* Already imported via center/ticket css if they do */
@import '@/assets/12306-order/iconfont.css';

/* Custom styles to match 12306 if CSS files miss something */

.order-page-content {
  font-family: "Microsoft YaHei", "SimSun", sans-serif;
  color: #333;
}

.order-page-content * {
  box-sizing: border-box;
}

/* Tabs */
.panel-tab {
  border-bottom: 2px solid #3B99FC;
  height: 32px;
  margin-bottom: 20px;
}
.tab-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.tab-list li {
  float: left;
  height: 30px;
  line-height: 30px;
  margin-right: 5px;
  border: 1px solid #ddd;
  border-bottom: none;
  background: #f8f8f8;
}
.tab-list li.active {
  background: #3B99FC;
  border-color: #3B99FC;
}
.tab-list li a {
  display: block;
  padding: 0 20px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
}
.tab-list li.active a {
  color: #fff;
}

/* Query Bar */
.order-query {
  border: 1px solid #dedede;
  background: #f8f8f8;
  padding: 15px;
  margin-bottom: 15px;
}
.query-form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.query-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}
.input-date {
  border: 1px solid #cfcfcf;
  padding: 4px;
  width: 120px;
}
.input-keyword {
  border: 1px solid #cfcfcf;
  padding: 4px;
  width: 200px;
  color: #999;
}
.btn-query {
  background: #ffb400; /* Orange/Yellowish */
  border: 1px solid #ffb400;
  color: #fff;
  padding: 4px 15px;
  cursor: pointer;
  border-radius: 3px;
}

/* Order List */
.order-panel-box {
  border: 1px solid #dedede;
}
.order-list-head {
  background: #f8f8f8;
  height: 32px;
  line-height: 32px;
  border-bottom: 1px solid #dedede;
  display: flex;
  font-size: 12px;
  color: #666;
  text-align: center;
}
.col-train { width: 35%; }
.col-passenger { width: 20%; }
.col-seat { width: 15%; }
.col-price { width: 15%; }
.col-state { width: 15%; }

.order-item {
  border-bottom: 1px solid #dedede;
}
.order-item:last-child {
  border-bottom: none;
}
.order-item-hd {
  background: #f0f8ff; /* Light blueish */
  padding: 8px 15px;
  font-size: 12px;
  color: #666;
  border-bottom: 1px dashed #dedede;
}
.order-date { margin-right: 20px; }

.order-item-bd {
  display: flex;
  padding: 0; /* Remove padding to let borders touch edges */
}
.train-info {
  width: 35%;
  padding: 30px 20px 20px; /* Increase top padding */
  border-right: 1px solid #dedede;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center; /* Center horizontally */
}
.train-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
}
.train-arrow { margin: 0 10px; font-family: sans-serif; }
.train-code { margin-left: 10px; }
.train-time { color: #999; font-size: 12px; }

.passengers-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.passenger-row {
  display: flex;
  text-align: center;
  font-size: 12px;
  flex: 1; /* Make sure it fills height if only one row */
  border-bottom: 1px solid #eee;
}
.passenger-row:last-child { border-bottom: none; }

/* Adjusted widths to sum to 100% of the remaining 65% space */
/* 20/65 ≈ 30.76%, 15/65 ≈ 23.07% */
.p-name { 
  width: 30.76%; 
  color: #333; 
  border-right: 1px solid #dedede; 
  padding: 15px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.p-seat { 
  width: 23.08%; 
  border-right: 1px solid #dedede; 
  padding: 15px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.p-price { 
  width: 23.08%; 
  color: #ff8200; 
  font-weight: bold; 
  border-right: 1px solid #dedede; 
  padding: 15px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.p-status { 
  width: 23.08%; 
  color: #333; 
  padding: 15px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.id-type { color: #999; margin-top: 4px; }
.price-val { font-size: 14px; }
.link-btn { color: #0077cc; text-decoration: none; margin-top: 4px; display: block;}

.order-item-ft {
  padding: 10px 20px;
  border-top: 1px dashed #dedede;
  text-align: right;
  background: #fff;
}
.btn-cancel {
  background: #fff;
  border: 1px solid #dedede;
  padding: 5px 15px;
  margin-right: 10px;
  cursor: pointer;
  color: #666;
  border-radius: 3px;
}
.btn-pay, .btn-detail {
  background: #ff8200;
  border: 1px solid #ff8200;
  color: #fff;
  padding: 5px 25px;
  cursor: pointer;
  border-radius: 3px;
  text-decoration: none;
  display: inline-block;
}
.btn-pay:hover {
  background: #ff9933;
  border-color: #ff9933;
}

/* Pagination */
.pagination {
  padding: 20px;
  text-align: center;
  font-size: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.current {
  background: #3B99FC;
  color: #fff;
  padding: 2px 8px;
  margin: 0 5px;
  line-height: 1.5;
}
.page-input {
  width: 30px;
  text-align: center;
  margin: 0 5px;
  height: 22px;
  line-height: 22px;
  border: 1px solid #ccc;
}
.btn-ok {
  margin-left: 5px;
  cursor: pointer;
  height: 22px;
  line-height: 18px; /* Adjust for border/padding */
  padding: 0 10px;
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 2px;
}

/* Empty */
.order-empty {
  padding: 50px;
  text-align: center;
  border: 1px solid #dedede;
  background: #fff;
}
.order-empty img {
  margin: 0 auto 20px;
}
.empty-txt {
  color: #666;
  font-size: 14px;
}
.empty-txt a {
  color: #3B99FC;
}

/* Warm Tips */
.warm-tips-box {
  border: 1px solid #ffce9d;
  background: #fffbf5;
  padding: 15px;
  margin-top: 20px;
}
.tips-tit {
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  font-size: 14px;
}
.tips-con p {
  font-size: 12px;
  color: #666;
  line-height: 24px;
  margin: 0;
}

/* Fold Button Icon */
.fold-btn {
  display: inline-block;
  width: 30px; 
  height: 30px;
  vertical-align: middle;
  margin-right: 5px;
  background: url('@/assets/12306-order/fold.png') no-repeat center center;
  cursor: pointer;
}
.fold-btn.folded {
  background-image: url('@/assets/12306-order/unfold.png');
}

/* Common Buttons in Footer */
.btn-common {
  display: inline-block;
  margin-left: 10px;
  color: #333;
  font-size: 12px;
  text-decoration: none;
  vertical-align: middle;
  background: #fff;
  border: 1px solid #dedede;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}
.btn-common:hover {
  color: #FF8200;
  border-color: #FF8200;
  text-decoration: none;
}
</style>
