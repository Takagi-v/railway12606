<template>
  <a-config-provider :locale="zhCN" :theme="antdTheme">
    <router-view />
  </a-config-provider>
</template>

<script setup>
<<<<<<< HEAD
import { ConfigProvider as AConfigProvider } from 'ant-design-vue'
import { inject } from 'vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'

dayjs.locale('zh-cn')

// 注入主题配置
const antdTheme = inject('antdTheme')
=======
import { ConfigProvider as AConfigProvider } from "ant-design-vue";
import zhCN from "ant-design-vue/es/locale/zh_CN";
import dayjs from "dayjs";
import "dayjs/locale/zh-cn";

dayjs.locale("zh-cn");
>>>>>>> origin/feature/user-authentication
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
<<<<<<< HEAD
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans',
    sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
=======
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue",
    Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji",
    "Segoe UI Symbol", "Noto Color Emoji";
>>>>>>> origin/feature/user-authentication
}
</style>
