<template>
  <a-config-provider :locale="zhCN" :theme="antdTheme">
    <router-view />
    <FixedRight12306 v-if="showFloating" />
    <GoToTop12306 v-if="showFloating" />
  </a-config-provider>
</template>

<script setup>
import { ConfigProvider as AConfigProvider } from 'ant-design-vue'
import { inject, computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import FixedRight12306 from './components/FixedRight12306.vue'
import GoToTop12306 from './components/GoToTop12306.vue'

dayjs.locale('zh-cn')

const antdTheme = inject('antdTheme')
const route = useRoute()
const showFloating = computed(() => route.name === 'home')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans',
    sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
}
</style>

<!-- 全局引入官网 iconfont 本地副本，供各组件使用 -->
<style>
@import url('@/assets/12306-icons/fonts/iconfont.css');
</style>
