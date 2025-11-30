# 全局 CSS 样式冲突分析报告

## 1. 问题现象
在进行浏览器刷新（Hard Refresh）后，顶部导航栏（Header）及部分页面元素（如搜索框、字体大小、间距）出现样式突变。具体表现为：
- 顶部文字字号变小（从 14px 变为 12px 或其他）。
- 搜索框样式（边框、高度）发生变化。
- 布局间距错乱。

## 2. 冲突根源分析
经过代码审查与页面样式分析，确认冲突的根源在于 **全局引入了 12306 官方的远程 CSS 文件**，且引入方式导致其样式规则污染了整个应用。

### 2.1 关键冲突文件
*   **入口文件**: `frontend/src/main.js`
    ```javascript
    // Line 15
    import './assets/12306-leftticket/leftTicket.css'
    ```
    此行代码将 `leftTicket.css` 作为全局样式加载，意味着应用中的**所有页面**都会受到该 CSS 的影响。

*   **样式定义文件**: `frontend/src/assets/12306-leftticket/leftTicket.css`
    ```css
    /* Line 1-3 */
    @import url('https://kyfw.12306.cn/otn/resources/merged/common_css.css');
    @import url('https://kyfw.12306.cn/otn/resources/merged/queryLeftTicket_css.css');
    @import url('https://kyfw.12306.cn/otn/resources/merged/queryLeftTicket_end_css.css');
    
    /* Line 9-15 */
    body {
        font-family: "Helvetica Neue", ...;
        font-size: 12px; /* 强制重置全局字号 */
        color: #333;
        margin: 0;
        padding: 0;
    }
    ```
    该文件通过 `@import` 引入了 12306 官方的 `common_css.css`。这个远程文件包含大量通用的类名选择器（如 `.header`, `.wrapper`, `.logo`, `.search-input` 等），这些选择器并未加命名空间限制。

### 2.2 冲突细节
本地组件 `Header12306.vue` 使用了 scoped CSS，但全局 CSS 的层叠规则（Cascading）依然会产生干扰，尤其是在以下情况：

1.  **全局 Body 重置**: `leftTicket.css` 将 `body` 字号强制设为 `12px`。而 `Header12306.vue` 中部分元素若未显式声明字号（依赖继承），则会由默认的 14px/16px 变为 12px。
2.  **同名类名冲突**: 
    *   **`.header`**: 远程 CSS 定义了 `.header` 的背景、高度等属性。
    *   **`.search-input`**: 远程 CSS 定义了输入框的边框、内边距，可能覆盖本地组件的样式。
    *   **`.logo`**: 远程 CSS 对 `.logo` 有特定定义。
3.  **加载顺序**: 在 SPA 路由跳转时，Vite 可能会动态管理样式标签的顺序；但在刷新页面时，`main.js` 中的全局 CSS 往往优先或最后加载（取决于构建顺序），导致 `common_css.css` 中的规则覆盖了组件样式的默认值（即使组件有 scoped，但若全局样式使用了 `!important` 或更高权重的选择器，或者作用于子元素，依然会产生影响）。

## 3. 受影响页面汇总
由于 `leftTicket.css` 在 `main.js` 中引入，**所有页面**均受影响，包括但不限于：
*   **首页 (`/`)**: Header 样式错乱。
*   **登录/注册页 (`/login`, `/register`)**: 顶部 Header 及表单通用样式可能受干扰。
*   **个人中心 (`/user/*`)**: 侧边栏或表格样式可能被远程 CSS 的通用表格样式污染。

## 4. 解决方案建议

### 方案一：移除全局引入（推荐）
将 `leftTicket.css` 的引入从 `main.js` 中移除，仅在需要该样式的具体页面（如余票查询页）中动态引入。

**操作步骤**:
1.  修改 `frontend/src/main.js`，删除 `import './assets/12306-leftticket/leftTicket.css'`。
2.  在 `frontend/src/views/ticket/LeftTicketSingle.vue` 和 `LeftTicketRound.vue` 中单独引入。
    *   *注意*: 由于 `@import` CSS 无法在 `<style scoped>` 中完美隔离（远程 CSS 依然是全局的），建议使用动态加载 CSS 的脚本，或者接受仅在这两个页面 Header 变样的事实。

### 方案二：样式隔离（Namespace）
如果必须保留 `leftTicket.css` 的内容，需要对其进行作用域限制。但由于它包含远程 `@import`，无法直接包裹在类名中（CSS 语法限制）。
唯一可行的方式是不使用 `@import`，而是将远程 CSS 内容下载到本地，并包裹在 `.leftticket-page` 类名下，同时确保相关页面的根元素加上该类名。

### 方案三：提高本地样式权重
在 `Header12306.vue` 等核心组件中，使用 `!important` 或增加选择器权重（如 `#app .header`）来强制覆盖远程样式。但这治标不治本，且维护成本高。

## 5. 结论
当前冲突的主要原因是**特定业务页面的 CSS（包含远程全局样式）被错误地注册为了应用级全局样式**。建议采用**方案一**，按需加载该样式文件。
