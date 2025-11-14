/**
 * Railway 12306 Frontend Main Entry
 */
import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";

import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
import "./styles/theme.css";
import "./assets/design-system.css";
import antdTheme from "./config/theme.js";

// 权限相关
import PermissionComponents from "./components/Permission";
import permissionDirectives from "./directives/permission";

const app = createApp(App);

// Pinia（保留本地持久化插件）
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);

// 路由与 UI 库
app.use(router);
app.use(Antd);

// 注册权限组件与指令（保留远端实现）
app.use(PermissionComponents);
app.directive("permission", permissionDirectives.permission);
app.directive("role", permissionDirectives.role);
app.directive("auth", permissionDirectives.auth);

// 主题配置（保留本地注入）
app.provide("antdTheme", antdTheme);

app.mount("#app");
