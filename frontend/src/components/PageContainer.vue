<template>
  <div class="page-container" :class="containerClass">
    <!-- 页面头部 -->
    <div v-if="title || $slots.header" class="page-header">
      <div v-if="title" class="page-title">
        <h1>{{ title }}</h1>
        <p v-if="description" class="page-description">{{ description }}</p>
      </div>
      <div v-if="$slots.extra" class="page-extra">
        <slot name="extra"></slot>
      </div>
      <slot name="header"></slot>
    </div>

    <!-- 页面内容 -->
    <div class="page-content" :class="contentClass">
      <slot></slot>
    </div>

    <!-- 页面底部 -->
    <div v-if="$slots.footer" class="page-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageContainer',
  props: {
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    fluid: {
      type: Boolean,
      default: false
    },
    ghost: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    containerClass() {
      return {
        'page-container--fluid': this.fluid,
        'page-container--ghost': this.ghost,
        'page-container--loading': this.loading
      }
    },
    contentClass() {
      return {
        'page-content--loading': this.loading
      }
    }
  }
}
</script>

<style scoped>
.page-container {
  min-height: 100%;
  background: var(--background-color-light);
}

.page-container--fluid {
  padding: 0;
}

.page-container--ghost {
  background: transparent;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-lg) var(--spacing-lg) var(--spacing-md);
  background: var(--background-color-light);
  border-bottom: 1px solid var(--border-color-light);
}

.page-title h1 {
  margin: 0;
  font-size: var(--font-size-xxl);
  font-weight: 600;
  color: var(--heading-color);
  line-height: var(--line-height-tight);
}

.page-description {
  margin: var(--spacing-xs) 0 0;
  color: var(--text-color);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
}

.page-extra {
  flex-shrink: 0;
  margin-left: var(--spacing-md);
}

.page-content {
  padding: var(--spacing-lg);
  min-height: calc(100vh - 200px);
}

.page-content--loading {
  position: relative;
  pointer-events: none;
  opacity: 0.7;
}

.page-footer {
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--background-color-light);
  border-top: 1px solid var(--border-color-light);
}

/* 12306风格适配 */
.page-container {
  background: var(--background-color);
}

.page-header {
  background: var(--background-color-light);
  box-shadow: var(--shadow-light);
}

.page-content {
  background: transparent;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-extra {
    margin-left: 0;
    margin-top: var(--spacing-md);
  }

  .page-content {
    padding: var(--spacing-md);
  }
}
</style>
