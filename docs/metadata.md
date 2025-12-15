# Railway 12306 项目元数据 (Metadata)

> **本文档是项目的唯一真理来源（Single Source of Truth）。**  
> 所有的代码生成、接口设计和文件结构必须严格遵守本文档定义的规范。  
> AI 在生成代码时，必须以本文档为最高优先级的约束规范。

**文档版本**: v1.0  
**创建日期**: 2025-12-15  
**项目名称**: Railway 12306 仿站项目  

---

## 1. 项目概述 (Project Overview)

这是一个模仿中国铁路12306官方网站的软件工程课程大作业项目。核心目标是实现火车票查询、预订、订单管理等核心功能。

### 1.1 核心功能模块
| 模块 | 功能描述 |
|------|----------|
| 用户认证 | 注册、登录、退出、找回密码 |
| 车票查询 | 单程/往返查询、筛选排序、余票显示 |
| 订单管理 | 创建订单、支付（模拟）、取消、退票 |
| 乘客管理 | 增删改查常用乘客 |
| 个人中心 | 个人信息查看与编辑 |
| 管理后台 | 用户管理、角色权限管理（RBAC） |

### 1.2 项目约束
- 仅考虑**单程/往返、普通票**
- 支付功能简化为"一键支付"模拟弹窗
- 车次数据可程序生成或使用脚本批量导入
- 需实现完整的**RBAC权限控制**

---

## 2. 技术栈约束 (Tech Stack Constraints)

必须严格使用以下技术栈，不得使用其他框架或依赖替代：

### 2.1 前端 (Frontend)

| 类别 | 技术选型 | 版本要求 |
|------|----------|----------|
| 核心框架 | Vue.js | ^3.4.x (Composition API, `<script setup>`) |
| 构建工具 | Vite | ^5.0.x |
| 路由管理 | Vue Router | ^4.2.x |
| 状态管理 | Pinia | ^3.0.x |
| 状态持久化 | pinia-plugin-persistedstate | ^4.x |
| UI 组件库 | Ant Design Vue | ^4.1.x |
| HTTP 客户端 | Axios | ^1.6.x |
| 日期处理 | Day.js | ^1.11.x |
| Cookie 管理 | js-cookie | ^3.0.x |
| 工具函数 | @vueuse/core | ^10.x |
| 代码检查 | ESLint | ^8.x |
| 代码格式化 | Prettier | ^3.x |

### 2.2 后端 (Backend)

| 类别 | 技术选型 | 版本要求 |
|------|----------|----------|
| 语言 | Python | ^3.10+ |
| Web 框架 | FastAPI | ^0.115.x |
| ASGI 服务器 | Uvicorn (with standard extras) | ^0.32.x |
| ORM | SQLAlchemy | ^2.0.x |
| 数据库 | PostgreSQL | ^14+ |
| 数据库驱动 | psycopg2-binary | ^2.9.x |
| 数据库迁移 | Alembic | ^1.14.x |
| 数据验证 | Pydantic | ^2.10.x |
| 环境配置 | pydantic-settings | ^2.7.x |
| JWT 认证 | python-jose[cryptography] | ^3.3.x |
| 密码加密 | passlib[bcrypt] | ^1.7.x |
| 环境变量 | python-dotenv | ^1.0.x |
| 日志 | loguru | ^0.7.x |
| 文件上传 | python-multipart | ^0.0.x |
| 邮箱验证 | email-validator | ^2.2.x |

---

## 3. 项目目录结构规范 (Directory Structure)

在生成文件时，必须**严格遵循**此树状结构。禁止创建未定义的顶级目录。

```text
/railway12606                          # 项目根目录
├── README.md                          # 项目说明文档
├── CONTRIBUTING.md                    # 贡献者指南
├── .gitignore                         # Git 忽略规则
├── .github/                           # GitHub 工作流配置
│   └── ...
│
├── docs/                              # 文档目录
│   ├── requirement.md                 # 需求文档
│   └── metadata.md                    # 本元数据文档
│
├── backend/                           # 后端 FastAPI 项目
│   ├── .env                           # 环境变量（不入库）
│   ├── .env.example                   # 环境变量模板
│   ├── .env.test                      # 测试环境变量
│   ├── .gitignore
│   ├── requirements.txt               # Python 依赖列表
│   ├── alembic.ini                    # Alembic 配置文件
│   ├── run.sh                         # Mac/Linux 启动脚本
│   ├── run_windows.bat                # Windows 启动脚本
│   │
│   ├── alembic/                       # 数据库迁移目录
│   │   ├── versions/                  # 迁移脚本
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── README
│   │
│   ├── app/                           # 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI 入口文件
│   │   │
│   │   ├── api/                       # API 层
│   │   │   ├── __init__.py
│   │   │   ├── deps.py                # 依赖注入（获取当前用户等）
│   │   │   └── v1/                    # API 版本 v1
│   │   │       ├── __init__.py
│   │   │       ├── router.py          # 路由聚合
│   │   │       └── endpoints/         # 各业务端点
│   │   │           ├── __init__.py
│   │   │           ├── auth.py        # 认证端点
│   │   │           ├── users.py       # 用户端点
│   │   │           ├── passengers.py  # 乘客端点
│   │   │           ├── trains.py      # 车次端点
│   │   │           ├── orders.py      # 订单端点
│   │   │           ├── admin.py       # 管理员端点
│   │   │           ├── roles.py       # 角色管理端点
│   │   │           ├── permissions.py # 权限管理端点
│   │   │           ├── user_roles.py  # 用户角色分配端点
│   │   │           └── password_recovery.py  # 找回密码端点
│   │   │
│   │   ├── core/                      # 核心配置层
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # 应用配置 (Settings)
│   │   │   ├── security.py            # 安全工具 (JWT, 密码)
│   │   │   ├── exceptions.py          # 自定义异常
│   │   │   ├── middleware.py          # 中间件
│   │   │   ├── permissions.py         # 权限检查逻辑
│   │   │   ├── init_rbac.py           # RBAC 初始化
│   │   │   └── validators.py          # 自定义验证器
│   │   │
│   │   ├── db/                        # 数据库层
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Base 类导入
│   │   │   ├── base_class.py          # 声明性基类
│   │   │   ├── session.py             # 数据库会话
│   │   │   └── init_db.py             # 数据库初始化
│   │   │
│   │   ├── models/                    # SQLAlchemy 数据模型
│   │   │   ├── __init__.py            # 模型导出
│   │   │   ├── user.py                # 用户模型
│   │   │   ├── passenger.py           # 乘客模型
│   │   │   ├── station.py             # 车站模型
│   │   │   ├── train.py               # 车次模型
│   │   │   ├── seat.py                # 座位模型
│   │   │   ├── order.py               # 订单模型
│   │   │   ├── role.py                # 角色模型
│   │   │   └── enums.py               # 枚举定义
│   │   │
│   │   └── schemas/                   # Pydantic 验证模型
│   │       ├── __init__.py
│   │       ├── common.py              # 公共响应模式
│   │       ├── user.py                # 用户模式
│   │       ├── passenger.py           # 乘客模式
│   │       ├── train.py               # 车次模式
│   │       ├── order.py               # 订单模式
│   │       ├── role.py                # 角色模式
│   │       └── password_recovery.py   # 找回密码模式
│   │
│   ├── scripts/                       # 实用脚本
│   │   ├── generate_demo_data.py      # 生成测试数据
│   │   └── ...
│   │
│   └── tests/                         # 测试目录
│       ├── conftest.py                # pytest 配置
│       ├── unit/                      # 单元测试
│       ├── integration/               # 集成测试
│       └── test_*.py                  # 测试文件
│
├── frontend/                          # 前端 Vue 项目
│   ├── .env.development               # 开发环境变量
│   ├── .env.production                # 生产环境变量
│   ├── .eslintrc.cjs                  # ESLint 配置
│   ├── .prettierrc                    # Prettier 配置
│   ├── .gitignore
│   ├── index.html                     # HTML 入口
│   ├── package.json                   # NPM 依赖配置
│   ├── vite.config.js                 # Vite 配置
│   │
│   ├── public/                        # 静态资源
│   │   └── ...
│   │
│   └── src/                           # 源代码
│       ├── App.vue                    # 根组件
│       ├── main.js                    # 应用入口
│       │
│       ├── api/                       # API 封装
│       │   ├── auth.js                # 认证 API
│       │   ├── order.js               # 订单 API
│       │   ├── passenger.js           # 乘客 API
│       │   ├── train.js               # 车次 API
│       │   └── permission.js          # 权限 API
│       │
│       ├── assets/                    # 静态资源（图片、字体）
│       │   └── ...
│       │
│       ├── components/                # 公共组件
│       │   ├── AppHeader.vue          # 应用头部
│       │   ├── AppFooter.vue          # 应用底部
│       │   ├── Header12306.vue        # 12306 风格头部
│       │   ├── CitySelector.vue       # 城市选择器
│       │   ├── DateSelector.vue       # 日期选择器
│       │   ├── Loading.vue            # 加载状态
│       │   ├── Empty.vue              # 空状态
│       │   ├── Permission/            # 权限相关组件
│       │   │   └── ...
│       │   ├── form/                  # 表单组件
│       │   │   └── ...
│       │   └── ...                    # 其他组件
│       │
│       ├── config/                    # 应用配置
│       │   └── ...
│       │
│       ├── directives/                # 自定义指令
│       │   └── ...
│       │
│       ├── router/                    # 路由配置
│       │   ├── index.js               # 路由定义
│       │   └── guards.js              # 路由守卫
│       │
│       ├── stores/                    # Pinia 状态管理
│       │   ├── user.js                # 用户状态
│       │   └── permission.js          # 权限状态
│       │
│       ├── styles/                    # 全局样式
│       │   └── ...
│       │
│       ├── utils/                     # 工具函数
│       │   ├── request.js             # Axios 请求封装
│       │   ├── formRules.js           # 表单验证规则
│       │   ├── cityData.js            # 城市数据
│       │   ├── env.js                 # 环境变量工具
│       │   └── permission.js          # 权限工具函数
│       │
│       └── views/                     # 页面视图
│           ├── HomePage.vue           # 首页
│           ├── NotFound.vue           # 404 页面
│           │
│           ├── auth/                  # 认证相关页面
│           │   ├── LoginPage.vue          # 登录
│           │   ├── RegisterPage.vue       # 注册
│           │   ├── ForgotPasswordPage.vue # 找回密码
│           │   ├── VerifyCodePage.vue     # 验证码验证
│           │   ├── NewPasswordPage.vue    # 设置新密码
│           │   └── DonePage.vue           # 完成页
│           │
│           ├── ticket/                # 车票相关页面
│           │   ├── LeftTicketSingle.vue   # 单程查询
│           │   ├── LeftTicketRound.vue    # 往返查询
│           │   ├── SchedulePage.vue       # 时刻表
│           │   └── WaitingListPage.vue    # 候补
│           │
│           ├── order/                 # 订单相关页面
│           │   ├── OrderConfirm.vue       # 确认订单
│           │   ├── OrderCreate.vue        # 创建订单
│           │   ├── OrderDetail.vue        # 订单详情
│           │   ├── OrderSuccess.vue       # 支付成功
│           │   └── OrderInquiry.vue       # 订单查询
│           │
│           ├── user/                  # 个人中心页面
│           │   ├── UserLayout.vue         # 用户中心布局
│           │   ├── ProfilePage.vue        # 个人信息
│           │   ├── PassengerPage.vue      # 乘客管理
│           │   └── OrderPage.vue          # 订单管理
│           │
│           ├── admin/                 # 管理后台页面
│           │   ├── AdminLayout.vue        # 管理布局
│           │   ├── Dashboard.vue          # 仪表盘
│           │   ├── UserManagement.vue     # 用户管理
│           │   ├── RoleManagement.vue     # 角色管理
│           │   ├── PermissionManagement.vue # 权限管理
│           │   ├── TrainManagement.vue    # 车次管理
│           │   ├── OrderManagement.vue    # 订单管理
│           │   └── SystemSettings.vue     # 系统设置
│           │
│           ├── service/               # 服务功能页面
│           │   └── ...                    # 各服务页面
│           │
│           ├── info/                  # 信息页面
│           │   ├── AnnouncementPage.vue   # 公告
│           │   ├── FAQPage.vue            # 常见问题
│           │   └── CreditPage.vue         # 信用信息
│           │
│           ├── train/                 # 车次列表
│           │   └── TrainList.vue
│           │
│           └── test/                  # 测试/演示页面
│               └── ...
```

---

## 4. API 接口规范 (API Specification)

### 4.1 API 前缀与版本
- **API 前缀**: `/api`
- **当前版本**: v1（隐式，可扩展为显式版本 `/api/v1`）

### 4.2 API 路由映射表

| 路由前缀 | 端点文件 | 功能描述 |
|----------|----------|----------|
| `/api/auth` | auth.py | 认证（登录、注册、验证码、退出） |
| `/api/user` | users.py | 用户个人信息管理 |
| `/api/passengers` | passengers.py | 乘客 CRUD |
| `/api/trains` | trains.py | 车次查询、余票查询 |
| `/api/orders` | orders.py | 订单创建、支付、取消、退票 |
| `/api/admin` | admin.py | 管理员功能 |
| `/api/roles` | roles.py | 角色管理 |
| `/api/permissions` | permissions.py | 权限管理 |
| `/api/user-roles` | user_roles.py | 用户角色分配 |
| `/api/password-recovery/*` | password_recovery.py | 找回密码流程 |

### 4.3 响应格式规范

所有 API 响应必须遵循以下统一格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

**错误响应**：
```json
{
  "code": 40001,
  "message": "具体错误信息",
  "data": null
}
```

### 4.4 HTTP 状态码规范
| 状态码 | 含义 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 过期 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 5. 数据库模型规范 (Database Model)

### 5.1 核心数据表

| 表名 | 模型文件 | 说明 |
|------|----------|------|
| `users` | user.py | 用户表 |
| `passengers` | passenger.py | 乘客表 |
| `stations` | station.py | 车站表 |
| `trains` | train.py | 车次表 |
| `seats` | seat.py | 座位表（每日生成） |
| `orders` | order.py | 订单表 |
| `order_passengers` | order.py | 订单乘客关联表 |
| `roles` | role.py | 角色表 |
| `permissions` | role.py | 权限表 |
| `role_permissions` | role.py | 角色权限关联表 |
| `user_roles` | role.py | 用户角色关联表 |

### 5.2 关键枚举定义 (enums.py)

```python
# 订单状态
class OrderStatus(str, Enum):
    PENDING = "pending"           # 待支付
    PAID = "paid"                 # 已支付
    CANCELLED = "cancelled"       # 已取消
    REFUNDED = "refunded"         # 已退票
    PARTIAL_REFUNDED = "partial_refunded"  # 部分退票
    COMPLETED = "completed"       # 已完成

# 座位类型
class SeatType(str, Enum):
    FIRST_CLASS = "first_class"       # 一等座
    SECOND_CLASS = "second_class"     # 二等座
    SOFT_SLEEPER = "soft_sleeper"     # 软卧
    HARD_SLEEPER = "hard_sleeper"     # 硬卧

# 车次类型
class TrainType(str, Enum):
    G = "G"  # 高铁
    D = "D"  # 动车
    Z = "Z"  # 直达
```

---

## 6. 前端路由规范 (Frontend Routes)

### 6.1 路由权限控制
| 路由标记 | 说明 |
|----------|------|
| `requiresAuth: true` | 需要登录 |
| `roles: ['admin', 'super_admin']` | 需要指定角色 |
| `permissions: 'user:read'` | 需要指定权限 |

### 6.2 核心路由表

| 路径 | 组件 | 访问权限 |
|------|------|----------|
| `/` | HomePage.vue | 公开 |
| `/login` | LoginPage.vue | 公开 |
| `/register` | RegisterPage.vue | 公开 |
| `/forgot-password/*` | 找回密码流程 | 公开 |
| `/leftTicket/single` | LeftTicketSingle.vue | 公开 |
| `/leftTicket/round` | LeftTicketRound.vue | 公开 |
| `/order/confirm` | OrderConfirm.vue | 需登录 |
| `/order/:orderId` | OrderDetail.vue | 需登录 |
| `/user/*` | 个人中心子页面 | 需登录 |
| `/admin/*` | 管理后台子页面 | 需 admin 角色 |

---

## 7. 认证与权限规范 (Auth & RBAC)

### 7.1 认证机制
- 使用 **JWT Token** 进行身份验证
- Token 存储在前端 Cookie（`js-cookie`）
- Token 过期时间：7 天（`ACCESS_TOKEN_EXPIRE_MINUTES = 10080`）

### 7.2 RBAC 权限模型
```
用户 (User) ──┬── 角色 (Role) ──┬── 权限 (Permission)
              └── 多对多       └── 多对多
```

### 7.3 内置角色
| 角色代码 | 角色名 | 权限范围 |
|----------|--------|----------|
| `user` | 普通用户 | 查询车次、购票、管理自己的乘客和订单 |
| `admin` | 管理员 | 管理用户、车次、订单 |
| `super_admin` | 超级管理员 | 所有权限 + 系统设置 |

---

## 8. 表单验证规范 (Validation Rules)

### 8.1 前端验证规则（formRules.js）

| 字段 | 规则 | 错误提示 |
|------|------|----------|
| 用户名 | 6-30 位，仅字母数字 | 用户名为6-30位字母或数字 |
| 密码 | 6-20 位，必须包含字母和数字 | 密码需6-20位，且包含字母和数字 |
| 真实姓名 | 2-10 个中文字符 | 请输入正确的姓名 |
| 身份证号 | 18 位，符合身份证规则 | 请输入正确的身份证号码 |
| 手机号 | 11 位数字，1 开头 | 请输入正确的手机号 |
| 邮箱 | 标准邮箱格式 | 请输入正确的邮箱地址 |

### 8.2 后端验证
- 使用 Pydantic 模型进行数据验证
- 自定义验证器位于 `validators.py`

---

## 9. 状态管理规范 (State Management)

### 9.1 Pinia Stores

| Store 文件 | 状态内容 |
|------------|----------|
| `user.js` | 用户信息、登录状态、Token |
| `permission.js` | 用户权限、角色列表 |

### 9.2 状态持久化
使用 `pinia-plugin-persistedstate` 持久化以下状态：
- 用户 Token
- 用户基本信息
- 权限和角色

---

## 10. 代码规范 (Code Style)

### 10.1 前端规范
- **Vue 组件**：使用 `<script setup>` 语法
- **命名规范**：
  - 组件文件：PascalCase（如 `UserProfile.vue`）
  - 页面组件后缀：`*Page.vue`（如 `LoginPage.vue`）
  - 布局组件后缀：`*Layout.vue`
- **代码格式**：使用 Prettier + ESLint

### 10.2 后端规范
- **模块命名**：snake_case
- **类命名**：PascalCase
- **函数命名**：snake_case
- **常量命名**：UPPER_SNAKE_CASE
- **文档字符串**：必须为每个模块、类、函数编写 docstring

---

## 11. 运行与部署约束 (Run & Deploy)

### 11.1 开发环境启动

**后端**：
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端**：
```bash
cd frontend
npm install
npm run dev
```

### 11.2 端口规范
| 服务 | 端口 |
|------|------|
| 前端开发服务 | 5173 |
| 后端 API 服务 | 8000 |
| PostgreSQL | 5432 |

### 11.3 API 代理配置
前端通过 Vite dev server 代理 `/api` 请求到后端：
```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

---

## 12. 测试规范 (Testing)

### 12.1 后端测试
- **测试框架**：pytest
- **HTTP 测试**：使用 pytest + httpx 或直接 TestClient
- **测试目录**：`backend/tests/`
- **命令**：`pytest` 或 `python -m pytest`

### 12.2 前端测试（可选）
- 可使用 Vitest 配合 @testing-library/vue
- 测试目录：`frontend/tests/`

---

## 13. 注意事项 (Notes)

### 13.1 AI 代码生成约束
1. 生成代码前，必须先阅读 `metadata.md` 和 `requirement.md`
2. 必须严格遵循本文档定义的技术栈，不得引入未定义的依赖
3. 目录结构必须与第 3 节规范完全一致
4. API 响应格式必须遵循第 4.3 节规范
5. 数据模型必须使用 SQLAlchemy 2.0 风格
6. 前端必须使用 Vue 3 Composition API + `<script setup>`

### 13.2 禁止事项
- ❌ 不得使用 React、Angular 等非 Vue 框架
- ❌ 不得使用 Express.js、Django 等非 FastAPI 框架
- ❌ 不得使用 MySQL/SQLite 替代 PostgreSQL
- ❌ 不得使用 Vuex 替代 Pinia
- ❌ 不得使用 Element Plus 替代 Ant Design Vue

---

**文档结束**

此元数据文档定义了 Railway 12306 项目的所有技术规范和约束条件。  
AI 在生成任何代码时，必须将本文档作为唯一的技术真理来源。
