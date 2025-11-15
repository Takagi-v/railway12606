<template>
  <div class="gototop js-top" :class="{ visible }">
    <a href="javascript:void(0)" class="js-gotop" title="返回顶部" @click="scrollTop">
      <i class="icon icon-gotop"></i>
    </a>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const visible = ref(false)
const threshold = 180

const handleScroll = () => {
  visible.value = window.scrollY > threshold
}

const scrollTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* 贴近官网：固定在右下角，渐显/隐藏 */
.gototop {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 50px;
  height: 50px;
  opacity: 0;
  visibility: hidden;
  transition: 0.6s linear opacity;
  z-index: 1100;
}
.gototop.visible { opacity: 1; visibility: visible; }

.js-gotop {
  display: flex; /* 让内部图标在容器中居中 */
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: #efefef; /* 与官网一致的浅灰底 */
  border: 1px solid #ddd;
  box-shadow: none;
  border-radius: 0;
}
.js-gotop:hover .icon-gotop { opacity: 0.85; }

.js-gotop .icon-gotop {
  display: block;
  margin: 0;
  font-size: 22px;
  line-height: 1; /* 由外层 flex 居中，不依赖行高 */
  text-align: center;
  color: #666; /* 官网图标为中性灰 */
  background: transparent; /* 防止出现色块背景 */
}
</style>