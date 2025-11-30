/**
 * Railway 12306 Frontend Main Entry
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import './assets/main.css'
import './styles/theme.css'
import './assets/design-system.css'
// [WARNING] 禁止在此处引入 12306 相关的全局 CSS (如 leftTicket.css, index_y_v50003.css)
// 这些样式文件包含大量通用类名，会污染整个应用的样式。
// 请务必在具体组件中使用 <style scoped> @import ... </style> 进行引入。
// 详情请参考：frontend/CSS_BEST_PRACTICES.md
// import './assets/12306-leftticket/leftTicket.css'
import antdTheme from './config/theme.js'

// 权限相关
import PermissionComponents from './components/Permission'
import permissionDirectives from './directives/permission'

const app = createApp(App)

// Pinia（保留本地持久化插件）
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 路由与 UI 库
app.use(router)
app.use(Antd)

// 注册权限组件与指令（保留远端实现）
app.use(PermissionComponents)
app.directive('permission', permissionDirectives.permission)
app.directive('role', permissionDirectives.role)
app.directive('auth', permissionDirectives.auth)

// 主题配置（保留本地注入）
app.provide('antdTheme', antdTheme)

app.mount('#app')
