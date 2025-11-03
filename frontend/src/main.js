/**
 * Railway 12306 Frontend Main Entry
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Antd from 'ant-design-vue'
import { ConfigProvider } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import antdTheme from './config/theme.js'
import { createPermissionDirective } from './utils/permission.js'
import './assets/main.css'
import './styles/theme.css'
import './assets/design-system.css'

const app = createApp(App)
const pinia = createPinia()

// 配置 Pinia 持久化插件
pinia.use(piniaPluginPersistedstate)

// 注册权限指令
app.directive('permission', createPermissionDirective())

// 配置 Ant Design Vue 主题
app.use(Antd)
app.use(pinia)
app.use(router)

// 全局配置 Ant Design Vue 主题
app.provide('antdTheme', antdTheme)

app.mount('#app')
