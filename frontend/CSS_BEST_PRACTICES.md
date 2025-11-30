# 12306 复刻页面样式开发规范 (CSS Best Practices)

## 背景 (Context)
本项目包含大量对 12306 官网页面的高保真复刻。为了实现这一目标，我们需要引入 12306 官方的 CSS 文件（如 `index_y_v50003.css`, `leftTicket.css` 等）。

## 问题 (The Problem)
12306 官方 CSS 文件是为了传统多页应用（MPA）设计的，使用了大量通用的全局类名（例如 `.header`, `.search-index`, `.nav`, `.input` 等）。
在 Vue 单页应用（SPA）中，如果在全局（如 `main.js` 或 `App.vue`）引入这些文件，会导致严重的**样式污染**：
- **覆盖问题**：复刻页面的样式会影响到项目中的其他通用组件（如 Ant Design 组件、通用布局）。
- **持久化问题**：一旦访问了加载过这些样式的页面，样式会残留在浏览器中，即使用户跳转到其他页面，布局依然会崩坏（直到页面刷新）。

## 开发规范 (Guidelines)

为了避免上述问题，所有复刻页面的开发**必须**严格遵守以下规范：

### 1. 资源本地化 (Localize Assets)
- **不要**直接使用远程 URL (`@import url('https://...')`) 引入 CSS。远程文件可能变化，且不仅影响加载速度，还难以控制。
- **操作**：将需要的 12306 CSS 文件下载到 `src/assets/` 下的专用目录中（例如 `src/assets/12306-homepage/` 或 `src/assets/12306-leftticket/`）。

### 2. 严格的作用域隔离 (Strict Scoped Import)
- **禁止**在 `main.js`、`App.vue` 或任何全局样式文件中引入 12306 的 CSS 文件。
- **必须**在具体使用该样式的 Vue 组件中，通过 `<style scoped>` 进行引入。

#### ✅ 正确示例 (Correct)
```vue
<!-- src/views/HomePage.vue 或 src/components/SectionFirst12306.vue -->
<template>
  <div class="railway-homepage">
    <!-- ... -->
  </div>
</template>

<style scoped>
/* 启用 scoped，确保样式只在当前组件生效 */
@import '@/assets/12306-homepage/index_y_v50003.css';

/* 组件特定的修正样式 */
.railway-homepage {
  /* ... */
}
</style>
```

#### ❌ 错误示例 (Incorrect)
```javascript
// src/main.js
import './assets/12306-homepage/index_y_v50003.css' // 禁止全局引入！
```

```vue
<!-- 组件中未使用 scoped -->
<style> 
@import '@/assets/12306-homepage/index_y_v50003.css'; /* 禁止！这会污染全局 */
</style>
```

### 3. 验证流程 (Verification)
开发完复刻页面后，必须执行以下测试：
1. **进入页面**：页面样式显示正常。
2. **离开页面**：跳转到系统的其他标准页面（如个人中心、登录页）。
3. **检查污染**：确认其他页面的布局（Header、导航栏、表单）没有发生变形或错位。
4. **返回页面**：再次回到复刻页面，确认样式依然正常。

## 现有资源目录
- `src/assets/12306-leftticket/`: 车票查询页相关样式
- `src/assets/12306-homepage/`: 首页相关样式
- `src/assets/design-system.css`: 系统通用的原子化设计系统（安全，可全局引用）

---
*此文档供开发人员及 AI 辅助工具参考，旨在维护项目样式的健壮性。*
