/**
 * Railway 12306 Frontend Main Entry
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import './assets/main.css'

// 导入权限相关
import PermissionComponents from './components/Permission'
import permissionDirectives from './directives/permission'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

// 注册权限组件
app.use(PermissionComponents)

// 注册权限指令
app.directive('permission', permissionDirectives.permission)
app.directive('role', permissionDirectives.role)
app.directive('auth', permissionDirectives.auth)

app.mount('#app')

