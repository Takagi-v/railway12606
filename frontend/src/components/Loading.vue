<template>
  <div class="loading-container" :class="containerClass">
    <div class="loading-content">
      <!-- 12306风格的火车加载动画 -->
      <div v-if="type === 'train'" class="loading-train">
        <div class="train-icon">
          <svg viewBox="0 0 24 24" width="48" height="48">
            <path
              fill="var(--primary-color)"
              d="M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H9L3,7V9H4V15H3V16H5V20A1,1 0 0,0 6,21H8A1,1 0 0,0 9,20V16H15V20A1,1 0 0,0 16,21H18A1,1 0 0,0 19,20V16H21V15H20V9H21M8,7.5A1.5,1.5 0 0,1 9.5,9A1.5,1.5 0 0,1 8,10.5A1.5,1.5 0 0,1 6.5,9A1.5,1.5 0 0,1 8,7.5M16,7.5A1.5,1.5 0 0,1 17.5,9A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 14.5,9A1.5,1.5 0 0,1 16,7.5Z"
            />
          </svg>
        </div>
        <div class="train-track">
          <div class="track-line"></div>
          <div class="track-line"></div>
        </div>
      </div>

      <!-- 圆形加载动画 -->
      <div v-else-if="type === 'spin'" class="loading-spin">
        <div class="spin-dot"></div>
      </div>

      <!-- 默认点状加载 -->
      <div v-else class="loading-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>

      <!-- 加载文字 -->
      <div v-if="text" class="loading-text">{{ text }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loading',
  props: {
    type: {
      type: String,
      default: 'dots', // dots, spin, train
      validator: value => ['dots', 'spin', 'train'].includes(value)
    },
    text: {
      type: String,
      default: '加载中...'
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    overlay: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    containerClass() {
      return {
        'loading-container--overlay': this.overlay,
        [`loading-container--${this.size}`]: true
      }
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--spacing-lg);
}

.loading-container--overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  z-index: 1000;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

/* 火车加载动画 */
.loading-train {
  position: relative;
  width: 120px;
  height: 60px;
}

.train-icon {
  animation: trainMove 2s linear infinite;
}

.train-track {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.track-line {
  height: 2px;
  background: var(--border-color);
  margin-bottom: 2px;
  position: relative;
  overflow: hidden;
}

.track-line::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
  animation: trackFlow 1.5s linear infinite;
}

@keyframes trainMove {
  0%,
  100% {
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(10px);
  }
}

@keyframes trackFlow {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* 圆形加载动画 */
.loading-spin {
  width: 32px;
  height: 32px;
}

.spin-dot {
  width: 100%;
  height: 100%;
  border: 3px solid var(--border-color-light);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 点状加载动画 */
.loading-dots {
  display: flex;
  gap: var(--spacing-xs);
}

.dot {
  width: 8px;
  height: 8px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: dotBounce 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}
.dot:nth-child(2) {
  animation-delay: -0.16s;
}
.dot:nth-child(3) {
  animation-delay: 0s;
}

@keyframes dotBounce {
  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 加载文字 */
.loading-text {
  color: var(--text-color);
  font-size: var(--font-size-sm);
  text-align: center;
}

/* 尺寸变体 */
.loading-container--small .loading-content {
  gap: var(--spacing-sm);
}

.loading-container--small .loading-train {
  width: 80px;
  height: 40px;
}

.loading-container--small .train-icon svg {
  width: 32px;
  height: 32px;
}

.loading-container--small .spin-dot {
  width: 24px;
  height: 24px;
}

.loading-container--small .dot {
  width: 6px;
  height: 6px;
}

.loading-container--large .loading-content {
  gap: var(--spacing-lg);
}

.loading-container--large .loading-train {
  width: 160px;
  height: 80px;
}

.loading-container--large .train-icon svg {
  width: 64px;
  height: 64px;
}

.loading-container--large .spin-dot {
  width: 48px;
  height: 48px;
}

.loading-container--large .dot {
  width: 12px;
  height: 12px;
}
</style>
