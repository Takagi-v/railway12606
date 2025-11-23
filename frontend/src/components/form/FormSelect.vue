<template>
  <a-form-item
    :name="name"
    :label="label"
    :rules="rules"
    :required="required"
    :help="help"
    :validate-status="validateStatus"
    :has-feedback="hasFeedback"
    :class="['form-select', className]"
  >
    <a-select
      v-model:value="selectValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :size="size"
      :mode="mode"
      :allow-clear="allowClear"
      :show-search="showSearch"
      :filter-option="filterOption"
      :not-found-content="notFoundContent"
      :loading="loading"
      :max-tag-count="maxTagCount"
      :max-tag-text-length="maxTagTextLength"
      :dropdown-match-select-width="dropdownMatchSelectWidth"
      :dropdown-style="dropdownStyle"
      :dropdown-class-name="dropdownClassName"
      :virtual="virtual"
      :option-label-prop="optionLabelProp"
      class="select-railway"
      @change="handleChange"
      @select="handleSelect"
      @deselect="handleDeselect"
      @search="handleSearch"
      @blur="handleBlur"
      @focus="handleFocus"
      @dropdown-visible-change="handleDropdownVisibleChange"
    >
      <template v-if="options && options.length">
        <a-select-option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
          :title="option.title || option.label"
        >
          {{ option.label }}
        </a-select-option>
      </template>

      <template v-else>
        <slot />
      </template>
    </a-select>
  </a-form-item>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

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
  // 选择值
  modelValue: {
    type: [String, Number, Array],
    default: undefined
  },
  // 选项数据
  options: {
    type: Array,
    default: () => []
  },
  // 占位符
  placeholder: {
    type: String,
    default: '请选择'
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
    validator: value => ['', 'success', 'warning', 'error', 'validating'].includes(value)
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
    validator: value => ['small', 'middle', 'large'].includes(value)
  },
  // 选择模式
  mode: {
    type: String,
    default: undefined,
    validator: value => [undefined, 'multiple', 'tags'].includes(value)
  },
  // 是否显示清除按钮
  allowClear: {
    type: Boolean,
    default: true
  },
  // 是否支持搜索
  showSearch: {
    type: Boolean,
    default: false
  },
  // 过滤选项函数
  filterOption: {
    type: [Boolean, Function],
    default: true
  },
  // 无数据时显示内容
  notFoundContent: {
    type: String,
    default: '无数据'
  },
  // 是否加载中
  loading: {
    type: Boolean,
    default: false
  },
  // 最多显示多少个标签
  maxTagCount: {
    type: [Number, String],
    default: undefined
  },
  // 最大标签文本长度
  maxTagTextLength: {
    type: Number,
    default: undefined
  },
  // 下拉菜单和选择器同宽
  dropdownMatchSelectWidth: {
    type: [Boolean, Number],
    default: true
  },
  // 下拉菜单样式
  dropdownStyle: {
    type: Object,
    default: () => ({})
  },
  // 下拉菜单类名
  dropdownClassName: {
    type: String,
    default: ''
  },
  // 是否使用虚拟滚动
  virtual: {
    type: Boolean,
    default: true
  },
  // 回填到选择框的 Option 的属性值
  optionLabelProp: {
    type: String,
    default: 'children'
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
  'select',
  'deselect',
  'search',
  'blur',
  'focus',
  'dropdownVisibleChange'
])

const selectValue = ref(props.modelValue)

// 监听外部值变化
watch(
  () => props.modelValue,
  newValue => {
    selectValue.value = newValue
  }
)

// 监听内部值变化
watch(selectValue, newValue => {
  emit('update:modelValue', newValue)
})

// 处理选择变化
const handleChange = (value, option) => {
  emit('change', value, option)
}

// 处理选中
const handleSelect = (value, option) => {
  emit('select', value, option)
}

// 处理取消选中
const handleDeselect = (value, option) => {
  emit('deselect', value, option)
}

// 处理搜索
const handleSearch = value => {
  emit('search', value)
}

// 处理失焦
const handleBlur = () => {
  emit('blur')
}

// 处理聚焦
const handleFocus = () => {
  emit('focus')
}

// 处理下拉菜单显示状态变化
const handleDropdownVisibleChange = open => {
  emit('dropdownVisibleChange', open)
}
</script>

<style scoped>
.form-select :deep(.ant-select) {
  width: 100%;
}

.form-select :deep(.ant-select .ant-select-selector) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
  transition: all var(--transition-normal);
}

.form-select :deep(.ant-select:not(.ant-select-disabled):hover .ant-select-selector) {
  border-color: var(--primary-color);
}

.form-select :deep(.ant-select-focused .ant-select-selector) {
  border-color: var(--primary-color) !important;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

/* 多选标签样式 */
.form-select :deep(.ant-select-selection-item) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: #fff;
  border-radius: var(--border-radius-small);
}

.form-select :deep(.ant-select-selection-item-remove) {
  color: rgba(255, 255, 255, 0.8);
}

.form-select :deep(.ant-select-selection-item-remove:hover) {
  color: #fff;
}

/* 占位符样式 */
.form-select :deep(.ant-select-selection-placeholder) {
  color: var(--text-color-placeholder);
}

/* 清除按钮样式 */
.form-select :deep(.ant-select-clear) {
  color: var(--text-color-secondary);
  background-color: var(--background-color);
}

.form-select :deep(.ant-select-clear:hover) {
  color: var(--text-color);
}

/* 箭头样式 */
.form-select :deep(.ant-select-arrow) {
  color: var(--text-color-secondary);
}

/* 错误状态样式 */
.form-select :deep(.ant-form-item-has-error .ant-select .ant-select-selector) {
  border-color: var(--error-color) !important;
}

.form-select :deep(.ant-form-item-has-error .ant-select-focused .ant-select-selector) {
  border-color: var(--error-color) !important;
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2) !important;
}

/* 成功状态样式 */
.form-select :deep(.ant-form-item-has-success .ant-select .ant-select-selector) {
  border-color: var(--success-color);
}

/* 禁用状态样式 */
.form-select :deep(.ant-select-disabled .ant-select-selector) {
  background-color: var(--background-color-light) !important;
  color: var(--text-color-secondary) !important;
  cursor: not-allowed !important;
}

/* 加载状态样式 */
.form-select :deep(.ant-select-selection-search-input) {
  color: var(--text-color);
}

/* 下拉菜单样式 */
.form-select :deep(.ant-select-dropdown) {
  border-radius: var(--border-radius-base);
  box-shadow: var(--shadow-base);
}

.form-select :deep(.ant-select-item) {
  color: var(--text-color);
  transition: all var(--transition-normal);
}

.form-select :deep(.ant-select-item:hover) {
  background-color: var(--background-color-light);
}

.form-select :deep(.ant-select-item-option-selected) {
  background-color: var(--primary-color);
  color: #fff;
}

.form-select :deep(.ant-select-item-option-active) {
  background-color: rgba(74, 144, 226, 0.1);
}

.form-select :deep(.ant-select-item-option-disabled) {
  color: var(--text-color-disabled);
  cursor: not-allowed;
}

/* 空状态样式 */
.form-select :deep(.ant-select-item-empty) {
  color: var(--text-color-secondary);
  text-align: center;
  padding: var(--spacing-md);
}
</style>
