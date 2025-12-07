# Railway 12306 仿站项目

这是一个模仿铁路12306官方网站的课程项目，旨在实现火车票查询、预订、订单管理等核心功能。系统采用前后端分离架构，前端使用 Vue 3，后端使用 FastAPI + PostgreSQL。

## 📚 项目概述

- **项目名称**: Railway 12306 Train Ticket Booking System
- **核心功能**: 车票查询、座位预订、订单管理、乘客管理、用户认证
- **参考网站**: [中国铁路12306](https://www.12306.cn/)

## 🛠 技术栈

### 前端 (Frontend)
- **核心框架**: Vue 3.4+ (Composition API)
- **构建工具**: Vite 5.x
- **路由管理**: Vue Router 4.x
- **状态管理**: Pinia 2.x
- **UI 组件库**: Ant Design Vue 4.x
- **HTTP 客户端**: Axios

### 后端 (Backend)
- **Web 框架**: FastAPI 0.109+
- **语言**: Python 3.10+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: PostgreSQL 16+
- **迁移工具**: Alembic
- **认证**: JWT (JSON Web Tokens)

## 📂 项目结构

```
railway12606/
├── frontend/              # 前端 Vue 项目
│   ├── src/
│   │   ├── api/          # API 接口定义
│   │   ├── components/   # 公共组件
│   │   ├── views/        # 页面视图
│   │   └── ...
│   └── ...
│
├── backend/               # 后端 FastAPI 项目
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置 (Config, Security)
│   │   ├── db/           # 数据库连接与会话
│   │   ├── models/       # SQLAlchemy 数据模型
│   │   └── schemas/      # Pydantic 数据验证模型
│   ├── alembic/          # 数据库迁移脚本
│   ├── scripts/          # 实用脚本 (数据生成等)
│   └── ...
├── CONTRIBUTING.md       # 贡献者指南
├── README.md             # 项目说明文档
```

## 🚀 部署与启动 (Deployment)

以下是针对 macOS/Linux 环境的标准部署流程。并且针对Windows环境下的特殊步骤进行了说明。

### 一、后端部署 (Normal Flow)

#### 1. 环境准备
确保已安装 Python 3.10+, PostgreSQL 14+, Node.js 18+。

#### 2. 数据库配置
首先创建数据库和用户。登录 PostgreSQL：

```bash
psql postgres
```

Windows 用户（推荐显式指定连接参数与超级用户，防止出现默认用操作系统用户名尝试作为数据库用户名登录，而如果该数据库角色不存在或没有密码引起失败的问题）：

```powershell
psql -h localhost -p 5432 -U postgres -d postgres
```

执行以下 SQL 语句：

```sql
CREATE USER railway_user WITH PASSWORD 'railway_password';
CREATE DATABASE railway12606 OWNER railway_user;
GRANT ALL PRIVILEGES ON DATABASE railway12606 TO railway_user;
\q
```

#### 3. 后端启动

```bash
cd backend

# 1. 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env

# 4. 执行数据库迁移
alembic upgrade head

# 5. 生成测试数据 (可选)
python scripts/generate_demo_data.py --days 14

# 6. 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Windows 用户部署注意

- 激活虚拟环境（PowerShell）：

```powershell
.\.venv\Scripts\Activate.ps1
```

- 如使用 `venv` 安装依赖出现问题，推荐使用 Conda 环境：

```powershell
conda create -n railway12606 python=3.11 -y
conda activate railway12606
pip install --upgrade pip
pip install -r requirements.txt
```

- 其余流程与 mac/linux 保持一致。

- API 文档地址: http://localhost:8000/api/docs

---

### 二、前端部署

新建一个终端窗口：

```bash
cd frontend
npm install
npm run dev
```

- 访问地址: http://localhost:5173

---


## 🔒 数据库权限问题排查指南 (Troubleshooting Database Permissions)

如果在部署过程中遇到数据库相关的 `Permission denied` 错误（尤其是 `permission denied for schema public`），请参考本节。

### 1. 为什么会出现权限问题？

在 PostgreSQL 中，即使是数据库的所有者 (`railway_user`)，有时也默认没有 `public` 模式 (Schema) 的操作权限。如果不显式授权，后端应用在尝试创建表（运行 `alembic upgrade`）或写入数据时就会因为权限不足而报错。

### 2. 修复步骤

请按照以下步骤手动授予 Schema 权限：

```bash
psql postgres
```

在 SQL 提示符中逐行执行：

```sql
-- 1. 切换到项目数据库 (非常重要！必须先切换库)
\c railway12606

-- 2. 授予 Schema 的所有权给项目用户
GRANT ALL ON SCHEMA public TO railway_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO railway_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO railway_user;

-- 3. 退出
\q
```

## ✅ 功能开发进度

### 核心模块
- [x] **用户认证**: 注册、登录、JWT Token、退出
- [x] **个人中心**: 信息查看与编辑
- [x] **乘客管理**: 增删改查乘客信息
- [x] **车次查询**: 
  - [x] 基础查询 (出发地、目的地、日期)
  - [x] 高级筛选 (车次类型、时间段)
  - [x] 结果排序 (价格、耗时)
- [x] **余票查询**: 实时显示各席别余票

### 待开发模块 (TODO)
- [ ] **订单系统**:
  - [x] 提交订单 (锁定座位)
  - [ ] 订单支付流程 (模拟)
  - [x] 订单列表与详情
  - [x] 取消订单与退票
- [ ] **系统优化**:
  - [ ] 引入 Redis 缓存余票
  - [ ] 消息队列处理订单超时

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/NewFeature`)
3. 提交改动 (`git commit -m 'Add some NewFeature'`)
4. 推送分支 (`git push origin feature/NewFeature`)
5. 提交 Pull Request
