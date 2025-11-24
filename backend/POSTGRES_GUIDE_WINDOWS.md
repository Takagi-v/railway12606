# PostgreSQL 管理指南（Windows）

## 🚀 PostgreSQL 安装与配置

### 1. 验证 PostgreSQL 安装

首先确认 PostgreSQL 已正确安装：

```powershell
# 检查 PostgreSQL 版本
psql --version

# 检查服务状态
Get-Service postgresql*
```

如果命令无法识别，需要将 PostgreSQL 的 bin 目录添加到系统 PATH 环境变量中。

### 2. 配置环境变量

将 PostgreSQL 的 bin 目录添加到系统 PATH：

```powershell
# 临时添加（当前会话有效）
$env:PATH += ";C:\Program Files\PostgreSQL\18\bin"

# 永久添加（需要管理员权限）
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\18\bin", "Machine")
```

**或者通过系统设置：**
1. 按 `Win + R`，输入 `sysdm.cpl`，回车
2. 点击"高级"选项卡 → "环境变量"
3. 在"系统变量"中找到 `Path`，点击"编辑"
4. 点击"新建"，添加：`C:\Program Files\PostgreSQL\18\bin`
5. 点击"确定"保存

### 3. 启动 PostgreSQL 服务

```powershell
# 启动 PostgreSQL 服务
net start postgresql-x64-18

# 或者使用服务管理器
Start-Service postgresql-x64-18

# 检查服务状态
Get-Service postgresql-x64-18
```

### 4. 设置数据库用户和数据库

```powershell
# 连接到 PostgreSQL（使用默认的 postgres 用户）
psql -U postgres

# 在 psql 命令行中执行以下 SQL 命令：
```

```sql
-- 创建项目专用用户
CREATE USER railway_user WITH PASSWORD 'railway_password';

-- 创建项目数据库
CREATE DATABASE railway12606 OWNER railway_user;

-- 授予用户权限
GRANT ALL PRIVILEGES ON DATABASE railway12606 TO railway_user;

-- 退出 psql
\q
```

### 5. 测试数据库连接

```powershell
# 测试连接到项目数据库
psql -U railway_user -d railway12606 -h localhost

# 如果连接成功，会看到类似这样的提示：
# railway12606=>
```

## 🔧 项目环境配置

### 1. 创建环境变量文件

在项目的 `backend` 目录下创建 `.env` 文件：

```powershell
# 进入项目后端目录
cd "f:\CS3604 软件工程与项目管理\railway12606\backend"

# 创建 .env 文件
New-Item -Path ".env" -ItemType File
```

### 2. 配置 .env 文件

在 `.env` 文件中添加以下配置：

```env
# 数据库配置
DATABASE_URL=postgresql://railway_user:railway_password@localhost:5432/railway12606
POSTGRES_USER=railway_user
POSTGRES_PASSWORD=railway_password
POSTGRES_DB=railway12606
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT 配置
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS 配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 3. 安装 Python 依赖

```powershell
# 确保在 backend 目录下
cd "f:\CS3604 软件工程与项目管理\railway12606\backend"

# 创建虚拟环境（如果还没有）
python -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 如果执行策略限制，先运行：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 安装依赖
pip install -r requirements.txt
```

## 🗄️ 数据库初始化

### 1. 运行数据库迁移

```powershell
# 确保虚拟环境已激活
.\.venv\Scripts\Activate.ps1

# 初始化 Alembic（仅首次运行）
alembic revision --autogenerate -m "Initial migration"

# 应用迁移到数据库
alembic upgrade head
```

### 2. 验证数据库表创建

```powershell
# 连接到数据库
psql -U railway_user -d railway12606 -h localhost

# 在 psql 中查看创建的表
\dt

# 应该看到以下表：
# - users (用户表)
# - passengers (乘客表)
# - stations (车站表)
# - trains (车次表)
# - seats (座位表)
# - orders (订单表)
# - order_passengers (订单乘客表)
```

## 🚀 启动项目

### 1. 启动后端服务

```powershell
# 确保在 backend 目录下且虚拟环境已激活
cd "f:\CS3604 软件工程与项目管理\railway12606\backend"
.\.venv\Scripts\Activate.ps1

# 启动 FastAPI 服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 验证服务启动

打开浏览器访问：
- **API 文档**: http://localhost:8000/api/docs
- **健康检查**: http://localhost:8000/health

## 🛠️ 常用管理命令

### PostgreSQL 服务管理

```powershell
# 启动服务
net start postgresql-x64-18

# 停止服务
net stop postgresql-x64-18

# 重启服务
net stop postgresql-x64-18
net start postgresql-x64-18

# 查看服务状态
Get-Service postgresql-x64-18
```

### 数据库连接

```powershell
# 连接到项目数据库
psql -U railway_user -d railway12606 -h localhost

# 连接到默认数据库
psql -U postgres -h localhost
```

### 常用 psql 命令

```sql
-- 列出所有数据库
\l

-- 连接到指定数据库
\c railway12606

-- 列出当前数据库的所有表
\dt

-- 查看表结构
\d users

-- 查看表数据
SELECT * FROM users LIMIT 5;

-- 退出 psql
\q
```

### 数据库迁移管理

```powershell
# 创建新迁移（当修改模型后）
alembic revision --autogenerate -m "描述你的修改"

# 应用迁移
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

## 🔍 故障排除

### 1. PostgreSQL 服务无法启动

```powershell
# 检查服务状态
Get-Service postgresql*

# 如果服务不存在，重新安装 PostgreSQL
# 或者检查服务名称是否正确
```

### 2. psql 命令无法识别

**方法1：临时添加到PATH（当前会话有效）**
```powershell
$env:PATH += ";C:\Program Files\PostgreSQL\18\bin"
```

**方法2：永久添加到PATH**
将 PostgreSQL 的 bin 目录添加到系统 PATH：
1. 打开"系统属性" → "高级" → "环境变量"
2. 在"系统变量"中找到 PATH
3. 添加 PostgreSQL 安装目录的 bin 路径：`C:\Program Files\PostgreSQL\18\bin`

**方法3：使用完整路径**
```powershell
"C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
```

### 3. 数据库连接失败

```powershell
# 检查 PostgreSQL 是否运行
Get-Service postgresql-x64-18

# 检查端口是否被占用
netstat -an | findstr :5432

# 测试连接
psql -U postgres -h localhost -p 5432
```

### 4. 权限问题

如果遇到权限错误：

```sql
-- 连接为 postgres 用户
psql -U postgres

-- 重新授予权限
GRANT ALL PRIVILEGES ON DATABASE railway12606 TO railway_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO railway_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO railway_user;
```

### 5. Python 虚拟环境问题

```powershell
# 如果激活脚本执行失败
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 重新创建虚拟环境
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📚 项目数据库信息

### 数据库配置
- **数据库名**: `railway12606`
- **用户名**: `railway_user`
- **密码**: `railway_password`
- **主机**: `localhost`
- **端口**: `5432`

### 数据表说明
1. **users** - 用户表：存储注册用户信息
2. **passengers** - 乘客表：存储用户添加的乘客信息
3. **stations** - 车站表：存储所有车站信息
4. **trains** - 车次表：存储车次信息
5. **seats** - 座位表：存储每个车次每天的座位信息
6. **orders** - 订单表：存储订单信息
7. **order_passengers** - 订单乘客表：关联订单和乘客

## 🎯 快速启动总结

1. **启动 PostgreSQL 服务**：`net start postgresql-x64-18`
2. **创建数据库和用户**：按照上述 SQL 命令执行
3. **配置 .env 文件**：复制上述配置内容
4. **安装依赖**：`pip install -r requirements.txt`
5. **运行迁移**：`alembic upgrade head`
6. **启动服务**：`uvicorn app.main:app --reload`

完成这些步骤后，你的 Railway 12306 项目就可以正常运行了！