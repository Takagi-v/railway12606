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
                <input name="singleRoundType" type="radio" id="dc" class="radio" value="dc" checked="checked" @change="handleTypeChange('dc')" />
                <label for="dc" id="dc_label" class="cursor">单程</label>
              </li>
              <li>
                <input name="singleRoundType" type="radio" id="wf" class="radio" value="wc" @change="handleTypeChange('wf')" />
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
                  <input autocomplete="off" type="text" class="inp_selected" name="back_train_date" id="back_train_date" disabled :value="backDateDisplay" style="color:#999" />
                  <span id="date_icon_2" class="i-date"></span>
                </div>
              </li>
            </ul>
          </div>
          <div class="quick-s">
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
            <div class="btn-area"><a style="margin-top: 12px;" href="javascript:" id="query_ticket" class="btn92s" shape="rect" @click.prevent="search">查询</a></div>
          </div>
        </form>
      </div>
      
      <!-- 日期选择与筛选 -->
      <div class="sear-sel sear-sel-lg" id="sear-sel">
        <div id="date_range" class="sear-sel-hd clearfix">
          <ul>
            <li v-for="(d,i) in dateTabs" :key="d.key" :class="{ sel: i===activeDate }" :alt="'show'">
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
        <div class="sear-sel-bd quick-buy-sel quick-buy-open" id="sear-sel-bd" :style="{ height: filtersExpanded ? 'auto' : '60px', overflow: 'hidden' }">
          <div class="pos-top" style="margin-right:20px;">发车时间：
            <select class="select-small" id="cc_start_time" v-model="filterTime">
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
                  <input name="cc_type" :value="t.value" type="checkbox" class="check" :id="t.id" v-model="selectedTypes">
                  <label :for="t.id" style="cursor: pointer;">{{ t.label }}</label>
                </li>
              </ul>
            </div>
          </div>
          <!-- 扩展筛选：出发车站 -->
          <div class="section clearfix" v-if="filtersExpanded">
            <div class="section-hd">出发车站：</div>
            <div class="section-bd">
              <span class="btn-all" style="cursor: pointer;">全部</span>
              <ul>
                <li><input type="checkbox" class="check" id="start_all"><label for="start_all">全部</label></li>
              </ul>
            </div>
          </div>
          <!-- 扩展筛选：到达车站 -->
          <div class="section clearfix" v-if="filtersExpanded">
            <div class="section-hd">到达车站：</div>
            <div class="section-bd">
              <span class="btn-all" style="cursor: pointer;">全部</span>
              <ul>
                <li><input type="checkbox" class="check" id="end_all"><label for="end_all">全部</label></li>
              </ul>
            </div>
          </div>
          <!-- 扩展筛选：车次席别 -->
          <div class="section clearfix" v-if="filtersExpanded">
            <div class="section-hd">车次席别：</div>
            <div class="section-bd">
              <span class="btn-all" style="cursor: pointer;">全部</span>
              <ul>
                <li><input type="checkbox" class="check" id="seat_all"><label for="seat_all">全部</label></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="quick-gif" style="top:10px;"><a href="javascript:" id="show_more" class="up" style="cursor: pointer;" @click="toggleFilters">筛选</a></div>
      </div>

      <!-- 结果列表 -->
      <div class="t-list" id="t-list">
        <div class="t-list-bd">
          <table>
            <colgroup>
              <col width="90"><col width="100"><col width="90"><col width="48">
              <col width="45"><col width="45"><col width="45"><col width="45">
              <col width="45"><col width="45"><col width="45"><col width="45">
              <col width="45"><col width="45"><col width="45"><col width="45">
              <col width="auto">
            </colgroup>
            <tbody>
              <tr class="th" id="float">
                <th width="90" colspan="1" rowspan="1">车次</th>
                <th width="100" colspan="1" rowspan="1">出发站<br clear="none">到达站</th>
                <th width="82" colspan="1" rowspan="1" id="startEndTime">出发时间<br clear="none">到达时间</th>
                <th width="48" colspan="1" rowspan="1">历时</th>
                <th width="37" colspan="1" rowspan="1">商务座<br clear="none">特等座</th>
                <th width="37" colspan="1" rowspan="1">优选<br clear="none">一等座</th>
                <th width="37" colspan="1" rowspan="1">一等座</th>
                <th width="37" colspan="1" rowspan="1">二等座<br clear="none">二等包座</th>
                <th width="37" colspan="1" rowspan="1">高级<br clear="none">软卧</th>
                <th width="37" colspan="1" rowspan="1">软卧<br clear="none">一等卧</th>
                <th width="37" colspan="1" rowspan="1">动卧</th>
                <th width="37" colspan="1" rowspan="1">硬卧<br clear="none">二等卧</th>
                <th width="37" colspan="1" rowspan="1">软座</th>
                <th width="37" colspan="1" rowspan="1">硬座</th>
                <th width="37" colspan="1" rowspan="1">无座</th>
                <th width="37" colspan="1" rowspan="1">其他</th>
                <th class="last" colspan="1" rowspan="1">备注</th>
              </tr>
              <template v-if="trains.length === 0">
                <tr class="no-ticket">
                  <td colspan="17" style="text-align: center; padding: 20px;">
                    <p style="font-size: 16px; color: #999;">{{ loading ? '加载中...' : '暂无车次信息' }}</p>
                  </td>
                </tr>
              </template>
              <template v-else>
                <tr :class="index % 2 === 0 ? 'bgc' : ''" v-for="(train, index) in trains" :key="train.train_no">
                  <td class="no-br">
                    <div class="train" :id="'train_num_'+index">
                      <div><a href="javascript:" class="number" style="text-decoration:underline;cursor:pointer;color:#333;">{{ train.station_train_code }}</a></div>
                    </div>
                  </td>
                  <td class="cdz">
                    <div class="cdz_name">
                      <strong class="start-s">{{ train.from_station_name }}</strong>
                      <strong class="end-s">{{ train.to_station_name }}</strong>
                    </div>
                  </td>
                  <td class="cds">
                    <div class="cds_name">
                      <strong class="start-t">{{ train.start_time }}</strong>
                      <strong class="color999">{{ train.arrive_time }}</strong>
                    </div>
                  </td>
                  <td class="ls">
                    <div class="ls_name">
                      <strong>{{ train.lishi }}</strong>
                      <span>{{ train.day_difference === '0' ? '当日到达' : '次日到达' }}</span>
                    </div>
                  </td>
                  <!-- 座位信息 -->
                  <td v-for="seat in seatTypes" :key="seat.key" :class="seat.class" style="text-align: center;">
                    {{ train[seat.key] || '--' }}
                  </td>
                  <td align="center" width="80" class="last">
                    <a href="javascript:" class="btn72" style="color:#fff;background:#ff8201;padding:2px 10px;border-radius:4px;">预订</a>
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
import { ref, computed, onMounted } from 'vue'
import Header12306 from '@/components/Header12306.vue'
import Footer from '@/components/LoginFooter.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const from = ref('北京')
const to = ref('上海')
const goDate = ref(new Date())
const backDate = ref(new Date())
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
  { value: 'G', id: 'type_G', label: 'GC-高铁/城际', aria: '车次类型为：GC-高铁/城际,按空格键进行操作' },
  { value: 'D', id: 'type_D', label: 'D-动车', aria: '车次类型为：D-动车,按空格键进行操作' },
  { value: 'Z', id: 'type_Z', label: 'Z-直达', aria: '车次类型为：Z-直达,按空格键进行操作' },
  { value: 'T', id: 'type_T', label: 'T-特快', aria: '车次类型为：T-特快,按空格键进行操作' },
  { value: 'K', id: 'type_K', label: 'K-快速', aria: '车次类型为：K-快速,按空格键进行操作' },
  { value: 'QT', id: 'type_QT', label: '其他', aria: '车次类型为：其他,按空格键进行操作' },
]
const selectedTypes = ref([])
const toggleAllTypes = () => {
  if(selectedTypes.value.length === typeDefs.length){ selectedTypes.value = [] } else { selectedTypes.value = typeDefs.map(t=>t.value) }
}
const selectDate = (i) => {
  activeDate.value = i
  const d = dateTabs.value[i].dateObj
  goDate.value = new Date(d)
  search()
}

const swap = () => {
  const a = from.value
  from.value = to.value
  to.value = a
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

const trains = ref([])
const loading = ref(false)

const seatTypes = [
  { key: 'swz_num', class: '' }, // 商务/特等
  { key: 'ydz_num', class: '' }, // 优选一等
  { key: 'ydz_num', class: '' }, // 一等
  { key: 'edz_num', class: '' }, // 二等
  { key: 'gjrw_num', class: '' }, // 高级软卧
  { key: 'rw_num', class: '' }, // 软卧
  { key: 'dw_num', class: '' }, // 动卧
  { key: 'yw_num', class: '' }, // 硬卧
  { key: 'rz_num', class: '' }, // 软座
  { key: 'yz_num', class: '' }, // 硬座
  { key: 'wz_num', class: '' }, // 无座
  { key: 'qt_num', class: '' }, // 其他
]

const search = () => {
  loading.value = true
  // Mock data
  setTimeout(() => {
    trains.value = [
      {
        train_no: '1',
        station_train_code: 'G1',
        from_station_name: from.value,
        to_station_name: to.value,
        start_time: '09:00',
        arrive_time: '13:30',
        lishi: '04:30',
        day_difference: '0',
        swz_num: '10',
        ydz_num: '20',
        edz_num: '有',
        wz_num: '--',
      },
      {
        train_no: '2',
        station_train_code: 'G2',
        from_station_name: from.value,
        to_station_name: to.value,
        start_time: '10:00',
        arrive_time: '14:30',
        lishi: '04:30',
        day_difference: '0',
        swz_num: '无',
        ydz_num: '5',
        edz_num: '有',
        wz_num: '--',
      },
       {
        train_no: '3',
        station_train_code: 'K100',
        from_station_name: from.value,
        to_station_name: to.value,
        start_time: '18:00',
        arrive_time: '06:00',
        lishi: '12:00',
        day_difference: '1',
        rw_num: '10',
        yw_num: '20',
        yz_num: '有',
        wz_num: '有',
      }
    ]
    loading.value = false
  }, 500)
}

onMounted(() => {
  search()
})
</script>

<style>
@import url('@/assets/12306-leftticket/leftTicket.css');
.leftticket-page .wrapper{width:1200px;margin:0 auto}
.t-list { border: 1px solid #298cce; margin-top: 10px; }
.t-list table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.t-list th { background: #eef1f8; height: 40px; border-right: 1px solid #b0cccc; border-bottom: 1px solid #b0cccc; font-size: 12px; color: #333; }
.t-list td { height: 50px; border-right: 1px solid #b0cccc; border-bottom: 1px solid #b0cccc; text-align: center; font-size: 12px; color: #333; }
.t-list .bgc { background: #f8f8f8; }
.train .number { font-size: 16px; font-weight: bold; }
.cdz_name strong, .cds_name strong { display: block; line-height: 20px; }
.start-s, .start-t { color: #333; }
.end-s, .color999 { color: #999; }
.ls_name strong { display: block; font-weight: bold; }
</style>