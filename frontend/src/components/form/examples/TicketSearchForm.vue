<template>
  <div class="ticket-search-form-container">
    <BaseForm
      :form-data="formData"
      :rules="searchRules"
      layout="horizontal"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      submit-text="查询车票"
      :show-cancel="false"
      @submit="handleSearch"
    >
      <template #form-items>
        <FormSelect
          name="fromStation"
          label="出发地"
          v-model:value="formData.fromStation"
          :options="stationOptions"
          placeholder="请选择出发地"
          show-search
          :filter-option="filterStation"
        />

        <FormSelect
          name="toStation"
          label="目的地"
          v-model:value="formData.toStation"
          :options="stationOptions"
          placeholder="请选择目的地"
          show-search
          :filter-option="filterStation"
        />

        <FormDatePicker
          name="departureDate"
          label="出发日期"
          v-model:value="formData.departureDate"
          placeholder="请选择出发日期"
          :disabled-date="disabledDate"
        />

        <FormDatePicker
          name="returnDate"
          label="返程日期"
          v-model:value="formData.returnDate"
          placeholder="请选择返程日期（可选）"
          :disabled-date="disabledReturnDate"
        />

        <FormSelect
          name="trainType"
          label="车次类型"
          v-model:value="formData.trainType"
          :options="trainTypeOptions"
          placeholder="请选择车次类型（可选）"
          mode="multiple"
          :max-tag-count="3"
        />

        <FormSelect
          name="seatType"
          label="座位类型"
          v-model:value="formData.seatType"
          :options="seatTypeOptions"
          placeholder="请选择座位类型（可选）"
          mode="multiple"
          :max-tag-count="3"
        />

        <a-form-item label="高级选项" name="advancedOptions">
          <div class="advanced-options">
            <a-checkbox v-model:checked="formData.onlyAvailable">只看有票</a-checkbox>
            <a-checkbox v-model:checked="formData.includeTransfer">包含中转</a-checkbox>
            <a-checkbox v-model:checked="formData.studentTicket">学生票</a-checkbox>
          </div>
        </a-form-item>
      </template>
    </BaseForm>

    <!-- 热门路线快速选择 -->
    <div class="popular-routes">
      <h3>热门路线</h3>
      <div class="route-buttons">
        <a-button
          v-for="route in popularRoutes"
          :key="`${route.from}-${route.to}`"
          size="small"
          @click="selectRoute(route)"
        >
          {{ route.from }} → {{ route.to }}
        </a-button>
      </div>
    </div>

    <!-- 站点互换按钮 -->
    <div class="station-swap">
      <a-button
        type="link"
        @click="swapStations"
        :disabled="!formData.fromStation || !formData.toStation"
      >
        <template #icon>
          <SwapOutlined />
        </template>
        互换
      </a-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { message } from 'ant-design-vue'
import { SwapOutlined } from '@ant-design/icons-vue'
import BaseForm from '../BaseForm.vue'
import FormSelect from '../FormSelect.vue'
import FormDatePicker from '../FormDatePicker.vue'
import { formRules } from '@/utils/formRules.js'
import dayjs from 'dayjs'

// 表单数据
const formData = reactive({
  fromStation: undefined,
  toStation: undefined,
  departureDate: null,
  returnDate: null,
  trainType: [],
  seatType: [],
  onlyAvailable: true,
  includeTransfer: false,
  studentTicket: false
})

// 验证规则
const searchRules = formRules.ticketSearch

// 车站选项数据
const stationOptions = [
  { label: '北京', value: 'BJP' },
  { label: '上海', value: 'SHH' },
  { label: '广州', value: 'GZQ' },
  { label: '深圳', value: 'SZN' },
  { label: '杭州', value: 'HZH' },
  { label: '南京', value: 'NJH' },
  { label: '武汉', value: 'WHN' },
  { label: '成都', value: 'CDW' },
  { label: '西安', value: 'XAN' },
  { label: '重庆', value: 'CQW' },
  { label: '天津', value: 'TJP' },
  { label: '青岛', value: 'QDK' },
  { label: '大连', value: 'DLT' },
  { label: '沈阳', value: 'SYT' },
  { label: '长春', value: 'CCT' },
  { label: '哈尔滨', value: 'HBB' },
  { label: '郑州', value: 'ZZF' },
  { label: '太原', value: 'TYV' },
  { label: '石家庄', value: 'SJP' },
  { label: '济南', value: 'JNK' }
]

// 车次类型选项
const trainTypeOptions = [
  { label: '高速动车组(G)', value: 'G' },
  { label: '动车组(D)', value: 'D' },
  { label: '城际动车组(C)', value: 'C' },
  { label: '直达特快(Z)', value: 'Z' },
  { label: '特快(T)', value: 'T' },
  { label: '快速(K)', value: 'K' },
  { label: '普通(其他)', value: 'OTHER' }
]

// 座位类型选项
const seatTypeOptions = [
  { label: '商务座', value: 'BUSINESS' },
  { label: '一等座', value: 'FIRST' },
  { label: '二等座', value: 'SECOND' },
  { label: '高级软卧', value: 'PREMIUM_SLEEPER' },
  { label: '软卧', value: 'SOFT_SLEEPER' },
  { label: '硬卧', value: 'HARD_SLEEPER' },
  { label: '软座', value: 'SOFT_SEAT' },
  { label: '硬座', value: 'HARD_SEAT' },
  { label: '无座', value: 'NO_SEAT' }
]

// 热门路线
const popularRoutes = [
  { from: 'BJP', to: 'SHH', fromName: '北京', toName: '上海' },
  { from: 'BJP', to: 'GZQ', fromName: '北京', toName: '广州' },
  { from: 'SHH', to: 'GZQ', fromName: '上海', toName: '广州' },
  { from: 'BJP', to: 'SZN', fromName: '北京', toName: '深圳' },
  { from: 'SHH', to: 'HZH', fromName: '上海', toName: '杭州' },
  { from: 'BJP', to: 'NJH', fromName: '北京', toName: '南京' }
]

// 车站过滤函数
const filterStation = (input, option) => {
  return option.label.toLowerCase().includes(input.toLowerCase())
}

// 禁用日期函数
const disabledDate = current => {
  // 禁用今天之前的日期
  return current && current < dayjs().startOf('day')
}

const disabledReturnDate = current => {
  // 禁用出发日期之前的日期
  const departureDate = formData.departureDate
  if (!departureDate) {
    return current && current < dayjs().startOf('day')
  }
  return current && current < dayjs(departureDate).startOf('day')
}

// 事件处理
const handleSearch = async values => {
  try {
    // 将前端字段映射到API参数
    const apiParams = {
      departure_city: values.fromStation,
      arrival_city: values.toStation,
      travel_date: values.departureDate ? dayjs(values.departureDate).format('YYYY-MM-DD') : null
    }

    console.log('车票搜索API参数:', apiParams)
    console.log('前端筛选条件:', {
      trainType: values.trainType,
      seatType: values.seatType,
      onlyAvailable: values.onlyAvailable,
      includeTransfer: values.includeTransfer,
      studentTicket: values.studentTicket,
      returnDate: values.returnDate
    })

    // 这里应该调用搜索API，只发送apiParams
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟API调用
    message.success('搜索完成！')
  } catch (error) {
    message.error('搜索失败，请重试')
  }
}

const selectRoute = route => {
  formData.fromStation = route.from
  formData.toStation = route.to
  message.success(`已选择路线：${route.fromName} → ${route.toName}`)
}

const swapStations = () => {
  const temp = formData.fromStation
  formData.fromStation = formData.toStation
  formData.toStation = temp
  message.info('出发地和目的地已互换')
}
</script>

<style scoped>
.ticket-search-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px;
  background: white;
  border-radius: 8px;
  box-shadow: var(--box-shadow);
  position: relative;
}

.advanced-options {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.popular-routes {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.popular-routes h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 16px;
}

.route-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.route-buttons .ant-btn {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.route-buttons .ant-btn:hover {
  background-color: var(--color-primary);
  color: white;
}

.station-swap {
  position: absolute;
  top: 50%;
  right: 32px;
  transform: translateY(-50%);
}

.station-swap .ant-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-primary);
}

.station-swap .ant-btn:hover {
  color: var(--color-primary-hover);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ticket-search-form-container {
    margin: 16px;
    padding: 24px 16px;
  }

  .advanced-options {
    flex-direction: column;
    gap: 8px;
  }

  .route-buttons {
    justify-content: center;
  }

  .station-swap {
    position: static;
    transform: none;
    text-align: center;
    margin-top: 16px;
  }
}

@media (max-width: 480px) {
  .route-buttons .ant-btn {
    font-size: 12px;
    padding: 4px 8px;
  }
}
</style>
