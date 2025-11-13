# Railway 12306 Backend

基于 FastAPI + PostgreSQL 的铁路12306后端服务

## 技术栈

- **Python 3.10+**
- **FastAPI 0.109+** - 高性能Web框架
- **SQLAlchemy 2.0+** - ORM框架
- **PostgreSQL** - 数据库
- **Alembic** - 数据库迁移工具
- **JWT** - 身份认证
- **Pydantic** - 数据验证

## 项目结构

```
backend/
├── app/
│   ├── api/                # API路由
│   │   └── v1/
│   │       ├── endpoints/  # 各模块端点
│   │       └── router.py   # 路由汇总
│   ├── core/               # 核心配置
│   │   ├── config.py       # 应用配置
│   │   └── security.py     # 安全相关
│   ├── db/                 # 数据库
│   │   ├── base.py         # 模型汇总
│   │   ├── session.py      # 会话管理
│   │   └── init_db.py      # 数据库初始化
│   ├── models/             # 数据库模型
│   │   ├── user.py
│   │   ├── passenger.py
│   │   ├── station.py
│   │   ├── train.py
│   │   ├── seat.py
│   │   └── order.py
│   ├── schemas/            # Pydantic模型
│   │   ├── user.py
│   │   ├── passenger.py
│   │   ├── train.py
│   │   ├── order.py
│   │   └── common.py
│   └── main.py             # 应用入口
├── alembic/                # 数据库迁移
├── requirements.txt        # 依赖包
├── .env.example            # 环境变量示例
└── README.md
```

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.10+
- PostgreSQL 12+

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
.env
# 编辑 .env 文件，配置数据库连接等信息
```

### 4. 创建数据库

```bash
# 连接到PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE railway12606;
CREATE USER railway_user WITH PASSWORD 'railway_password';
GRANT ALL PRIVILEGES ON DATABASE railway12606 TO railway_user;
```

### 5. 运行数据库迁移

```bash
# 初始化Alembic（仅首次）
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 6. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

访问 http://localhost:8000/api/docs 查看API文档

## API文档

启动服务后，访问以下地址查看交互式API文档：

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API模块

### 认证模块 (`/api/auth`)
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `POST /logout` - 退出登录

### 用户模块 (`/api/user`)
- `GET /profile` - 获取个人信息
- `PUT /profile` - 更新个人信息

### 乘客管理 (`/api/passengers`)
- `GET /` - 获取乘客列表
- `POST /` - 添加乘客
- `PUT /{passenger_id}` - 编辑乘客
- `DELETE /{passenger_id}` - 删除乘客

### 车次查询 (`/api/trains`)
- `GET /search` - 查询车次（支持筛选与排序：`train_type`、`min_departure_time`、`max_departure_time`、`min_duration_minutes`、`max_duration_minutes`、`max_price`、`sort_by`、`sort_order`）
- `GET /{train_number}` - 车次详情
- `GET /{train_number}/availability` - 指定日期余票与价格

### 订单管理 (`/api/orders`)
- `POST /create` - 创建订单
- `GET /` - 订单列表
- `GET /{order_id}` - 订单详情
- `POST /{order_id}/pay` - 支付订单
- `POST /{order_id}/cancel` - 取消订单
- `POST /{order_id}/refund` - 退票

## 开发指南

### 数据库迁移

```bash
# 创建新的迁移
alembic revision --autogenerate -m "Description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history
```

### 添加新的API端点

1. 在 `app/models/` 中定义数据库模型（如需要）
2. 在 `app/schemas/` 中定义Pydantic模型
3. 在 `app/api/v1/endpoints/` 中创建路由文件
4. 在 `app/api/v1/router.py` 中注册路由

### 代码规范

- 遵循 PEP 8 代码风格
- 使用类型提示
- 编写清晰的文档字符串
- 添加适当的注释

## 待实现功能（Issues）

以下功能已搭建好框架，需要实现具体业务逻辑：

- [x] 车次查询功能实现（含筛选与排序）
- [x] 余票独立接口
- [ ] 订单创建逻辑（座位锁定、价格计算）
- [ ] 订单支付逻辑
- [ ] 订单取消逻辑
- [ ] 退票逻辑
- [ ] 订单超时自动取消（定时任务）
- [x] 数据生成脚本（车站、车次、座位）
- [ ] 验证码生成
- [ ] 单元测试

### 演示数据

运行脚本快速生成演示数据用于联调：

```bash
cd backend
source .venv/bin/activate
python scripts/generate_demo_data.py --days 14
```


## 注意事项

1. 开发环境使用 SQLite 或 PostgreSQL
2. 所有密码使用 bcrypt 加密
3. JWT Token 默认7天有效期
4. 订单创建后座位锁定45分钟
5. 退票手续费按规则计算

## 故障排除

### 数据库连接失败

检查 `.env` 文件中的数据库配置是否正确

### 迁移失败

```bash
# 清除所有迁移并重新开始
alembic downgrade base
alembic upgrade head
```

