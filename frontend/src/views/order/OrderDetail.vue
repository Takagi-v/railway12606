<template>
  <div class="order-detail-page">
    <Header12306 />
    <div class="wrapper content">
      <!-- 面包屑 -->
      <div class="breadcrumb">
        当前位置：<router-link to="/user/orders">个人中心</router-link><span class="sep">&gt;</span><span class="active">订单详情</span>
      </div>
      
      <!-- 个人中心 -->
      <a-spin :spinning="loading">
        <div class="panel-tab" v-if="order">
          <div class="tab-hd">
            <ul class="tab-hd-list">
              <li :class="{ active: activeTab === 'tracking' }" @click="activeTab = 'tracking'">
                <a href="javascript:;">订单跟踪</a>
              </li>
              <li :class="{ active: activeTab === 'refund' }" @click="activeTab = 'refund'">
                <a href="javascript:;">退款详情</a>
              </li>
              <li :class="{ active: activeTab === 'insurance' }" @click="activeTab = 'insurance'">
                <a href="javascript:;">购/赠/退保险</a>
              </li>
              <li :class="{ active: activeTab === 'children' }" @click="activeTab = 'children'">
                <a href="javascript:;">免费乘车儿童</a>
              </li>
            </ul>
          </div>
          
          <div class="tab-bd">
            <!-- 订单跟踪 -->
            <div id="J-order-detail" class="tab-item" v-show="activeTab === 'tracking'">
              <div class="order-tracking">
                <div class="order-tracking-hd">
                  <!-- 锯齿边缘 -->
                  <div class="ticket-edge"></div>
                  <div class="tracking-hd-content">
                    <div class="tracking-hd-tit">订单信息</div>
                    <div class="tracking-hd-con">
                      <div class="hd-label">订票日期：</div>
                      <div class="hd-value">{{ formatDate(order.create_time) }}</div>
                    </div>
                    <div class="tracking-hd-con">
                      <div class="hd-label">订单编号：</div>
                      <div class="hd-value">{{ order.order_number }}</div>
                    </div>
                  </div>
                </div>
                <div class="order-tracking-bd">
                  <ul class="tracking-status" v-if="trackingEvents.length">
                    <li 
                      v-for="(event, idx) in trackingEvents" 
                      :key="idx" 
                      class="status-item status-item-newdate"
                      :class="{ 'status-item-today': idx === 0 }"
                    >
                      <i class="s-dot"></i>
                      <span class="s-date">{{ event.date }}</span>
                      <div class="status-txt">{{ event.time }} {{ event.action }}</div>
                      <div class="status-txt txt-second">{{ event.detail }}</div>
                    </li>
                  </ul>
                  <div v-else class="no-tracking">
                    暂无订单跟踪信息
                  </div>
                </div>
              </div>
              
              <div class="tips-box mt-lg">
                <h4 class="tips-tit">温馨提示</h4>
                <p>1.订单信息查询有效期限为30日。</p>
                <p>2.在12306.cn网站改签和退票，改签应不晚于票面日期当日24:00，变更到站不晚于开车前48小时，退票应不晚于开车前。</p>
                <p>3.在本网站办理退票，只能逐次单张办理。</p>
                <p>4.车票改签、变更到站均只能办理一次。已经改签或变更到站的车票不再办理改签;对已改签车票、团体票暂不提供"变更到站"服务。</p>
              </div>
            </div>
            
            <!-- 退款详情 -->
            <div id="J-order-refund" class="tab-item" v-show="activeTab === 'refund'">
              <div class="order-panel order-panel-refund" v-if="refundRecords.length">
                <div class="order-item mt0" v-for="(record, idx) in refundRecords" :key="idx">
                  <div class="order-item-bd">
                    <table class="order-item-table">
                      <colgroup>
                        <col class="col-info">
                        <col class="col-result">
                        <col class="col-num">
                        <col>
                      </colgroup>
                      <tbody>
                        <tr>
                          <th>退款信息</th>
                          <th>明细</th>
                          <th>流水号</th>
                          <th>状态</th>
                        </tr>
                        <tr>
                          <td class="td-left">
                            <div class="txt-light">退款金额：<span class="txt-price">￥<span class="txt-mlg">{{ record.amount }}</span></span></div>
                            <div class="txt-light">来源：<span class="txt-primary">已退票</span></div>
                            <div class="txt-light">申请时间：<span class="txt-price">{{ record.applyTime }}</span></div>
                          </td>
                          <td>
                            <div class="txt-success">{{ record.passengerName }}已退票</div>
                          </td>
                          <td>
                            <div>{{ record.serialNo }}</div>
                          </td>
                          <td class="td-left br-none">
                            <span class="txt-success">成功</span>，已成功退至银行，如已超过7个工作日尚未到账，请持支付银行卡至发卡行查询。
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <!-- 无退款信息 -->
              <div class="order-empty-inline" v-else>
                <div class="empty-pic"><img src="https://kyfw.12306.cn/otn/images/center/empty.png" alt=""></div>
                <div class="empty-txt">
                  <p class="empty-tit">您没有对应的退款信息哦~</p>
                </div>
              </div>
              
              <div class="tips-box mt-lg">
                <h4 class="tips-tit">温馨提示</h4>
                <p>1.退票、改签、变更到站后，如有应退票款，按购票时所使用的在线支付工具相关规定，将在规定时间内退还至原在线支付工具账户，请及时查询；如超过7个工作日尚未到账，请致电铁路客服12306进行查询。</p>
                <p>2.应退票款按银行规定时限退还至购票时所使用的网上支付工具账户，请注意查询，如有疑问请致电12306 人工客服查询。</p>
              </div>
            </div>
            
            <!-- 购/赠/退保险 -->
            <div id="J-order-insurance" class="tab-item" v-show="activeTab === 'insurance'">
              <!-- 没有保险信息 -->
              <div class="order-empty-inline">
                <div class="empty-pic"><img src="https://kyfw.12306.cn/otn/images/center/empty.png" alt=""></div>
                <div class="empty-txt">
                  <p class="empty-tit">您没有对应的保险信息哦~</p>
                </div>
              </div>
              
              <div class="tips-box mt-lg">
                <h4 class="tips-tit">温馨提示</h4>
                <p>1.已投保的中国居民身份证父母点击"立即投保/领取赠保"，可为其免费携带的一名未满6周岁且不单独占用席位并通过中国居民身份证核验的子女，领取中国铁路保险赠送的一份乘意险。</p>
                <p>2.办理车票改签、变更到站后，电子保单按改签、变更到站后车票信息自动批改，保单号不变。</p>
                <p>3.办理退票或单独退保后，相应保险合同自动解除，已退保费按银行规定时限退回投保银行卡。</p>
                <p>4.退保后如再投保，请点击"立即投保/领取赠保"。</p>
                <p>5.成年人保险方案共3种，保险费分别为1元、3元、5元乘意险。</p>
                <p>6.请您充分理解保险责任、责任免除、保险期间、合同解除等约定，凭电子保单查询号登录 <a href="http://www.china-ric.com" target="_blank" class="txt-primary">www.china-ric.com</a> 查看电子保单。</p>
              </div>
            </div>
            
            <!-- 免费乘车儿童 -->
            <div id="J-order-children" class="tab-item" v-show="activeTab === 'children'">
              <div class="txt_top_yellow">
                *自2023年1月1日起，每一名持票成年人旅客可免费携带一名未满6周岁且不单独占用席位的儿童乘车，
                超过一名时，超过人数应购买儿童优惠票。免费乘车儿童可以在购票成功后申明。
              </div>
              <div class="blue_border_box">
                <div class="blue_bg_box">列车行程信息</div>
                <div class="train_box">
                  <p class="txt_train">
                    {{ order.departure_station }}站
                    <span>→</span>
                    {{ order.arrival_station }}站
                    {{ order.train_number }}
                  </p>
                  <p>{{ formatDate(order.travel_date) }}（{{ getWeekday(order.travel_date) }}）</p>
                </div>
                <div class="blue_bg_box header-row">
                  <p>序号
                    <span class="th_box">旅客信息</span>
                    <span class="th_box">车厢席位</span>
                  </p>
                </div>
                <div class="table_box">
                  <table border="1" frame="void" width="100%" cellpadding="20">
                    <tbody>
                      <tr class="tr_box" v-for="(p, idx) in passengers" :key="idx">
                        <td align="center" width="60px">{{ idx + 1 }}</td>
                        <td align="center" width="270px">{{ p.name }} {{ maskIdNumber(p.id_number) }}</td>
                        <td align="center" width="270px">{{ formatSeatType(p.seat_type) }} {{ p.seat_number || '待分配' }}</td>
                        <td class="td_box_1">
                          <span v-if="isRefunded(p.refund_status)">已退票</span>
                          <span v-else>—</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div class="tips_box">
                <h4 class="tips_tit">温馨提示</h4>
                <p>1. 随同成年人乘车的儿童，年满6周岁且未满14周岁的应当购买儿童优惠票；年满14周岁，应购买全价票。</p>
                <p>2. 旅客携带免费乘车儿童时，应当向承运人提前申明，并取得免费乘车儿童的乘车凭证。</p>
                <p>3. 免费乘车的儿童单独使用席位时应购买儿童优惠票。</p>
                <p>4. 儿童优惠票的乘车日期、车次及席别应与同行成年人所持车票相同，其到站不得远于成年人车票的到站。</p>
                <p>5. 儿童应随同成年人旅客乘车。乘坐卧铺时，2名儿童或1名成年人带1名儿童可共用一个卧铺。</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="!loading" class="order-empty-full">
          <div class="empty-pic"><img src="https://kyfw.12306.cn/otn/images/center/empty.png" alt=""></div>
          <div class="empty-txt">
            <p class="empty-tit">未找到订单信息</p>
            <p>请检查订单编号是否正确，或 <router-link to="/user/orders">返回订单列表</router-link></p>
          </div>
        </div>
      </a-spin>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { getOrderDetail } from '@/api/order'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const order = ref(null)
const activeTab = ref('tracking')

// 席别映射
const seatTypeMap = {
  'first_class': '一等座',
  'second_class': '二等座', 
  'soft_sleeper': '软卧',
  'hard_sleeper': '硬卧',
  'hard_seat': '硬座',
  'no_seat': '无座'
}

const formatSeatType = (seatType) => {
  if (!seatType) return ''
  return seatTypeMap[seatType] || seatType
}

// 判断是否已退票
const isRefunded = (status) => {
  return status === 'refunded' || status === '已退票'
}

// 判断是否已支付
const isPaid = (status) => {
  return status === 'paid' || status === '已支付' || 
         status === 'partially_refunded' || status === '部分退票' ||
         status === 'refunded' || status === '已退票'
}

// 乘客信息
const passengers = computed(() => {
  if (!order.value) return []
  return order.value.passengers || order.value.order_passengers || []
})

// 订单跟踪事件
const trackingEvents = computed(() => {
  if (!order.value) return []
  
  const events = []
  const passengerList = passengers.value
  
  console.log('Order status:', order.value.status)
  console.log('Passengers:', passengerList)
  
  // 已退票的旅客事件
  passengerList.forEach(p => {
    if (isRefunded(p.refund_status)) {
      events.push({
        date: formatDateWithWeekday(p.refund_time || order.value.update_time || new Date()),
        time: formatTime(p.refund_time || order.value.update_time || new Date()),
        action: '已退票(互联网/手机端)',
        detail: `${p.name} ${order.value.train_number}（${formatSeatType(p.seat_type)} ${p.seat_number || '待分配'}）${order.value.departure_station}-${order.value.arrival_station}`,
        timestamp: dayjs(p.refund_time || order.value.update_time || new Date()).valueOf()
      })
    }
  })
  
  // 已支付事件
  if (isPaid(order.value.status)) {
    passengerList.forEach(p => {
      events.push({
        date: formatDateWithWeekday(order.value.pay_time || order.value.create_time),
        time: formatTime(order.value.pay_time || order.value.create_time),
        action: '已支付(互联网/手机端)',
        detail: `${p.name} ${order.value.train_number}（${formatSeatType(p.seat_type)} ${p.seat_number || '待分配'}）${order.value.departure_station}-${order.value.arrival_station}`,
        timestamp: dayjs(order.value.pay_time || order.value.create_time).valueOf()
      })
    })
  }
  
  // 待支付事件
  if (order.value.status === 'pending' || order.value.status === '待支付') {
    passengerList.forEach(p => {
      events.push({
        date: formatDateWithWeekday(order.value.create_time),
        time: formatTime(order.value.create_time),
        action: '订单已提交，等待支付',
        detail: `${p.name} ${order.value.train_number}（${formatSeatType(p.seat_type)} ${p.seat_number || '待分配'}）${order.value.departure_station}-${order.value.arrival_station}`,
        timestamp: dayjs(order.value.create_time).valueOf()
      })
    })
  }
  
  // 按时间排序，最新的在前
  return events.sort((a, b) => b.timestamp - a.timestamp)
})

// 退款记录
const refundRecords = computed(() => {
  if (!order.value) return []
  
  const records = []
  const refundedPassengers = passengers.value.filter(p => isRefunded(p.refund_status))
  
  refundedPassengers.forEach((p, idx) => {
    records.push({
      amount: p.refund_amount || p.price || (order.value.total_price / passengers.value.length),
      passengerName: p.name,
      applyTime: formatDateTime(p.refund_time || order.value.update_time),
      serialNo: `2${order.value.order_number}${String(idx + 1).padStart(9, '0')}`
    })
  })
  
  return records
})

const fetchOrder = async () => {
  const id = route.params.orderId
  if (!id) return
  loading.value = true
  try {
    const res = await getOrderDetail(id)
    if (res.code === 200) {
      order.value = res.data
      console.log('Order data:', order.value)
    }
  } catch (e) {
    console.error('获取订单详情失败:', e)
    message.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (time) => {
  return time ? dayjs(time).format('YYYY-MM-DD') : '-'
}

const formatTime = (time) => {
  return time ? dayjs(time).format('HH:mm') : ''
}

const formatDateTime = (time) => {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm:ss') : '-'
}

const formatDateWithWeekday = (time) => {
  if (!time) return ''
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const d = dayjs(time)
  return `${d.format('YYYY-MM-DD')}/${weekdays[d.day()]}`
}

const getWeekday = (time) => {
  if (!time) return ''
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdays[dayjs(time).day()]
}

const maskIdNumber = (idNumber) => {
  if (!idNumber) return ''
  if (idNumber.length > 10) {
    return idNumber.substring(0, 4) + '***********' + idNumber.substring(idNumber.length - 3)
  }
  return idNumber
}

onMounted(() => {
  fetchOrder()
})
</script>

<style scoped>
.order-detail-page {
  font-family: "Microsoft YaHei", "SimSun", sans-serif;
  background: #f5f5f5;
  min-height: 100vh;
}

.wrapper.content {
  width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
  min-height: 600px;
}

/* 面包屑 */
.breadcrumb {
  margin-bottom: 15px;
  font-size: 12px;
  color: #666;
}
.breadcrumb a {
  color: #3b99fc;
  text-decoration: none;
}
.breadcrumb a:hover {
  text-decoration: underline;
}
.breadcrumb .sep {
  margin: 0 5px;
  color: #999;
}
.breadcrumb .active {
  color: #ff8200;
}

/* Tab样式 - 精确模仿12306 */
.panel-tab {
  background: #fff;
}

.tab-hd {
  border-bottom: 1px solid #dedede;
  background: #fff;
}

.tab-hd-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
}

.tab-hd-list li {
  cursor: pointer;
  position: relative;
}

.tab-hd-list li a {
  display: block;
  padding: 12px 25px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  background: #fff;
  border-right: 1px solid #dedede;
  position: relative;
}

.tab-hd-list li:first-child a {
  border-left: 1px solid #dedede;
}

.tab-hd-list li.active a {
  color: #3b99fc;
  background: #fff;
  border-bottom: 1px solid #fff;
  margin-bottom: -1px;
}

.tab-hd-list li:hover:not(.active) a {
  color: #3b99fc;
}

.tab-bd {
  padding: 20px;
  min-height: 600px;
  border: 1px solid #dedede;
  border-top: none;
}

.tab-item {
  display: block;
}

/* 订单跟踪样式 - 精确模仿12306 */
.order-tracking {
  border: 1px solid #3b99fc;
  display: flex;
  min-height: 242px;
  position: relative;
}

.order-tracking-hd {
  width: 296px;
  min-height: 240px;
  color: #fff;
  background: #3b99fc;
  flex-shrink: 0;
  position: relative;
}

/* 锯齿边缘效果 - 半圆形凹槽模仿撕开的票根 */
.ticket-edge {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 10px;
  background-image: radial-gradient(circle at 100% 50%, #fff 5px, transparent 5px);
  background-size: 10px 18px;
  background-position: 0 0;
  background-color: #3b99fc;
}

.tracking-hd-content {
  padding: 20px 25px 20px 30px;
}

.tracking-hd-tit {
  height: 60px;
  line-height: 60px;
  border-bottom: 1px solid rgba(255,255,255,0.35);
  font-size: 20px;
  font-weight: normal;
}

.tracking-hd-con {
  padding: 12px 0 0;
}

.tracking-hd-con .hd-label {
  color: #87b7f2;
  line-height: 24px;
}

.tracking-hd-con .hd-value {
  color: #fff;
  font-size: 14px;
  line-height: 28px;
}

/* 订单跟踪时间线 */
.order-tracking-bd {
  flex: 1;
  max-height: 400px;
  overflow: auto;
  padding: 10px 36px;
}

.no-tracking {
  padding: 80px 0;
  text-align: center;
  color: #999;
}

.tracking-status {
  border-left: 1px solid #dbdbdb;
  position: relative;
  list-style: none;
  margin: 0;
  padding: 0;
}

.tracking-status:before {
  content: "";
  position: absolute;
  top: 0;
  left: -1px;
  width: 1px;
  height: 9px;
  background: #fff;
  z-index: 2;
}

.tracking-status:after {
  content: "";
  position: absolute;
  bottom: 0;
  left: -1px;
  width: 1px;
  height: 9px;
  background: #fff;
  z-index: 2;
}

.tracking-status .status-item {
  line-height: 34px;
  position: relative;
  padding-left: 150px;
  min-height: 70px;
}

.tracking-status .s-date {
  position: absolute;
  top: 0;
  left: 20px;
  font-size: 12px;
  color: #666;
  line-height: 34px;
}

.tracking-status .s-dot {
  position: absolute;
  top: 9px;
  left: -9px;
  width: 17px;
  height: 17px;
  border: 6px solid #fff;
  background: #dbdbdb;
  border-radius: 50%;
}

.tracking-status .status-item-newdate .s-dot {
  border-width: 5px;
}

.tracking-status .status-item-today .s-dot {
  background: #ff8000;
}

.tracking-status .status-txt {
  height: 34px;
  line-height: 34px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #333;
}

.tracking-status .status-txt.txt-second {
  color: #ff8000;
  font-size: 13px;
  height: 28px;
  line-height: 28px;
}

/* 温馨提示 */
.tips-box {
  border: 1px solid #ffce9d;
  background: #fffbf5;
  padding: 15px 20px;
  margin-top: 20px;
}

.tips-box .tips-tit {
  font-weight: bold;
  color: #333;
  margin: 0 0 10px;
  font-size: 14px;
}

.tips-box p {
  font-size: 12px;
  color: #666;
  line-height: 24px;
  margin: 0;
}

.mt-lg {
  margin-top: 20px;
}

/* 退款详情表格 */
.order-panel-refund .order-item {
  border: 1px solid #acd1f9;
  margin-top: 20px;
}

.order-panel-refund .order-item.mt0 {
  margin-top: 0;
}

.order-item-table {
  width: 100%;
  text-align: center;
  border-collapse: collapse;
}

.order-item-table th {
  background: #f0f8ff;
  height: 40px;
  padding: 0 10px;
  border-bottom: 1px solid #dedede;
  font-weight: normal;
  color: #333;
}

.order-item-table td {
  padding: 15px 10px;
  border-top: 1px solid #dedede;
  border-right: 1px solid #dedede;
  line-height: 22px;
  vertical-align: middle;
}

.order-item-table .td-left {
  padding-left: 20px;
  text-align: left;
}

.order-item-table .br-none {
  border-right: none;
}

.order-item-table .col-info {
  width: 25%;
}

.order-item-table .col-result {
  width: 20%;
}

.order-item-table .col-num {
  width: 25%;
}

.txt-light {
  color: #666;
  line-height: 28px;
}

.txt-price {
  color: #ff8200;
}

.txt-mlg {
  font-size: 18px;
  font-weight: bold;
}

.txt-primary {
  color: #3b99fc;
}

.txt-success {
  color: #52c41a;
}

/* 空状态 */
.order-empty-inline {
  padding: 80px 0;
  text-align: center;
}

.order-empty-inline .empty-pic img {
  width: 87px;
  height: 70px;
  margin-bottom: 20px;
}

.order-empty-inline .empty-txt {
  color: #999;
}

.order-empty-inline .empty-tit {
  font-size: 14px;
  margin: 0;
}

.order-empty-full {
  padding: 100px 0;
  text-align: center;
  background: #fff;
  border: 1px solid #dedede;
}

.order-empty-full .empty-pic img {
  width: 87px;
  height: 70px;
  margin-bottom: 20px;
}

.order-empty-full .empty-txt {
  color: #999;
}

.order-empty-full .empty-txt a {
  color: #3b99fc;
}

/* 免费乘车儿童样式 */
.txt_top_yellow {
  background: #fff9e6;
  border: 1px solid #ffe58f;
  padding: 12px 15px;
  color: #d46b08;
  font-size: 12px;
  margin-bottom: 20px;
  line-height: 22px;
}

.blue_border_box {
  border: 1px solid #acd1f9;
}

.blue_bg_box {
  background: #f0f8ff;
  padding: 12px 20px;
  font-weight: bold;
  color: #333;
}

.blue_bg_box.header-row {
  font-weight: normal;
}

.blue_bg_box p {
  margin: 0;
}

.blue_bg_box .th_box {
  display: inline-block;
  width: 270px;
  text-align: center;
}

.train_box {
  padding: 15px 20px;
  border-bottom: 1px solid #e8e8e8;
}

.train_box p {
  margin: 0;
  line-height: 28px;
}

.txt_train {
  font-size: 16px;
  font-weight: bold;
}

.txt_train span {
  margin: 0 10px;
  color: #999;
}

.table_box table {
  border-color: #e8e8e8;
}

.table_box .tr_box td {
  padding: 15px 10px;
  border-bottom: 1px solid #e8e8e8;
  font-size: 13px;
}

.table_box .td_box_1 {
  color: #999;
  text-align: center;
}

.tips_box {
  border: 1px solid #ffce9d;
  background: #fffbf5;
  padding: 15px 20px;
  margin-top: 20px;
}

.tips_box .tips_tit {
  font-weight: bold;
  color: #333;
  margin: 0 0 10px;
  font-size: 14px;
}

.tips_box p {
  font-size: 12px;
  color: #666;
  line-height: 24px;
  margin: 0;
}
</style>