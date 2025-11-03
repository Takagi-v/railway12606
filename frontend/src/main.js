/**
 * Railway 12306 Frontend Main Entry
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import { ConfigProvider } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import antdTheme from './config/theme.js'
import './assets/main.css'
import './styles/theme.css'
import './assets/design-system.css'

const app = createApp(App)

// 配置 Ant Design Vue 主题
app.use(Antd)
app.use(createPinia())
app.use(router)

// 全局配置 Ant Design Vue 主题
app.provide('antdTheme', antdTheme)

app.mount('#app')
