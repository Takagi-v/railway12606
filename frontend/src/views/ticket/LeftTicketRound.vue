<template>
  <div class="leftticket-page">
    <Header12306 />
    <div class="wrapper">
      <!-- 搜索框 -->
      <div class="sear-box quick-sear-box sear-box-lg">
        <form id="queryLeftForm" method="get" enctype="application/x-www-form-urlencoded">
          <div class="dfc" id="dfc">
            <ul>
              <li>
                <input name="singleRoundType" type="radio" id="dc" class="radio" value="dc" @change="handleTypeChange('dc')" />
                <label for="dc" id="dc_label" class="cursor">单程</label>
              </li>
              <li>
                <input name="singleRoundType" type="radio" id="wf" class="radio" value="wc" checked="checked" @change="handleTypeChange('wf')" />
                <label for="wf" id="wf_label" class="cursor">往返</label>
              </li>
            </ul>
          </div>
          <div class="s-info" id="place_area">
            <ul>
              <li>
                <span class="label"><label id="fromStationText_label">出发地</label></span>
                <div class="inp-w">
                  <input id="fromStation" type="hidden" name="leftTicketDTO.from_station" />
                  <input autocomplete="off" type="text" id="fromStationText" class="inp-txt" v-model="from" name="leftTicketDTO.from_station_name" placeholder="简拼/全拼/汉字" />
                </div>
              </li>
              <li class="i-change i-change2" id="change_station" style="background-position: -67px -96px; cursor: pointer;" @click="swap">
                <a href="javascript:" title="将出发地与目的地互换" style="width:1px;height:1px;position:absolute;display:block;"></a>
              </li>
              <li>
                <span class="label"><label id="toStationText_label"> 目的地</label></span>
                <div class="inp-w">
                  <input id="toStation" type="hidden" name="leftTicketDTO.to_station" />
                  <input autocomplete="off" type="text" id="toStationText" class="inp-txt" v-model="to" name="leftTicketDTO.to_station_name" placeholder="简拼/全拼/汉字" />
                </div>
              </li>
              <li>
                <span class="label"> 出发日</span>
                <div class="inp-w" style="z-index:1200">
                  <input autocomplete="off" type="text" class="inp_selected" name="leftTicketDTO.train_date" id="train_date" :value="goDateDisplay" />
                  <span id="date_icon_1" class="i-date"></span>
                </div>
              </li>
              <li class="">
                <span class="label"> 返程日</span>
                <div class="inp-w" id="back_div" style="z-index:1100">
                  <input autocomplete="off" type="text" class="inp_selected" name="back_train_date" id="back_train_date" :value="backDateDisplay" />
                  <span id="date_icon_2" class="i-date"></span>
                </div>
              </li>
            </ul>
          </div>
          <div class="quick-s">
            <div class="quick-s-inner">
              <ul>
                <li>
                  <input type="radio" id="sf1" class="radio" name="sf" checked="checked" />
                  <label id="sf1_label" for="sf1" class="cursor">普通</label>
                </li>
                <li>
                  <input type="radio" id="sf2" class="radio" name="sf" />
                  <label id="sf2_label" for="sf2" class="cursor">学生</label>
                </li>
              </ul>
              <div class="btn-area quick-s-btn"><a style="margin-top: 12px;" href="javascript:" id="query_ticket" class="btn92s" shape="rect" @click.prevent="search">查询</a></div>
            </div>
          </div>
        </form>
      </div>
      
      <!-- 日期选择与筛选 -->
      <div class="sear-sel sear-sel-lg" id="sear-sel">
        <div id="date_range" class="sear-sel-hd clearfix">
          <ul>
            <li v-for="(d,i) in dateTabs" :key="d.key" :class="{ sel: i===activeDate, end: i===dateTabs.length-1 }" :alt="'show'">
              <span :class="i===activeDate ? 'first hide' : ''" style="cursor: pointer;" @click="selectDate(i)">
                <a href="javascript:" :title="d.title" style="width:1px;height:1px;position:absolute;display:block;"></a>{{ d.short }}
              </span>
              <span :class="i===activeDate ? 'first' : 'hide'" @click="selectDate(i)">
                <a href="javascript:" :title="d.title" style="width:1px;height:1px;position:absolute;display:block;"></a>{{ d.full }}
              </span>
            </li>
          </ul>
          <div class="clear"></div>
        </div>
        <div class="sear-sel-bd quick-buy-sel" :class="{ 'quick-buy-open': filtersExpanded }" id="sear-sel-bd" :style="{ height: filtersExpanded ? 'auto' : '60px' }">
          <div class="pos-top" style="margin-right:20px;">发车时间：
            <select class="select-small" id="cc_start_time" v-model="filterTime" aria-label="请选择发车时间,按上下键进行选择">
              <option value="00002400">00:00--24:00</option>
              <option value="00000600">00:00--06:00</option>
              <option value="06001200">06:00--12:00</option>
              <option value="12001800">12:00--18:00</option>
              <option value="18002400">18:00--24:00</option>
            </select>
          </div>
          <div class="section clearfix">
            <div class="section-hd">车次类型：</div>
            <div class="section-bd" id="cc_train_type_btn_all">
              <span class="btn-all" id="train_type_btn_all" style="cursor: pointer;" @click="toggleAllTypes">全部</span>
              <ul id="_ul_station_train_code">
                <li v-for="t in typeDefs" :key="t.value">
                  <input name="cc_type" :value="t.value" type="checkbox" class="check" :id="t.id" v-model="selectedTypes" :aria-label="t.aria">
                  <label :for="t.id" style="cursor: pointer;">{{ t.label }}</label>
                </li>
              </ul>
            </div>
          </div>
          <div class="section clearfix">
            <div class="section-hd">出发车站：</div>
            <div class="section-bd" id="cc_from_station_name_all">
              <span class="btn-all" id="from_station_name_all" style="cursor: pointer;">全部</span>
              <ul id="from_station_ul">
                <li v-for="s in fromStations" :key="s.value">
                  <input type="checkbox" class="check" name="cc_from_station" :value="s.value" :id="'cc_from_station_'+s.value+'_check'">
                  <label :title="s.value" class="cursor" :for="'cc_from_station_'+s.value+'_check'" :id="'cc_from_station_'+s.value">{{ s.value }}</label>
                </li>
              </ul>
            </div>
          </div>
          <div class="section clearfix">
            <div class="section-hd">到达车站：</div>
            <div class="section-bd" id="cc_to_station_name_all">
              <span class="btn-all" id="to_station_name_all" style="cursor: pointer;">全部</span>
              <ul id="to_station_ul">
                <li v-for="s in toStations" :key="s.value">
                  <input type="checkbox" class="check" name="cc_to_station" :value="s.value" :id="'cc_to_station_'+s.value+'_check'">
                  <label :title="s.value" class="cursor" :for="'cc_to_station_'+s.value+'_check'" :id="'cc_to_station_'+s.value">{{ s.value }}</label>
                </li>
              </ul>
            </div>
          </div>
          <div class="section clearfix">
            <div class="section-hd">车次席别：</div>
            <div class="section-bd" id="cc_seat_type_new_all">
              <span class="btn-all" id="to_seat_type_new_all">全部</span>
              <ul id="seat_type_new_ul">
                <li v-for="st in seatTypeDefs" :key="st.value">
                  <input type="checkbox" class="check" :value="st.value" name="cc_seat_type" :id="'cc_seat_type_'+st.value+'_check'">
                  <label class="cursor" :for="'cc_seat_type_'+st.value+'_check'" :id="'cc_seat_type_'+st.value">{{ st.label }}</label>
                </li>
              </ul>
            </div>
          </div>
          <div style="display: none;" class="section pt2 clearfix">
            <div class="section-hd" id="memb">乘车人：</div>
            <div class="section-bd pt2" id="setion_postion" style="width:688px;">
              <span class="wrap-left"><a href="javascript:" class="btn-small" shape="rect" aria-label="请选择乘车人">请选择</a></span>
            </div>
            <span style="color:red;width:auto;">您可点击“成人乘车人”添加儿童票。</span>
          </div>
          <div style="display: none;" class="section clearfix">
            <div class="section-hd" id="train_first">优先车次：</div>
            <div class="section-bd pt2" id="prior_train">
              <span style="display: none;" name="prior_train-span" class="wrap-left add-cc">
                <input type="text" maxlength="5" class="inp-small" id="inp-train" style="text-transform:uppercase" value="  请输入">
                <a href="javascript:" class="btn-add" id="add-train" shape="rect"></a>
              </span>
            </div>
          </div>
          <div style="display: none;" class="section clearfix">
            <div class="section-hd" id="seat_first">优先席别：</div>
            <div class="section-bd pt2" id="prior_seat">
              <span class="wrap-left"><a href="javascript:" class="btn-small" shape="rect" aria-label="请选择优先席别">请选择</a></span>
            </div>
          </div>
          <div style="display: none;" class="section pt2 clearfix">
            <div class="section-hd" id="select_date">备选日期：</div>
            <div class="section-bd pt2" id="prior_date">
              <span class="wrap-left"><a href="javascript:" class="btn-small" id="train_date" shape="rect" aria-label="请选择备选日期">请选择</a></span>
            </div>
          </div>
          <div style="display: none;" class="section pt2 clearfix">
            <div class="section-hd" id="ad_setting">高级设置：</div>
            <div class="section-bd pt2">
              <span class="mr17">
                <select id="_prior" class="select-small" style="width:75px;margin-right:10px" aria-label="请选择优先席别">
                  <option value="1">席别优先</option>
                  <option value="2">车次优先</option>
                </select>
              </span>
              <span class="mr17">
                <input type="checkbox" class="check" id="autoSubmit" aria-label="勾选本选项并点击查询后，网站将自动查询符合设定条件的车票信息，如有符合条件的车次，将自动提交订单信息。,按空格键进行操作">
                <label for="autoSubmit" id="autoSubmitTxt" style="cursor: pointer; color: rgb(51, 51, 51);">自动提交</label>
              </span>
              <span class="mr17">
                <input type="checkbox" class="check" id="partSubmit" aria-label="如果网站查询同一车次只有部分符合您设定条件的车票时，将按您设定的乘车人和席别优先顺序进行提交。,按空格键进行操作">
                <label for="partSubmit" id="partSubmitTxt" style="cursor: pointer; color: rgb(51, 51, 51);">余票不足时部分提交</label>
              </span>
              <a href="javascript:" class="btn-small mr5" id="tryPlayer" shape="rect">试听提示音乐</a>
              <a href="javascript:" id="clearAll" class="btn-small" shape="rect">清空所有选项</a>
            </div>
          </div>
        </div>
        <div class="quick-gif">
          <a href="javascript:" id="show_more" :class="filtersExpanded ? 'up' : 'down'" shape="rect" style="cursor: pointer;" @click="toggleFilters">筛选</a>
        </div>
      </div>

      <!-- 结果列表 -->
      <div class="t-list" id="t-list">
        <div class="t-list-bd">
          <table>
            <colgroup>
              <col width="90"><col width="100"><col width="82"><col width="82">
              <col width="66"><col width="66"><col width="66"><col width="66">
              <col width="66"><col width="66"><col width="66"><col width="66">
              <col width="66"><col width="66"><col width="66">
              <col width="118">
            </colgroup>
            <thead><tr class="th" id="float"><th width="90" colspan="1" rowspan="1">车次</th>
<th width="100" colspan="1" rowspan="1">出发站<br clear="none">
到达站</th>
<th width="82" colspan="1" rowspan="1" id="startendtime"><span class="b1" id="s_time" style="cursor: pointer;"><a href="javascript:" title="按出发时间排序" style="width:1px;height:1px;position:absolute;display:block;"></a>出发时间</span><br><span class="b4" id="r_time" style="cursor: pointer;"><a href="javascript:" title="按到达时间排序" style="width:1px;height:1px;position:absolute;display:block;"></a>到达时间</span></th>
<th width="82" colspan="1" rowspan="1"><span class="b1" id="l_s" style="cursor: pointer;">历时</span>
</th>
<th width="66" colspan="1" rowspan="1">商务座<br clear="none">
特等座</th>
<th width="66" colspan="1" rowspan="1">优选<br clear="none">
一等座</th>
<th width="66" colspan="1" rowspan="1">一等座</th>
<th width="66" colspan="1" rowspan="1">二等座<br clear="none">
二等包座</th>
<th width="66" colspan="1" rowspan="1">高级<br clear="none">
软卧</th>
<th width="66" colspan="1" rowspan="1">软卧/动卧<br clear="none">
一等卧</th>
<th width="66" colspan="1" rowspan="1">硬卧<br clear="none">
二等卧</th>
<th width="66" colspan="1" rowspan="1">软座</th>
<th width="66" colspan="1" rowspan="1">硬座</th>
<th width="66" colspan="1" rowspan="1">无座</th>
<th width="66" colspan="1" rowspan="1">其他</th>
<th colspan="1" rowspan="1">备注</th>
</tr>
</thead>
            <tbody>
              <template v-if="trains.length === 0">
                <tr class="no-ticket">
                  <td colspan="16" style="text-align: center; padding: 20px;">
                    <p style="font-size: 16px; color: #999;">{{ loading ? '加载中...' : '暂无车次信息' }}</p>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr v-for="(train, index) in trains" :key="train.train_no" :class="{ 'bgc': index % 2 === 0 }" :id="'ticket_' + train.train_no">
                  <td colspan="4" width="370">
                    <div class="ticket-info clearfix" :id="'train_num_' + index">
                      <div class="train" :id="'ticket_' + train.train_no + '_train'">
                        <div>
                          <a title="点击查看停靠站信息" style="height: 18px; line-height: 18px;" href="javascript:" class="number" @click="showStopStation(train)">{{ train.station_train_code }}</a>
                          <div class="train-type" v-if="train.train_type_features">
                            <div class="train-type-item item-zhi" title="智能动车组" v-if="train.train_type_features.includes('智')">智</div>
                            <div class="train-type-item item-fu" title="复兴号" v-if="train.train_type_features.includes('复')">复</div>
                            <div class="train-type-item item-jing" title="静音车厢" v-if="train.train_type_features.includes('静')">静</div>
                          </div>
                        </div>
                        <span class="lookup" @click="showTicketPrice(train)"><span style="display:none;">查看票价</span><b title="查看票价" tabindex="0" aria-label="查看票价,按回车键操作"></b></span>
                      </div>
                      <div class="cdz">
                        <strong :title="train.from_station_name" class="start-s">{{ train.from_station_name }}</strong>
                        <strong :title="train.to_station_name" class="end-s">{{ train.to_station_name }}</strong>
                      </div>
                      <div class="cds">
                        <strong class="start-t">{{ train.start_time }}</strong>
                        <strong class="color999">{{ train.arrive_time }}</strong>
                      </div>
                      <div class="ls">
                        <strong>{{ train.lishi }}</strong>
                        <span>{{ train.day_difference === '0' ? '当日到达' : '次日到达' }}</span>
                      </div>
                    </div>
                  </td>
                  <!-- 商务座/特等座 -->
                  <td width="46" align="center" :style="{ cursor: 'pointer', color: train.swz_num === '候补' ? '#f80' : '' }" @click="showTicketPrice(train)">
                    {{ train.swz_num || '--' }}
                  </td>
                  <!-- 优选一等座 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.yxdz_num || '--' }}
                  </td>
                  <!-- 一等座 -->
                  <td width="46" align="center" :style="{ cursor: 'pointer', color: train.ydz_num === '候补' ? '#f80' : '' }" @click="showTicketPrice(train)">
                    {{ train.ydz_num || '--' }}
                  </td>
                  <!-- 二等座/二等包座 -->
                  <td width="46" align="center" :style="{ cursor: 'pointer', color: train.edz_num === '候补' ? 'grey' : '' }" @click="showTicketPrice(train)">
                     {{ train.edz_num || '--' }}
                     <i v-if="train.edz_num === '候补'" class="icon icon-add-fill ml5" style="vertical-align: middle; font-size: 14px;"></i>
                  </td>
                  <!-- 高级软卧 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.gjrw_num || '--' }}
                  </td>
                  <!-- 软卧/一等卧 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.rw_num || '--' }}
                  </td>
                  <!-- 硬卧/二等卧 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.yw_num || '--' }}
                  </td>
                  <!-- 软座 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.rz_num || '--' }}
                  </td>
                  <!-- 硬座 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.yz_num || '--' }}
                  </td>
                  <!-- 无座 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.wz_num || '--' }}
                  </td>
                  <!-- 其他 -->
                  <td width="46" align="center" style="cursor: pointer;" @click="showTicketPrice(train)">
                    {{ train.qt_num || '--' }}
                  </td>
                  <!-- 预订按钮 (备注栏) -->
                  <td align="center" width="80" class="no-br">
                    <a href="javascript:" class="btn72" style="cursor: pointer;" @click="showTicketPrice(train)">预订<i class="ico-dh"></i></a>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>

    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import dayjs from 'dayjs'
import { message } from 'ant-design-vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { useRouter, useRoute } from 'vue-router'
import { searchTrains } from '@/api/train'

const router = useRouter()
const route = useRoute()

const showTicketPrice = (train) => {
  console.log('Show price for', train.station_train_code)
}
const showStopStation = (train) => {
  console.log('Show stops for', train.station_train_code)
}

const from = ref('北京')
const to = ref('上海')
const goDate = ref(new Date())
const backDate = ref(dayjs().add(1, 'day').toDate())
const weekday = ['周日','周一','周二','周三','周四','周五','周六']
const fmt = (d) => {
  const y = d.getFullYear()
  const m = String(d.getMonth()+1).padStart(2,'0')
  const dd = String(d.getDate()).padStart(2,'0')
  return `${y}-${m}-${dd} ${weekday[d.getDay()]}`
}
const goDateDisplay = computed(() => fmt(goDate.value))
const backDateDisplay = computed(() => fmt(backDate.value))

const dateTabs = computed(() => {
  const arr = []
  for(let i=0;i<15;i++){
    const d = new Date()
    d.setDate(d.getDate()+i)
    const m = String(d.getMonth()+1).padStart(2,'0')
    const dd = String(d.getDate()).padStart(2,'0')
    const short = `${m}-${dd}`
    const full = `${m}-${dd} ${weekday[d.getDay()]}`
    arr.push({ key: short, short, full, title: `按回车键搜索${full}全部车次`, dateObj: new Date(d) })
  }
  return arr
})
const activeDate = ref(0)
const filterTime = ref('00002400')
const filtersExpanded = ref(false)

const typeDefs = [
  { value: 'G', id: 'checkbox_fTDm4W85Mw', label: 'GC-高铁/城际', aria: '车次类型为：GC-高铁/城际,按空格键进行操作' },
  { value: 'D', id: 'checkbox_QsAk5fZKX1', label: 'D-动车', aria: '车次类型为：D-动车,按空格键进行操作' },
  { value: 'Z', id: 'checkbox_OhCkG7mqBy', label: 'Z-直达', aria: '车次类型为：Z-直达,按空格键进行操作' },
  { value: 'T', id: 'checkbox_o4cXrjU8yT', label: 'T-特快', aria: '车次类型为：T-特快,按空格键进行操作' },
  { value: 'K', id: 'checkbox_WgMnto5j1e', label: 'K-快速', aria: '车次类型为：K-快速,按空格键进行操作' },
  { value: 'QT', id: 'checkbox_vnG2WIAAMs', label: '其他', aria: '车次类型为：其他,按空格键进行操作' },
  { value: '复', id: 'checkbox_YtoHtQH5R6', label: '复兴号', aria: '车次类型为：复兴号,按空格键进行操作' },
  { value: '智', id: 'checkbox_Nxn2gxtUa6', label: '智能动车组', aria: '车次类型为：智能动车组,按空格键进行操作' },
]
const selectedTypes = ref([])
const toggleAllTypes = () => {
  if(selectedTypes.value.length === typeDefs.length){
    selectedTypes.value = []
  } else {
    selectedTypes.value = typeDefs.map(t=>t.value)
  }
}

const formatDateValue = (d) => dayjs(d).format('YYYY-MM-DD')
const normalizeTime = (value) => {
  const hour = value.slice(0, 2)
  if (hour === '24') {
    return '23:59'
  }
  return `${hour}:${value.slice(2,4)}`
}
const parseTimeRange = (range) => {
  if (!range || range.length !== 8) return [null, null]
  const start = normalizeTime(range.slice(0,4))
  const end = normalizeTime(range.slice(4,8))
  return [start, end]
}

const formatSeatDisplay = (seatInfo) => {
  if (!seatInfo) return '--'
  if (seatInfo.available <= 0) return '无'
  if (seatInfo.available <= 20) return String(seatInfo.available)
  return '有'
}

const trainTypeFeatureMap = {
  '高铁': ['复'],
  '动车': ['智'],
  '直达': []
}

const transformTrain = (train, direction) => {
  const seatMap = {
    swz_num: '--',
    yxdz_num: '--',
    ydz_num: formatSeatDisplay(train.first_class),
    edz_num: formatSeatDisplay(train.second_class),
    gjrw_num: '--',
    rw_num: formatSeatDisplay(train.soft_sleeper),
    yw_num: formatSeatDisplay(train.hard_sleeper),
    rz_num: '--',
    yz_num: '--',
    wz_num: '--',
    qt_num: '--'
  }
  const prefix = direction === 'go' ? '去程 ' : '返程 '
  return {
    train_no: `${direction}-${train.train_id}`,
    station_train_code: `${prefix}${train.train_number}`,
    from_station_name: train.departure_station,
    to_station_name: train.arrival_station,
    start_time: train.departure_time,
    arrive_time: train.arrival_time,
    lishi: train.duration,
    day_difference: String(train.arrival_day_offset ?? 0),
    train_type: train.train_type,
    train_type_features: trainTypeFeatureMap[train.train_type] || [],
    direction,
    ...seatMap
  }
}

const filterValueMap = {
  G: '高铁',
  复: '高铁',
  D: '动车',
  智: '动车',
  Z: '直达',
  T: '直达',
  K: '直达'
}

const goTrainsRaw = ref([])
const backTrainsRaw = ref([])
const goLoading = ref(false)
const backLoading = ref(false)
const loading = computed(() => goLoading.value || backLoading.value)

const rawTrains = computed(() => [...goTrainsRaw.value, ...backTrainsRaw.value])

const trains = computed(() => {
  let list = rawTrains.value
  const typeLabels = new Set()
  selectedTypes.value.forEach((val) => {
    const mapped = filterValueMap[val]
    if (mapped) {
      typeLabels.add(mapped)
    }
  })
  if (typeLabels.size > 0) {
    list = list.filter((item) => typeLabels.has(item.train_type))
  }
  return list
})

const collectStations = (list, key) => {
  if (!list.length) return null
  const set = new Set(list.map((item) => item[key]))
  return Array.from(set).map((value) => ({ value }))
}

const fromStations = computed(() => collectStations(trains.value, 'from_station_name') || [{ value: from.value }])
const toStations = computed(() => collectStations(trains.value, 'to_station_name') || [{ value: to.value }])

const seatTypeDefs = [
  { value: 'A', label: '高级动卧' },
  { value: 'O', label: '二等座' },
  { value: 'F', label: '动卧' },
  { value: '4', label: '软卧' },
  { value: '3', label: '硬卧' },
  { value: '1', label: '硬座' },
]

const seatTypes = [
  { key: 'swz_num', class: '' },
  { key: 'yxdz_num', class: '' },
  { key: 'ydz_num', class: '' },
  { key: 'edz_num', class: '' },
  { key: 'gjrw_num', class: '' },
  { key: 'rw_num', class: '' },
  { key: 'yw_num', class: '' },
  { key: 'rz_num', class: '' },
  { key: 'yz_num', class: '' },
  { key: 'wz_num', class: '' },
  { key: 'qt_num', class: '' },
]

const buildQueryParams = (direction) => {
  const isGo = direction === 'go'
  const params = {
    departure_city: isGo ? from.value.trim() : to.value.trim(),
    arrival_city: isGo ? to.value.trim() : from.value.trim(),
    travel_date: formatDateValue(isGo ? goDate.value : backDate.value),
  }
  const [minTime, maxTime] = parseTimeRange(filterTime.value)
  if (minTime) params.min_departure_time = minTime
  if (maxTime) params.max_departure_time = maxTime
  return params
}

const fetchGoTrains = async () => {
  if (!from.value.trim() || !to.value.trim()) return
  goLoading.value = true
  try {
    const resp = await searchTrains(buildQueryParams('go'))
    const rows = Array.isArray(resp?.data) ? resp.data : []
    goTrainsRaw.value = rows.map((item) => transformTrain(item, 'go'))
  } catch (error) {
    message.error('查询去程失败，请稍后重试')
  } finally {
    goLoading.value = false
  }
}

const fetchBackTrains = async () => {
  if (!from.value.trim() || !to.value.trim()) return
  backLoading.value = true
  try {
    const resp = await searchTrains(buildQueryParams('back'))
    const rows = Array.isArray(resp?.data) ? resp.data : []
    backTrainsRaw.value = rows.map((item) => transformTrain(item, 'back'))
  } catch (error) {
    message.error('查询返程失败，请稍后重试')
  } finally {
    backLoading.value = false
  }
}

const ensureBackDateValid = () => {
  if (dayjs(backDate.value).isBefore(dayjs(goDate.value))) {
    backDate.value = dayjs(goDate.value).add(1, 'day').toDate()
  }
}

const updateActiveDateByGoDate = () => {
  const diff = dayjs(goDate.value).startOf('day').diff(dayjs().startOf('day'), 'day')
  if (diff >= 0 && diff < dateTabs.value.length) {
    activeDate.value = diff
  }
}

const search = async () => {
  if (!from.value.trim() || !to.value.trim()) {
    message.warning('请输入出发地和目的地')
    return
  }
  ensureBackDateValid()
  await Promise.all([fetchGoTrains(), fetchBackTrains()])
}

const selectDate = (i) => {
  activeDate.value = i
  const d = dateTabs.value[i].dateObj
  goDate.value = new Date(d)
  ensureBackDateValid()
  search()
}

const swap = () => {
  const a = from.value
  from.value = to.value
  to.value = a
  search()
}

const handleTypeChange = (type) => {
  if (type === 'dc') {
    router.push('/leftTicket/single')
  } else {
    router.push('/leftTicket/round')
  }
}

const toggleFilters = () => {
  filtersExpanded.value = !filtersExpanded.value
}

const pickQueryValue = (value) => (Array.isArray(value) ? value[0] : value)

const syncFromRoute = () => {
  let changed = false
  const routeFrom = pickQueryValue(route.query.departure_city)
  const routeTo = pickQueryValue(route.query.arrival_city)
  const routeGo = pickQueryValue(route.query.travel_date)
  const routeBack = pickQueryValue(route.query.return_date)

  if (routeFrom && routeFrom !== from.value) {
    from.value = routeFrom
    changed = true
  }
  if (routeTo && routeTo !== to.value) {
    to.value = routeTo
    changed = true
  }
  if (routeGo && dayjs(routeGo, 'YYYY-MM-DD', true).isValid()) {
    const parsed = dayjs(routeGo).toDate()
    if (parsed.toDateString() !== goDate.value.toDateString()) {
      goDate.value = parsed
      changed = true
    }
  }
  if (routeBack && dayjs(routeBack, 'YYYY-MM-DD', true).isValid()) {
    const parsedBack = dayjs(routeBack).toDate()
    if (parsedBack.toDateString() !== backDate.value.toDateString()) {
      backDate.value = parsedBack
      changed = true
    }
  }
  if (changed) {
    ensureBackDateValid()
    updateActiveDateByGoDate()
  }
  return changed
}

watch(filterTime, () => {
  if (rawTrains.value.length) {
    search()
  }
})

watch(
  () => route.query,
  () => {
    const changed = syncFromRoute()
    if (changed) {
      search()
    }
  }
)

onMounted(() => {
  syncFromRoute()
  updateActiveDateByGoDate()
  search()
})
</script>

<style>
@import url('@/assets/12306-leftticket/leftTicket.css');
.btn72 {
  display: inline-block;
  height: 30px;
  line-height: 30px;
  width: 72px;
  background-position: 0 -250px;
  color: #fff !important;
  text-decoration: none;
  text-align: center;
}
.btn72:hover {
  color: #fff !important;
  text-decoration: none;
}
.leftticket-page .wrapper{width:1200px;margin:0 auto}
.quick-s-inner{display:flex;align-items:center;justify-content:space-between}
.quick-s-inner ul{flex:1}
.quick-s-btn{margin-left:20px}
</style>