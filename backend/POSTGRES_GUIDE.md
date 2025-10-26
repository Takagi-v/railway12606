# PostgreSQL 管理指南（macOS）

## 🚀 启动和停止

### 启动 PostgreSQL

```bash
# 方式 1：启动并设置为开机自启（推荐）
brew services start postgresql@16

# 方式 2：仅启动一次（不自启）
brew services run postgresql@16

# 方式 3：手动启动
pg_ctl -D /opt/homebrew/var/postgresql@16 start
```

### 停止 PostgreSQL

```bash
# 使用 brew services
brew services stop postgresql@16

# 或手动停止
pg_ctl -D /opt/homebrew/var/postgresql@16 stop
```

### 重启 PostgreSQL

```bash
brew services restart postgresql@16
```

### 查看状态

```bash
# 查看所有 brew 服务
brew services list

# 仅查看 PostgreSQL
brew services list | grep postgresql

# 检查是否可连接
pg_isready -h localhost -p 5432

# 查看进程
ps aux | grep postgres
```

## 🗄️ 数据库操作

### 连接数据库

```bash
# 连接到项目数据库
psql -U railway_user -d railway12606

# 连接到默认数据库
psql postgres
```

### 常用 psql 命令

在 psql 命令行中：

```sql
-- 列出所有数据库
\l

-- 连接到指定数据库
\c railway12606

-- 列出当前数据库的所有表
\dt

-- 查看表结构
\d users
\d passengers
\d trains

-- 查看表数据
SELECT * FROM users;

-- 退出 psql
\q
```

### 管理数据库

```bash
# 创建新数据库
createdb mydb

# 删除数据库
dropdb mydb

# 创建新用户
createuser myuser

# 列出所有数据库
psql -l

# 备份数据库
pg_dump -U railway_user railway12606 > backup.sql

# 恢复数据库
psql -U railway_user railway12606 < backup.sql
```

## 🔧 数据库迁移

### 什么是迁移？

迁移是将代码中的模型（models）转换为数据库表结构的过程。

### 何时需要迁移？

✅ **需要迁移：**
- 第一次启动项目（创建所有表）
- 添加新的数据表（新模型）
- 修改表结构（添加/删除字段）
- 修改字段类型、约束等

❌ **不需要迁移：**
- 只修改业务逻辑
- 只修改 API 接口
- 数据库结构没变化

### 迁移命令

```bash
# 进入后端目录并激活虚拟环境
cd backend
source .venv/bin/activate

# 创建迁移文件（自动检测模型变化）
alembic revision --autogenerate -m "描述你的修改"

# 应用迁移（执行到最新版本）
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

### 迁移示例

**场景：给 User 表添加头像字段**

```python
# 1. 修改 app/models/user.py
class User(Base):
    # ... 原有字段
    avatar = Column(String(255), nullable=True, comment="用户头像URL")
```

```bash
# 2. 创建迁移
alembic revision --autogenerate -m "Add avatar field to user table"

# 3. 应用迁移
alembic upgrade head
```

## 🛠️ 故障排除

### PostgreSQL 无法启动

```bash
# 查看日志
tail -f /opt/homebrew/var/log/postgresql@16.log

# 检查端口是否被占用
lsof -i :5432

# 重新初始化数据库（谨慎使用，会清空数据）
rm -rf /opt/homebrew/var/postgresql@16
initdb /opt/homebrew/var/postgresql@16
```

### 无法连接数据库

```bash
# 1. 确认 PostgreSQL 正在运行
brew services list | grep postgresql

# 2. 检查端口
pg_isready -h localhost -p 5432

# 3. 检查用户和密码
psql -U railway_user -d railway12606
```

### 忘记密码

```bash
# 编辑配置文件临时允许无密码登录
# /opt/homebrew/var/postgresql@16/pg_hba.conf
# 将 md5 改为 trust

# 重启 PostgreSQL
brew services restart postgresql@16

# 修改密码
psql postgres
ALTER USER railway_user WITH PASSWORD 'new_password';

# 改回配置文件并重启
```

### 端口冲突

```bash
# 查看占用 5432 端口的进程
lsof -i :5432

# 杀死进程
kill -9 <PID>

# 或者修改 PostgreSQL 端口（不推荐）
# 编辑 /opt/homebrew/var/postgresql@16/postgresql.conf
# port = 5433
```

## 📊 性能和维护

### 查看数据库大小

```sql
-- 查看所有数据库大小
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- 查看表大小
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### 清理和优化

```sql
-- 清理删除的数据（回收空间）
VACUUM;

-- 完整清理并分析
VACUUM FULL ANALYZE;

-- 重建索引
REINDEX DATABASE railway12606;
```

### 备份建议

```bash
# 每日备份脚本示例
#!/bin/bash
BACKUP_DIR="$HOME/backups/railway12606"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
pg_dump -U railway_user railway12606 > "$BACKUP_DIR/backup_$DATE.sql"

# 只保留最近7天的备份
find $BACKUP_DIR -type f -name "backup_*.sql" -mtime +7 -delete
```

## 🎯 推荐配置

### 开发环境（推荐）

```bash
# 1. 设置开机自启
brew services start postgresql@16

# 2. 添加环境变量到 ~/.zshrc
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 3. 使用 run.sh 启动后端（会自动处理迁移）
cd backend
./run.sh
```

### 资源节省模式

```bash
# 开发前启动
brew services start postgresql@16

# 开发后停止
brew services stop postgresql@16
```

## 📚 有用的资源

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [psql 命令速查](https://www.postgresql.org/docs/current/app-psql.html)
- [Alembic 文档](https://alembic.sqlalchemy.org/)

## 🆘 快速命令参考

```bash
# === PostgreSQL 管理 ===
brew services start postgresql@16     # 启动
brew services stop postgresql@16      # 停止
brew services restart postgresql@16   # 重启
brew services list                    # 查看状态

# === 数据库操作 ===
psql -U railway_user -d railway12606  # 连接数据库
createdb dbname                       # 创建数据库
dropdb dbname                         # 删除数据库
pg_dump dbname > backup.sql           # 备份
psql dbname < backup.sql              # 恢复

# === 迁移管理 ===
alembic revision --autogenerate -m "msg"  # 创建迁移
alembic upgrade head                      # 应用迁移
alembic downgrade -1                      # 回滚
alembic history                           # 查看历史
alembic current                           # 当前版本

# === 故障排除 ===
pg_isready                            # 检查状态
lsof -i :5432                         # 检查端口
tail -f /opt/homebrew/var/log/postgresql@16.log  # 查看日志
```

