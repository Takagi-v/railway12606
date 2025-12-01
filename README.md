# 铁路12306 课程项目

这是一个模仿铁路12306官方网站的课程项目，实现了火车票查询、预订等核心功能。

## 项目概述

- **项目名称**: Railway 12306 Train Ticket Booking System
- **技术栈**: Vue 3 + FastAPI + PostgreSQL
- **开发模式**: 前后端分离
- **参考网站**: https://www.12306.cn/

## 技术栈

### 前端
- Vue 3.4+ (Composition API)
- Vite 5.x
- Vue Router 4.x
- Pinia 2.x
- Ant Design Vue 4.x
- Axios

### 后端
- Python 3.10+
- FastAPI 0.109+
- SQLAlchemy 2.0+
- PostgreSQL
- Alembic (数据库迁移)
- JWT (身份认证)

## 项目结构

```
railway12606/
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── api/          # API接口
│   │   ├── components/   # 公共组件
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # 状态管理
│   │   ├── views/        # 页面组件
│   │   └── main.js       # 入口文件
│   ├── package.json
│   └── README.md
│
├── backend/               # 后端项目
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 数据库
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic模型
│   │   └── main.py       # 入口文件
│   ├── alembic/          # 数据库迁移
│   ├── requirements.txt
│   └── README.md
│
├── requirement.md         # 需求文档
└── README.md             # 项目说明
```

## 核心功能模块

### 1. 用户认证
- ✅ 用户注册（框架已完成，待完善验证）
- ✅ 用户登录（框架已完成）
- ✅ JWT Token认证
- ✅ 退出登录

### 2. 车票查询
- ✅ 查询界面（已完成）
- ⏳ 车次查询逻辑（待实现）
- ⏳ 车次筛选功能（待实现）
- ⏳ 余票查询（待实现）

### 3. 订单管理
- ⏳ 创建订单（框架已完成，待实现逻辑）
- ⏳ 订单支付（简化实现）
- ⏳ 订单取消
- ⏳ 订单退票
- ⏳ 订单列表查询

### 4. 乘客管理
- ✅ 乘客列表（API已完成）
- ✅ 添加乘客（API已完成）
- ✅ 编辑乘客（API已完成）
- ✅ 删除乘客（API已完成）
- ⏳ 前端页面实现（待实现）

### 5. 个人信息管理
- ✅ 查看个人信息（API已完成）
- ✅ 编辑个人信息（API已完成）
- ⏳ 前端页面实现（待实现）

## 快速开始

### 环境要求

- Node.js 16+
- Python 3.10+
- PostgreSQL 12+

### 1. 克隆项目

```bash
git clone <repository-url>
cd railway12606
```

### 2. 启动后端

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接

# 创建数据库
# 参考 backend/README.md

# 运行数据库迁移
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

后端服务运行在 http://localhost:8000  
API文档: http://localhost:8000/api/docs

### 3. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用运行在 http://localhost:5173

## 开发指南

### 数据库设计

数据库包含以下主要表：

- `users` - 用户表
- `passengers` - 乘客表
- `stations` - 车站表
- `trains` - 车次表
- `seats` - 座位表
- `orders` - 订单表
- `order_passengers` - 订单乘客关联表

详细设计请参考 `requirement.md`

### API 接口

#### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 退出登录

#### 用户相关
- `GET /api/user/profile` - 获取个人信息
- `PUT /api/user/profile` - 更新个人信息

#### 乘客管理
- `GET /api/passengers` - 获取乘客列表
- `POST /api/passengers` - 添加乘客
- `PUT /api/passengers/{id}` - 编辑乘客
- `DELETE /api/passengers/{id}` - 删除乘客

#### 车次查询
- `GET /api/trains/search` - 查询车次

#### 订单管理
- `POST /api/orders/create` - 创建订单
- `GET /api/orders` - 订单列表
- `GET /api/orders/{id}` - 订单详情
- `POST /api/orders/{id}/pay` - 支付订单
- `POST /api/orders/{id}/cancel` - 取消订单
- `POST /api/orders/{id}/refund` - 退票

完整API文档请访问: http://localhost:8000/api/docs

### 团队协作

#### Issue 管理

项目已搭建好基础框架，以下功能待团队成员领取实现：

**前端 Issues:**
1. 车次列表页 - 展示查询结果、筛选、排序功能
2. 订单填写页 - 乘客选择、席别选择、价格计算
3. 订单详情页 - 订单信息展示、支付、取消、退票
4. 乘客管理页 - 完整的CRUD界面
5. 个人信息页 - 信息展示和编辑
6. 订单管理页 - 订单列表、状态筛选

**后端 Issues:**
1. 车次查询逻辑 - 根据出发地、目的地、日期查询车次
2. 余票计算 - 实时计算各席别余票数量
3. 订单创建逻辑 - 座位锁定、价格计算、订单生成
4. 支付功能 - 简化支付实现
5. 退票逻辑 - 手续费计算、座位释放
6. 订单超时处理 - 定时任务自动取消超时订单
7. 数据生成脚本 - 生成车站、车次、座位数据

**数据库 Issues:**
1. 初始数据生成 - 车站数据、车次数据
2. 测试数据准备 - 用于开发测试的完整数据集

#### 分支管理

- `main` - 主分支（稳定版本）
- `dev` - 开发分支
- `feature/<功能名>` - 功能分支
- `fix/<问题描述>` - 修复分支

#### 提交规范

```
feat: 添加xxx功能
fix: 修复xxx问题
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
```

## 测试账号

开发测试时可以使用以下账号（需先运行后端并注册）：

```
用户名: testuser
密码: Test123456
```

## 注意事项

1. **安全性**: 
   - 生产环境需修改 `.env` 中的 SECRET_KEY
   - 不要将 `.env` 文件提交到版本控制

2. **数据库**:
   - 首次运行需要创建数据库和运行迁移
   - 修改模型后需要创建新的迁移文件

3. **跨域**:
   - 开发环境前端通过 Vite 代理解决跨域
   - 生产环境需要配置 CORS

4. **仅考虑单程、普通票**:
   - 不实现往返票、联程票
   - 不实现学生优惠、儿童票优惠计算逻辑

## 文档

- [需求文档](./requirement.md) - 详细的功能需求和设计
- [后端文档](./backend/README.md) - 后端开发指南
- [前端文档](./frontend/README.md) - 前端开发指南

## 开发进度

- [x] 项目框架搭建
- [x] 数据库模型设计
- [x] 后端API基础框架
- [x] 前端页面基础框架
- [x] 用户认证功能（登录/注册）
- [x] API接口封装
- [ ] 车次查询功能
- [ ] 订单创建功能
- [ ] 乘客管理页面
- [ ] 订单管理页面
- [ ] 个人信息页面
- [ ] 数据生成脚本
- [ ] 完整测试

## 常见问题

### Q: 后端启动失败？
A: 检查 PostgreSQL 是否运行，`.env` 配置是否正确，依赖是否安装完整。

### Q: 前端无法访问后端API？
A: 检查后端是否启动，CORS 配置是否正确，`.env.development` 中的 API_BASE_URL 是否正确。

### Q: 数据库迁移失败？
A: 检查数据库连接，删除 `alembic/versions/` 中的迁移文件后重新生成。

### Q: 如何添加测试数据？
A: 可以手动在数据库中插入，或编写数据生成脚本（待实现）。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目仅用于课程学习，不得用于商业用途。

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。


Try trivial update.
