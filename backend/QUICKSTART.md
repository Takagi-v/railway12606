# 后端快速启动指南

## 🚀 一键启动

后端环境已完全配置好！直接运行启动脚本即可：

```bash
cd backend
./run.sh
```

脚本会自动：
- ✅ 检查并激活虚拟环境
- ✅ 检查并安装依赖
- ✅ 启动 PostgreSQL 服务（如果未运行）
- ✅ 检查数据库连接
- ✅ 运行数据库迁移
- ✅ 启动 FastAPI 服务器

## 📖 访问 API 文档

启动成功后，访问以下地址：

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## 🗄️ 数据库信息

- **数据库名**: `railway12606`
- **用户**: `railway_user`
- **密码**: `railway_password`
- **主机**: `localhost`
- **端口**: `5432`

### 连接数据库

```bash
psql -U railway_user -d railway12606
```

### 查看所有表

```sql
\dt
```

### 查看表结构

```sql
\d users
\d passengers
\d trains
\d stations
\d seats
\d orders
\d order_passengers
```

## 🛠️ 常用命令

### 停止服务

按 `Ctrl+C` 停止 FastAPI 服务器

### 停止 PostgreSQL

```bash
brew services stop postgresql@16
```

### 重启 PostgreSQL

```bash
brew services restart postgresql@16
```

### 查看 PostgreSQL 状态

```bash
brew services list | grep postgresql
```

### 创建新的数据库迁移

```bash
cd backend
source .venv/bin/activate
alembic revision --autogenerate -m "描述你的修改"
alembic upgrade head
```

### 回滚迁移

```bash
alembic downgrade -1
```

### 查看迁移历史

```bash
alembic history
```

## 📝 已创建的数据表

1. **users** - 用户表
   - 存储注册用户信息
   - 包含用户名、密码、证件信息等

2. **passengers** - 乘客表
   - 存储用户添加的乘客信息
   - 用于购票时选择乘客

3. **stations** - 车站表
   - 存储所有车站信息
   - 包含车站名称、城市、拼音等

4. **trains** - 车次表
   - 存储车次信息
   - 包含车次号、出发/到达站、时间、价格等

5. **seats** - 座位表
   - 存储每个车次每天的座位信息
   - 包含座位类型、状态、锁定时间等

6. **orders** - 订单表
   - 存储订单信息
   - 包含订单号、总价、状态等

7. **order_passengers** - 订单乘客表
   - 关联订单和乘客
   - 存储每个乘客的票价、座位等信息

## 🔧 环境配置

配置文件位于 `backend/.env`，主要配置项：

```env
# 数据库配置
DATABASE_URL=postgresql://railway_user:railway_password@localhost:5432/railway12606

# JWT 配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS 配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## ⚠️ 故障排除

### 1. 端口被占用

如果 8000 端口被占用：

```bash
lsof -ti:8000 | xargs kill -9
```

### 2. PostgreSQL 连接失败

检查 PostgreSQL 是否运行：

```bash
brew services list | grep postgresql
```

如果未运行：

```bash
brew services start postgresql@16
```

### 3. 依赖安装失败

删除虚拟环境重新创建：

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. 数据库迁移失败

重置数据库：

```bash
# 删除所有表
psql -U railway_user -d railway12606 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 重新运行迁移
alembic upgrade head
```

## 🎯 下一步

后端已完全配置好，可以开始：

1. 测试 API 接口（访问 /api/docs）
2. 实现具体的业务逻辑
3. 添加测试数据
4. 开发前端对接 API

祝开发顺利！🚀

