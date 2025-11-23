<template>
  <a-form-item
    :name="name"
    :label="label"
    :rules="rules"
    :required="required"
    :help="help"
    :validate-status="validateStatus"
    :has-feedback="hasFeedback"
    :class="['form-input', className]"
  >
    <a-input
      v-if="type === 'text' || type === 'email' || type === 'tel'"
      v-model:value="inputValue"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :size="size"
      :maxlength="maxlength"
      :show-count="showCount"
      :allow-clear="allowClear"
      :prefix="prefix"
      :suffix="suffix"
      :addon-before="addonBefore"
      :addon-after="addonAfter"
      class="input-railway"
      @change="handleChange"
      @blur="handleBlur"
      @focus="handleFocus"
      @pressEnter="handlePressEnter"
    />

    <a-input-password
      v-else-if="type === 'password'"
      v-model:value="inputValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :size="size"
      :maxlength="maxlength"
      :show-count="showCount"
      :visibility-toggle="visibilityToggle"
      class="input-railway"
      @change="handleChange"
      @blur="handleBlur"
      @focus="handleFocus"
      @pressEnter="handlePressEnter"
    />

    <a-textarea
      v-else-if="type === 'textarea'"
      v-model:value="inputValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :size="size"
      :maxlength="maxlength"
      :show-count="showCount"
      :allow-clear="allowClear"
      :rows="rows"
      :auto-size="autoSize"
      class="input-railway"
      @change="handleChange"
      @blur="handleBlur"
      @focus="handleFocus"
      @pressEnter="handlePressEnter"
    />

    <a-input-number
      v-else-if="type === 'number'"
      v-model:value="inputValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :size="size"
      :min="min"
      :max="max"
      :step="step"
      :precision="precision"
      :formatter="formatter"
      :parser="parser"
      class="input-railway"
      @change="handleChange"
      @blur="handleBlur"
      @focus="handleFocus"
      @pressEnter="handlePressEnter"
    />
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
  // 输入类型
  type: {
    type: String,
    default: 'text',
    validator: value => ['text', 'password', 'email', 'tel', 'textarea', 'number'].includes(value)
  },
  // 输入值
  modelValue: {
    type: [String, Number],
    default: ''
  },
  // 占位符
  placeholder: {
    type: String,
    default: ''
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
  // 是否只读
  readonly: {
    type: Boolean,
    default: false
  },
  // 尺寸
  size: {
    type: String,
    default: 'middle',
    validator: value => ['small', 'middle', 'large'].includes(value)
  },
  // 最大长度
  maxlength: {
    type: Number,
    default: undefined
  },
  // 是否显示字符计数
  showCount: {
    type: Boolean,
    default: false
  },
  // 是否显示清除按钮
  allowClear: {
    type: Boolean,
    default: true
  },
  // 前缀图标
  prefix: {
    type: String,
    default: ''
  },
  // 后缀图标
  suffix: {
    type: String,
    default: ''
  },
  // 前置标签
  addonBefore: {
    type: String,
    default: ''
  },
  // 后置标签
  addonAfter: {
    type: String,
    default: ''
  },
  // 自定义类名
  className: {
    type: String,
    default: ''
  },
  // 密码输入框是否显示切换按钮
  visibilityToggle: {
    type: Boolean,
    default: true
  },
  // 文本域行数
  rows: {
    type: Number,
    default: 4
  },
  // 文本域自适应高度
  autoSize: {
    type: [Boolean, Object],
    default: false
  },
  // 数字输入框最小值
  min: {
    type: Number,
    default: undefined
  },
  // 数字输入框最大值
  max: {
    type: Number,
    default: undefined
  },
  // 数字输入框步长
  step: {
    type: Number,
    default: 1
  },
  // 数字输入框精度
  precision: {
    type: Number,
    default: undefined
  },
  // 数字输入框格式化函数
  formatter: {
    type: Function,
    default: undefined
  },
  // 数字输入框解析函数
  parser: {
    type: Function,
    default: undefined
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'blur', 'focus', 'pressEnter'])

const inputValue = ref(props.modelValue)

// 监听外部值变化
watch(
  () => props.modelValue,
  newValue => {
    inputValue.value = newValue
  }
)

// 监听内部值变化
watch(inputValue, newValue => {
  emit('update:modelValue', newValue)
})

// 处理输入变化
const handleChange = e => {
  const value = e.target ? e.target.value : e
  emit('change', value)
}

// 处理失焦
const handleBlur = e => {
  emit('blur', e)
}

// 处理聚焦
const handleFocus = e => {
  emit('focus', e)
}

// 处理回车
const handlePressEnter = e => {
  emit('pressEnter', e)
}
</script>

<style scoped>
.form-input :deep(.ant-input) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
  transition: all var(--transition-normal);
}

.form-input :deep(.ant-input:hover) {
  border-color: var(--primary-color);
}

.form-input :deep(.ant-input:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.form-input :deep(.ant-input-number) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
  width: 100%;
}

.form-input :deep(.ant-input-number:hover) {
  border-color: var(--primary-color);
}

.form-input :deep(.ant-input-number-focused) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* 错误状态样式 */
.form-input :deep(.ant-form-item-has-error .ant-input) {
  border-color: var(--error-color);
}

.form-input :deep(.ant-form-item-has-error .ant-input:focus) {
  border-color: var(--error-color);
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2);
}

.form-input :deep(.ant-form-item-has-error .ant-input-number) {
  border-color: var(--error-color);
}

.form-input :deep(.ant-form-item-has-error .ant-input-number-focused) {
  border-color: var(--error-color);
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2);
}

/* 成功状态样式 */
.form-input :deep(.ant-form-item-has-success .ant-input) {
  border-color: var(--success-color);
}

.form-input :deep(.ant-form-item-has-success .ant-input-number) {
  border-color: var(--success-color);
}

/* 禁用状态样式 */
.form-input :deep(.ant-input[disabled]) {
  background-color: var(--background-color-light);
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

.form-input :deep(.ant-input-number[disabled]) {
  background-color: var(--background-color-light);
  color: var(--text-color-secondary);
  cursor: not-allowed;
}

/* 前缀后缀样式 */
.form-input :deep(.ant-input-prefix) {
  color: var(--text-color-secondary);
}

.form-input :deep(.ant-input-suffix) {
  color: var(--text-color-secondary);
}

/* 计数器样式 */
.form-input :deep(.ant-input-show-count-suffix) {
  color: var(--text-color-secondary);
  font-size: var(--font-size-sm);
}

/* 清除按钮样式 */
.form-input :deep(.ant-input-clear-icon) {
  color: var(--text-color-secondary);
  font-size: var(--font-size-sm);
}

.form-input :deep(.ant-input-clear-icon:hover) {
  color: var(--text-color);
}
</style>
