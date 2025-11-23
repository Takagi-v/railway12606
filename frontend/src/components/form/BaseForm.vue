<template>
  <a-form
    ref="formRef"
    :model="formData"
    :rules="formRules"
    :layout="layout"
    :label-col="labelCol"
    :wrapper-col="wrapperCol"
    :class="[
      'base-form',
      'form-railway',
      `form-railway--${layout}`,
      `base-form--${size}`,
      className
    ]"
    @finish="handleSubmit"
    @finishFailed="handleSubmitFailed"
    @valuesChange="handleValuesChange"
  >
    <slot />

    <!-- 表单操作按钮区域 -->
    <a-form-item v-if="showActions" :wrapper-col="actionWrapperCol" class="base-form__actions">
      <a-space :size="16">
        <a-button v-if="showCancel" @click="handleCancel">
          {{ cancelText }}
        </a-button>
        <a-button
          type="primary"
          html-type="submit"
          :loading="loading"
          :disabled="disabled"
          class="btn-railway-primary"
        >
          {{ submitText }}
        </a-button>
      </a-space>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // 表单数据
  modelValue: {
    type: Object,
    default: () => ({})
  },
  // 验证规则
  rules: {
    type: Object,
    default: () => ({})
  },
  // 表单布局
  layout: {
    type: String,
    default: 'vertical',
    validator: value => ['horizontal', 'vertical', 'inline'].includes(value)
  },
  // 标签列配置
  labelCol: {
    type: Object,
    default: () => ({ span: 6 })
  },
  // 包装列配置
  wrapperCol: {
    type: Object,
    default: () => ({ span: 18 })
  },
  // 表单尺寸
  size: {
    type: String,
    default: 'middle',
    validator: value => ['small', 'middle', 'large'].includes(value)
  },
  // 自定义类名
  className: {
    type: String,
    default: ''
  },
  // 是否显示操作按钮
  showActions: {
    type: Boolean,
    default: true
  },
  // 是否显示取消按钮
  showCancel: {
    type: Boolean,
    default: false
  },
  // 提交按钮文本
  submitText: {
    type: String,
    default: '提交'
  },
  // 取消按钮文本
  cancelText: {
    type: String,
    default: '取消'
  },
  // 提交状态
  loading: {
    type: Boolean,
    default: false
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'submit',
  'cancel',
  'change',
  'validate',
  'validateFailed'
])

const formRef = ref()
const formData = ref({ ...props.modelValue })
const formRules = computed(() => props.rules)

// 操作按钮的包装列配置
const actionWrapperCol = computed(() => {
  if (props.layout === 'horizontal') {
    return { offset: props.labelCol.span, span: props.wrapperCol.span }
  }
  return { span: 24 }
})

// 监听外部数据变化
watch(
  () => props.modelValue,
  newValue => {
    formData.value = { ...newValue }
  },
  { deep: true }
)

// 监听内部数据变化
watch(
  formData,
  newValue => {
    emit('update:modelValue', newValue)
  },
  { deep: true }
)

// 表单提交成功
const handleSubmit = values => {
  emit('submit', values)
}

// 表单提交失败
const handleSubmitFailed = errorInfo => {
  emit('validateFailed', errorInfo)
}

// 表单值变化
const handleValuesChange = (changedValues, allValues) => {
  emit('change', changedValues, allValues)
}

// 取消操作
const handleCancel = () => {
  emit('cancel')
}

// 验证表单
const validate = () => {
  return formRef.value?.validate()
}

// 验证指定字段
const validateFields = fields => {
  return formRef.value?.validateFields(fields)
}

// 重置表单
const resetFields = () => {
  formRef.value?.resetFields()
}

// 清除验证
const clearValidate = fields => {
  formRef.value?.clearValidate(fields)
}

// 设置字段值
const setFieldsValue = values => {
  formRef.value?.setFieldsValue(values)
  Object.assign(formData.value, values)
}

// 获取字段值
const getFieldsValue = fields => {
  return formRef.value?.getFieldsValue(fields)
}

// 暴露方法给父组件
defineExpose({
  validate,
  validateFields,
  resetFields,
  clearValidate,
  setFieldsValue,
  getFieldsValue,
  formRef
})
</script>

<style scoped>
.base-form {
  --form-item-margin-bottom: 24px;
}

.base-form--small {
  --form-item-margin-bottom: 16px;
}

.base-form--large {
  --form-item-margin-bottom: 32px;
}

.base-form :deep(.ant-form-item) {
  margin-bottom: var(--form-item-margin-bottom);
}

.base-form__actions {
  margin-top: var(--spacing-lg);
  margin-bottom: 0 !important;
}

.base-form__actions :deep(.ant-form-item-control-input) {
  text-align: center;
}

/* 12306风格表单样式 */
.base-form :deep(.ant-input) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
  transition: all var(--transition-normal);
}

.base-form :deep(.ant-input:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.base-form :deep(.ant-select .ant-select-selector) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
}

.base-form :deep(.ant-select:not(.ant-select-disabled):hover .ant-select-selector) {
  border-color: var(--primary-color);
}

.base-form :deep(.ant-select-focused .ant-select-selector) {
  border-color: var(--primary-color) !important;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

.base-form :deep(.ant-picker) {
  border-radius: var(--border-radius-small);
  border-color: var(--border-color);
}

.base-form :deep(.ant-picker:hover) {
  border-color: var(--primary-color);
}

.base-form :deep(.ant-picker-focused) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* 表单标签样式 */
.base-form :deep(.ant-form-item-label > label) {
  color: var(--text-color);
  font-weight: 500;
}

.base-form
  :deep(
    .ant-form-item-label
      > label.ant-form-item-required:not(.ant-form-item-required-mark-optional)::before
  ) {
  color: var(--error-color);
}

/* 错误提示样式 */
.base-form :deep(.ant-form-item-explain-error) {
  color: var(--error-color);
  font-size: var(--font-size-sm);
}

/* 成功状态样式 */
.base-form :deep(.ant-form-item-has-success .ant-input) {
  border-color: var(--success-color);
}

/* 错误状态样式 */
.base-form :deep(.ant-form-item-has-error .ant-input) {
  border-color: var(--error-color);
}

.base-form :deep(.ant-form-item-has-error .ant-select .ant-select-selector) {
  border-color: var(--error-color);
}

.base-form :deep(.ant-form-item-has-error .ant-picker) {
  border-color: var(--error-color);
}
</style>
