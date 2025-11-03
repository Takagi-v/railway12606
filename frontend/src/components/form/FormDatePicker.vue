<template>
  <a-form-item
    :name="name"
    :label="label"
    :rules="rules"
    :required="required"
    :help="help"
    :validate-status="validateStatus"
    :has-feedback="hasFeedback"
    :class="['form-date-picker', className]"
  >
    <a-date-picker
      v-if="type === 'date'"
      v-model:value="dateValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :size="size"
      :format="format"
      :value-format="valueFormat"
      :show-time="showTime"
      :show-today="showToday"
      :allow-clear="allowClear"
      :disabled-date="disabledDate"
      :disabled-time="disabledTime"
      :picker="picker"
      :mode="mode"
      :open="open"
      :dropdown-class-name="dropdownClassName"
      :popup-style="popupStyle"
      :input-read-only="inputReadOnly"
      class="picker-railway"
      @change="handleChange"
      @ok="handleOk"
      @panel-change="handlePanelChange"
      @open-change="handleOpenChange"
    />
    
    <a-range-picker
      v-else-if="type === 'range'"
      v-model:value="dateValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :size="size"
      :format="format"
      :value-format="valueFormat"
      :show-time="showTime"
      :allow-clear="allowClear"
      :disabled-date="disabledDate"
      :disabled-time="disabledTime"
      :picker="picker"
      :mode="mode"
      :open="open"
      :dropdown-class-name="dropdownClassName"
      :popup-style="popupStyle"
      :input-read-only="inputReadOnly"
      :separator="separator"
      class="picker-railway"
      @change="handleChange"
      @ok="handleOk"
      @panel-change="handlePanelChange"
      @open-change="handleOpenChange"
      @calendar-change="handleCalendarChange"
    />
    
    <a-time-picker
      v-else-if="type === 'time'"
      v-model:value="dateValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :size="size"
      :format="format"
      :value-format="valueFormat"
      :allow-clear="allowClear"
      :disabled-time="disabledTime"
      :hour-step="hourStep"
      :minute-step="minuteStep"
      :second-step="secondStep"
      :use12-hours="use12Hours"
      :open="open"
      :dropdown-class-name="dropdownClassName"
      :popup-style="popupStyle"
      :input-read-only="inputReadOnly"
      class="picker-railway"
      @change="handleChange"
      @open-change="handleOpenChange"
    />
  </a-form-item>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs'

const props = defineProps({
  // 表单项名称
  name: {
    type: String,
    required: true
  },
  // 标签文本
  label: {
    type: String,
    default: ''
  },
  // 选择器类型
  type: {
    type: String,
    default: 'date',
    validator: (value) => ['date', 'range', 'time'].includes(value)
  },
  // 日期值
  modelValue: {
    type: [String, Array, Object],
    default: undefined
  },
  // 占位符
  placeholder: {
    type: [String, Array],
    default: () => {
      return {
        date: '请选择日期',
        range: ['开始日期', '结束日期'],
        time: '请选择时间'
      }
    }
  },
  // 验证规则
  rules: {
    type: Array,
    default: () => []
  },
  // 是否必填
  required: {
    type: Boolean,
    default: false
  },
  // 帮助文本
  help: {
    type: String,
    default: ''
  },
  // 验证状态
  validateStatus: {
    type: String,
    default: '',
    validator: (value) => ['', 'success', 'warning', 'error', 'validating'].includes(value)
  },
  // 是否显示反馈图标
  hasFeedback: {
    type: Boolean,
    default: false
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  },
  // 尺寸
  size: {
    type: String,
    default: 'middle',
    validator: (value) => ['small', 'middle', 'large'].includes(value)
  },
  // 显示格式
  format: {
    type: String,
    default: 'YYYY-MM-DD'
  },
  // 值格式
  valueFormat: {
    type: String,
    default: 'YYYY-MM-DD'
  },
  // 是否显示时间选择
  showTime: {
    type: [Boolean, Object],
    default: false
  },
  // 是否显示今天按钮
  showToday: {
    type: Boolean,
    default: true
  },
  // 是否显示清除按钮
  allowClear: {
    type: Boolean,
    default: true
  },
  // 禁用日期函数
  disabledDate: {
    type: Function,
    default: undefined
  },
  // 禁用时间函数
  disabledTime: {
    type: Function,
    default: undefined
  },
  // 选择器类型
  picker: {
    type: String,
    default: 'date',
    validator: (value) => ['date', 'week', 'month', 'quarter', 'year'].includes(value)
  },
  // 面板模式
  mode: {
    type: [String, Array],
    default: undefined
  },
  // 是否打开
  open: {
    type: Boolean,
    default: undefined
  },
  // 下拉菜单类名
  dropdownClassName: {
    type: String,
    default: ''
  },
  // 弹出框样式
  popupStyle: {
    type: Object,
    default: () => ({})
  },
  // 输入框是否只读
  inputReadOnly: {
    type: Boolean,
    default: false
  },
  // 范围选择器分隔符
  separator: {
    type: String,
    default: '~'
  },
  // 时间选择器小时步长
  hourStep: {
    type: Number,
    default: 1
  },
  // 时间选择器分钟步长
  minuteStep: {
    type: Number,
    default: 1
  },
  // 时间选择器秒步长
  secondStep: {
    type: Number,
    default: 1
  },
  // 是否使用12小时制
  use12Hours: {
    type: Boolean,
    default: false
  },
  // 自定义类名
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits([
  'update:modelValue',
  'change',
  'ok',
  'panelChange',
  'openChange',
  'calendarChange'
])

const dateValue = ref(props.modelValue)

// 计算占位符
const computedPlaceholder = computed(() => {
  if (typeof props.placeholder === 'string' || Array.isArray(props.placeholder)) {
    return props.placeholder
  }
  return props.placeholder[props.type] || '请选择'
})

// 监听外部值变化
watch(
  () => props.modelValue,
  (newValue) => {
    dateValue.value = newValue
  }
)

// 监听内部值变化
watch(
  dateValue,
  (newValue) => {
    emit('update:modelValue', newValue)
  }
)

// 处理日期变化
const handleChange = (date, dateString) => {
  emit('change', date, dateString)
}

// 处理确定
const handleOk = (date) => {
  emit('ok', date)
}

// 处理面板变化
const handlePanelChange = (value, mode) => {
  emit('panelChange', value, mode)
}

// 处理打开状态变化
const handleOpenChange = (open) => {
  emit('openChange', open)
}

// 处理日历变化（范围选择器）
const handleCalendarChange = (dates, dateStrings, info) => {
  emit('calendarChange', dates, dateStrings, info)
}
</script>

<style scoped>
.form-date-picker :deep(.ant-picker) {
  width: 100%;
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
  transition: all var(--transition-normal);
}

.form-date-picker :deep(.ant-picker:hover) {
  border-color: var(--primary-color);
}

.form-date-picker :deep(.ant-picker-focused) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* 输入框样式 */
.form-date-picker :deep(.ant-picker-input > input) {
  color: var(--text-color);
}

.form-date-picker :deep(.ant-picker-input > input::placeholder) {
  color: var(--text-color-placeholder);
}

/* 清除按钮样式 */
.form-date-picker :deep(.ant-picker-clear) {
  color: var(--text-color-secondary);
  background-color: var(--background-color);
}

.form-date-picker :deep(.ant-picker-clear:hover) {
  color: var(--text-color);
}

/* 后缀图标样式 */
.form-date-picker :deep(.ant-picker-suffix) {
  color: var(--text-color-secondary);
}

/* 分隔符样式 */
.form-date-picker :deep(.ant-picker-separator) {
  color: var(--text-color-secondary);
}

/* 错误状态样式 */
.form-date-picker :deep(.ant-form-item-has-error .ant-picker) {
  border-color: var(--error-color);
}

.form-date-picker :deep(.ant-form-item-has-error .ant-picker-focused) {
  border-color: var(--error-color);
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2);
}

/* 成功状态样式 */
.form-date-picker :deep(.ant-form-item-has-success .ant-picker) {
  border-color: var(--success-color);
}

/* 禁用状态样式 */
.form-date-picker :deep(.ant-picker[disabled]) {
  background-color: var(--background-color-light);
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

.form-date-picker :deep(.ant-picker[disabled] .ant-picker-input > input) {
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

/* 下拉面板样式 */
.form-date-picker :deep(.ant-picker-dropdown) {
  border-radius: var(--border-radius-base);
  box-shadow: var(--shadow-base);
}

.form-date-picker :deep(.ant-picker-panel) {
  background-color: var(--background-color);
  border-radius: var(--border-radius-base);
}

/* 日期单元格样式 */
.form-date-picker :deep(.ant-picker-cell) {
  color: var(--text-color);
}

.form-date-picker :deep(.ant-picker-cell:hover:not(.ant-picker-cell-selected):not(.ant-picker-cell-range-start):not(.ant-picker-cell-range-end):not(.ant-picker-cell-range-hover-start):not(.ant-picker-cell-range-hover-end)) .ant-picker-cell-inner {
  background-color: var(--background-color-light);
}

.form-date-picker :deep(.ant-picker-cell-selected .ant-picker-cell-inner) {
  background-color: var(--primary-color);
  color: #fff;
}

.form-date-picker :deep(.ant-picker-cell-today .ant-picker-cell-inner) {
  border-color: var(--primary-color);
}

/* 范围选择样式 */
.form-date-picker :deep(.ant-picker-cell-range-start .ant-picker-cell-inner) {
  background-color: var(--primary-color);
  color: #fff;
}

.form-date-picker :deep(.ant-picker-cell-range-end .ant-picker-cell-inner) {
  background-color: var(--primary-color);
  color: #fff;
}

.form-date-picker :deep(.ant-picker-cell-in-range .ant-picker-cell-inner) {
  background-color: rgba(74, 144, 226, 0.1);
}

/* 按钮样式 */
.form-date-picker :deep(.ant-picker-today-btn) {
  color: var(--primary-color);
}

.form-date-picker :deep(.ant-picker-today-btn:hover) {
  color: var(--primary-color-hover);
}

.form-date-picker :deep(.ant-btn-primary) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.form-date-picker :deep(.ant-btn-primary:hover) {
  background-color: var(--primary-color-hover);
  border-color: var(--primary-color-hover);
}
</style>