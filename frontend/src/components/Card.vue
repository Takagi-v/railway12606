<template>
  <div class="railway-card" :class="cardClass">
    <!-- 卡片头部 -->
    <div v-if="title || $slots.title || $slots.extra" class="card-header">
      <div class="card-title-wrapper">
        <slot name="title">
          <h3 v-if="title" class="card-title">{{ title }}</h3>
        </slot>
      </div>
      <div v-if="$slots.extra" class="card-extra">
        <slot name="extra"></slot>
      </div>
    </div>

    <!-- 卡片内容 -->
    <div class="card-body" :class="bodyClass">
      <slot></slot>
    </div>

    <!-- 卡片底部 -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    title: {
      type: String,
      default: ''
    },
    bordered: {
      type: Boolean,
      default: true
    },
    hoverable: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'default', // small, default, large
      validator: value => ['small', 'default', 'large'].includes(value)
    },
    type: {
      type: String,
      default: 'default', // default, primary, success, warning, error
      validator: value => ['default', 'primary', 'success', 'warning', 'error'].includes(value)
    },
    shadow: {
      type: String,
      default: 'light', // none, light, medium, heavy
      validator: value => ['none', 'light', 'medium', 'heavy'].includes(value)
    }
  },
  computed: {
    cardClass() {
      return {
        'railway-card--bordered': this.bordered,
        'railway-card--hoverable': this.hoverable,
        'railway-card--loading': this.loading,
        [`railway-card--${this.size}`]: this.size !== 'default',
        [`railway-card--${this.type}`]: this.type !== 'default',
        [`railway-card--shadow-${this.shadow}`]: this.shadow !== 'none'
      }
    },
    bodyClass() {
      return {
        'card-body--loading': this.loading
      }
    }
  }
}
</script>

<style scoped>
.railway-card {
  background: var(--background-color-light);
  border-radius: var(--border-radius-medium);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.railway-card--bordered {
  border: 1px solid var(--border-color-light);
}

.railway-card--hoverable {
  cursor: pointer;
}

.railway-card--hoverable:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.railway-card--loading {
  pointer-events: none;
}

.railway-card--loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  z-index: 1;
}

/* 阴影变体 */
.railway-card--shadow-light {
  box-shadow: var(--shadow-light);
}

.railway-card--shadow-medium {
  box-shadow: var(--shadow-medium);
}

.railway-card--shadow-heavy {
  box-shadow: var(--shadow-heavy);
}

/* 类型变体 */
.railway-card--primary {
  border-color: var(--primary-color);
}

.railway-card--primary .card-header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-color-hover));
  color: var(--text-color-inverse);
}

.railway-card--success {
  border-color: var(--success-color);
}

.railway-card--success .card-header {
  background: var(--success-color);
  color: var(--text-color-inverse);
}

.railway-card--warning {
  border-color: var(--warning-color);
}

.railway-card--warning .card-header {
  background: var(--warning-color);
  color: var(--text-color-inverse);
}

.railway-card--error {
  border-color: var(--error-color);
}

.railway-card--error .card-header {
  background: var(--error-color);
  color: var(--text-color-inverse);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color-light);
  background: var(--background-color);
}

.card-title-wrapper {
  flex: 1;
}

.card-title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--heading-color);
  line-height: var(--line-height-tight);
}

.card-extra {
  flex-shrink: 0;
  margin-left: var(--spacing-md);
}

/* 卡片内容 */
.card-body {
  padding: var(--spacing-lg);
  position: relative;
}

.card-body--loading {
  opacity: 0.7;
}

/* 卡片底部 */
.card-footer {
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--border-color-light);
  background: var(--background-color);
}

/* 尺寸变体 */
.railway-card--small .card-header {
  padding: var(--spacing-sm) var(--spacing-md);
}

.railway-card--small .card-title {
  font-size: var(--font-size-md);
}

.railway-card--small .card-body {
  padding: var(--spacing-md);
}

.railway-card--small .card-footer {
  padding: var(--spacing-sm) var(--spacing-md);
}

.railway-card--large .card-header {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.railway-card--large .card-title {
  font-size: var(--font-size-xl);
}

.railway-card--large .card-body {
  padding: var(--spacing-xl);
}

.railway-card--large .card-footer {
  padding: var(--spacing-lg) var(--spacing-xl);
}

/* 12306特色样式 */
.railway-card {
  background: var(--background-color-light);
  border: 1px solid var(--border-color-light);
  box-shadow: var(--shadow-light);
}

.railway-card--primary .card-header {
  background: var(--primary-gradient);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .card-extra {
    margin-left: 0;
    margin-top: var(--spacing-sm);
  }
  
  .card-body {
    padding: var(--spacing-md);
  }
}
</style>