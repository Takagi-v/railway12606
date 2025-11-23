<template>
  <div class="empty-container" :class="containerClass">
    <div class="empty-content">
      <!-- 图标区域 -->
      <div class="empty-icon">
        <slot name="icon">
          <!-- 12306风格的火车站图标 -->
          <svg v-if="type === 'train'" viewBox="0 0 64 64" width="64" height="64">
            <g fill="var(--text-color-secondary)" opacity="0.4">
              <path
                d="M32 8c-13.255 0-24 10.745-24 24s10.745 24 24 24 24-10.745 24-24S45.255 8 32 8zm0 44c-11.046 0-20-8.954-20-20s8.954-20 20-20 20 8.954 20 20-8.954 20-20 20z"
              />
              <path
                d="M32 16c-8.837 0-16 7.163-16 16s7.163 16 16 16 16-7.163 16-16-7.163-16-16-16zm-8 20h4v-8h8v8h4v-12c0-2.209-1.791-4-4-4h-8c-2.209 0-4 1.791-4 4v12z"
              />
            </g>
          </svg>

          <!-- 订单图标 -->
          <svg v-else-if="type === 'order'" viewBox="0 0 64 64" width="64" height="64">
            <g fill="var(--text-color-secondary)" opacity="0.4">
              <path
                d="M48 12H16c-2.21 0-4 1.79-4 4v32c0 2.21 1.79 4 4 4h32c2.21 0 4-1.79 4-4V16c0-2.21-1.79-4-4-4zM44 44H20V20h24v24z"
              />
              <path d="M24 28h16v4H24zm0 8h12v4H24z" />
            </g>
          </svg>

          <!-- 搜索图标 -->
          <svg v-else-if="type === 'search'" viewBox="0 0 64 64" width="64" height="64">
            <g fill="var(--text-color-secondary)" opacity="0.4">
              <circle cx="26" cy="26" r="16" fill="none" stroke="currentColor" stroke-width="4" />
              <path d="M46 46l-8-8" stroke="currentColor" stroke-width="4" />
            </g>
          </svg>

          <!-- 默认图标 -->
          <svg v-else viewBox="0 0 64 64" width="64" height="64">
            <g fill="var(--text-color-secondary)" opacity="0.4">
              <path
                d="M32 8L8 20v24l24 12 24-12V20L32 8zm0 8l16 8-16 8-16-8 16-8zm-20 12l16 8v16l-16-8V28zm40 0v16l-16 8V28l16-8z"
              />
            </g>
          </svg>
        </slot>
      </div>

      <!-- 文字描述 -->
      <div class="empty-description">
        <div class="empty-title">{{ title || defaultTitle }}</div>
        <div v-if="description" class="empty-subtitle">{{ description }}</div>
      </div>

      <!-- 操作按钮 -->
      <div v-if="$slots.action" class="empty-action">
        <slot name="action"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Empty',
  props: {
    type: {
      type: String,
      default: 'default', // default, train, order, search
      validator: value => ['default', 'train', 'order', 'search'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: value => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    containerClass() {
      return [`empty-container--${this.size}`]
    },
    defaultTitle() {
      const titles = {
        train: '暂无车次信息',
        order: '暂无订单记录',
        search: '未找到相关结果',
        default: '暂无数据'
      }
      return titles[this.type] || titles.default
    }
  }
}
</script>

<style scoped>
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--spacing-xxl) var(--spacing-lg);
  min-height: 200px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 400px;
}

.empty-icon {
  margin-bottom: var(--spacing-lg);
  opacity: 0.6;
}

.empty-description {
  margin-bottom: var(--spacing-lg);
}

.empty-title {
  font-size: var(--font-size-lg);
  color: var(--text-color);
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
}

.empty-subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
  line-height: var(--line-height-normal);
}

.empty-action {
  margin-top: var(--spacing-md);
}

/* 尺寸变体 */
.empty-container--small {
  padding: var(--spacing-lg);
  min-height: 120px;
}

.empty-container--small .empty-icon svg {
  width: 48px;
  height: 48px;
}

.empty-container--small .empty-title {
  font-size: var(--font-size-md);
}

.empty-container--small .empty-subtitle {
  font-size: var(--font-size-xs);
}

.empty-container--large {
  padding: var(--spacing-xxl) var(--spacing-xl);
  min-height: 300px;
}

.empty-container--large .empty-icon svg {
  width: 96px;
  height: 96px;
}

.empty-container--large .empty-title {
  font-size: var(--font-size-xl);
}

.empty-container--large .empty-subtitle {
  font-size: var(--font-size-md);
}

/* 12306风格适配 */
.empty-container {
  background: var(--background-color-light);
  border-radius: var(--border-radius-medium);
}

.empty-title {
  color: var(--heading-color);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .empty-container {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .empty-content {
    max-width: 300px;
  }
}
</style>
