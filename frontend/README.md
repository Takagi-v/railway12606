# Railway 12306 Frontend

基于 Vue 3 + Vite + Ant Design Vue 的铁路12306前端应用

## 技术栈

- **Vue 3.4+** - 渐进式 JavaScript 框架
- **Vite 5.x** - 下一代前端构建工具
- **Vue Router 4.x** - 官方路由管理器
- **Pinia 2.x** - 官方状态管理库
- **Ant Design Vue 4.x** - 企业级UI组件库
- **Axios** - HTTP 客户端
- **Day.js** - 日期处理库
- **VueUse** - Vue组合式工具集

## 项目结构

```
frontend/
├── .eslintrc.cjs          # ESLint 配置文件
├── .gitignore             # Git 忽略文件
├── .prettierrc            # Prettier 配置文件
├── src/
│   ├── api/               # API 接口封装
│   │   ├── auth.js        # 认证接口
│   │   ├── order.js       # 订单接口
│   │   ├── passenger.js   # 乘客接口
│   │   ├── request.js     # Axios 配置
│   │   └── train.js       # 车次接口
│   ├── assets/            # 资源文件
│   │   └── main.css       # 全局样式
│   ├── components/        # 公共组件
│   │   ├── AppFooter.vue  # 底部信息
│   │   └── AppHeader.vue  # 顶部导航
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── stores/            # 状态管理
│   │   └── user.js        # 用户状态
│   ├── views/             # 页面组件
│   │   ├── HomePage.vue       # 首页
│   │   ├── NotFound.vue       # 404页面
│   │   ├── auth/              # 认证相关
│   │   │   ├── LoginPage.vue
│   │   │   └── RegisterPage.vue
│   │   ├── order/             # 订单相关
│   │   │   ├── OrderCreate.vue
│   │   │   └── OrderDetail.vue
│   │   ├── train/             # 车次相关
│   │   │   └── TrainList.vue
│   │   └── user/              # 用户中心
│   │       ├── OrderPage.vue
│   │       ├── PassengerPage.vue
│   │       ├── ProfilePage.vue
│   │       └── UserLayout.vue
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── index.html             # HTML 模板
├── package-lock.json      # 依赖锁定文件
├── package.json           # 项目配置和依赖
├── README.md              # 项目说明文档
└── vite.config.js         # Vite 配置
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产构建

```bash
npm run preview
```

## 开发规范

### 组件命名

- 组件文件名使用 PascalCase：`UserProfile.vue`
- 组件在模板中使用 kebab-case 或 PascalCase

### 路由配置

路由定义在 `src/router/index.js` 中，支持：

- 路由懒加载
- 路由元信息（meta）
- 路由守卫（需要登录的页面）

### 状态管理

使用 Pinia 进行状态管理，Store 定义在 `src/stores/` 目录下：

```javascript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
```

### API 调用

所有 API 调用统一使用 `src/api/` 中封装的方法：

```javascript
import { login } from '@/api/auth'

const response = await login({ username, password })
```

### 样式规范

- 使用 scoped 样式避免全局污染
- 公共样式定义在 `src/assets/main.css`
- 使用 CSS 变量定义主题色
- **特别注意**：对于 12306 复刻页面（如 LeftTicket, Homepage），**严禁**在全局引入其 CSS 文件。
  - 请参考 [CSS开发规范](CSS_BEST_PRACTICES.md) 进行资源本地化和隔离开发。

## 功能模块

### 已完成的功能框架

- [x] 项目基础架构
- [x] 路由配置和导航守卫
- [x] 用户认证（登录/注册页面框架）
- [x] 首页查询框架
- [x] 用户中心布局
- [x] API 接口封装
- [x] 状态管理配置

### 待实现的功能（Issues）

以下页面框架已搭建，需要实现具体业务逻辑：

- [ ] **首页车票查询** - 完善站点选择、日期验证
- [ ] **车次列表页** - 实现车次展示、筛选、排序
- [ ] **订单填写页** - 乘客选择、座位选择、价格计算
- [ ] **订单详情页** - 展示订单信息、支付、取消、退票
- [ ] **个人信息页** - 展示和编辑个人信息
- [ ] **乘客管理页** - 添加、编辑、删除乘客
- [ ] **订单管理页** - 订单列表、状态筛选

## 环境变量

开发环境和生产环境使用不同的环境变量文件：

- `.env.development` - 开发环境
- `.env.production` - 生产环境

变量说明：

```bash
VITE_API_BASE_URL=http://localhost:8000/api  # API 基础 URL
VITE_APP_TITLE=中国铁路12306                 # 应用标题
```

## 常用命令

### 基础命令

```bash
# 安装依赖（包含开发依赖）
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 代码质量和格式化

项目已配置 ESLint 和 Prettier 来确保代码质量和统一的代码风格：

```bash
# 检查并自动修复代码问题（推荐）
npm run lint

# 仅检查代码问题，不自动修复
npm run lint:check

# 格式化所有代码文件
npm run format

# 检查代码格式是否符合规范
npm run format:check
```

#### 使用场合

- **开发时**：保存文件时 IDE 会自动运行 Prettier 格式化
- **提交前**：运行 `npm run lint` 确保代码质量
- **团队协作**：统一的代码风格，减少合并冲突
- **CI/CD**：可在构建流程中运行 `npm run lint:check` 和 `npm run format:check`

#### 配置文件

- `.eslintrc.cjs` - ESLint 规则配置
- `.prettierrc` - Prettier 格式化配置

#### 代码规范

- 使用单引号
- 无分号结尾
- 2 空格缩进
- 行宽限制 100 字符
- 禁止使用 `var`，推荐使用 `const`
- 开发环境允许 `console`，生产环境警告

## 环境变量配置

项目使用环境变量来管理不同环境下的配置，支持开发、生产等多种环境。

### 环境文件

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

### 主要环境变量

| 变量名 | 说明 | 开发环境默认值 | 生产环境默认值 |
|--------|------|----------------|----------------|
| `VITE_API_BASE_URL` | API基础地址 | `http://localhost:8000/api` | `https://api.railway12306.com/api` |
| `VITE_REQUEST_TIMEOUT` | 请求超时时间(ms) | `30000` | `15000` |
| `VITE_APP_TITLE` | 应用标题 | `中国铁路12306 - 开发环境` | `中国铁路12306` |
| `VITE_DEBUG` | 调试模式 | `true` | `false` |
| `VITE_PAGE_SIZE` | 分页大小 | `20` | `20` |
| `VITE_UPLOAD_SIZE_LIMIT` | 上传文件大小限制(MB) | `10` | `5` |
| `VITE_TOKEN_EXPIRE_HOURS` | Token过期时间(小时) | `24` | `12` |

### 使用方式

```javascript
// 直接使用
const apiUrl = import.meta.env.VITE_API_BASE_URL

// 使用工具函数（推荐）
import { ENV_CONFIG, isDebug, isDev } from '@/utils/env'

const apiUrl = ENV_CONFIG.API_BASE_URL
const isDebugMode = isDebug()
```

### 测试环境变量

访问 `/env-test` 页面可以查看当前环境变量配置和测试功能。

## 注意事项

1. 组件应该尽可能可复用
2. API 请求需要做错误处理
3. 表单验证要在前后端都进行
4. 敏感操作需要二次确认
5. 使用 v-if 而不是 v-show 来控制需要权限的内容

## 开发团队协作

### Issue 创建规范

创建 Issue 时请使用以下标签：

- `feature` - 新功能
- `bug` - 问题修复
- `enhancement` - 功能增强
- `documentation` - 文档更新

### 分支管理

- `main` - 主分支，保持稳定
- `dev` - 开发分支
- `feature/xxx` - 功能分支
- `fix/xxx` - 修复分支

### 提交信息规范

```
feat: 添加用户登录功能
fix: 修复订单列表显示问题
docs: 更新 README 文档
style: 调整页面布局
refactor: 重构车次查询组件
```

## 问题排查

### 开发服务器无法启动

1. 检查 Node.js 版本（需要 16+）
2. 删除 `node_modules` 和 `package-lock.json`，重新安装
3. 检查端口 5173 是否被占用

### API 请求失败

1. 检查后端服务是否启动
2. 检查 `.env.development` 中的 API_BASE_URL
3. 查看浏览器控制台的网络请求

### 路由跳转失败

1. 检查路由配置是否正确
2. 检查是否需要登录（查看路由守卫）
3. 检查组件路径是否正确

## 参考资源

- [Vue 3 文档](https://cn.vuejs.org/)
- [Vite 文档](https://cn.vitejs.dev/)
- [Ant Design Vue 文档](https://antdv.com/)
- [Vue Router 文档](https://router.vuejs.org/zh/)
- [Pinia 文档](https://pinia.vuejs.org/zh/)

## 联系方式

如有问题，请提交 Issue 或联系团队成员。

