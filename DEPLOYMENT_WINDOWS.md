# Railway 12306 项目部署指南（Windows）

本指南面向 Windows 10/11 环境，覆盖后端 FastAPI、数据库 PostgreSQL 与前端 Vite+Vue 的本地开发与生产部署流程。

## 环境准备
- 必备软件
  - `Python` 3.11+（建议）
  - `Node.js` 18+/20+（Vite 5 需要 18+）
  - `PostgreSQL` 16/18（示例使用 18）（需要前往PostgreSQL官网下载安装）
  - `PowerShell` 7+（建议）
- 基本检查
  - `python --version`
  - `node -v && npm -v`
  - `psql --version`

## 项目结构
- `backend/` FastAPI 后端（端口 `8000`）
- `frontend/` Vite 前端（端口 `5173`，占用时自动切换）

## 快速启动（本地开发）
1) 数据库与后端
- 启动 PostgreSQL 服务（安装为 18 版本示例）：
  - `net start postgresql-x64-18`
 - 在 `backend` 目录将 `.env.example` 复制为 `.env` 并按需修改：
  - 默认示例值可直接用于本地运行；如需自定义数据库账号密码，请同步修改 `DATABASE_URL/POSTGRES_*`
  - `SECRET_KEY` 本地开发可任意使用，或者运行命令：`python -c "import secrets; print(secrets.token_hex(32))"` 生成随机值
- 创建并激活虚拟环境，安装依赖：
  - `cd backend`
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`
  - 如执行策略受限：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
  - `pip install -r requirements.txt`
  - 如果更熟悉 conda，也可以：
    - `conda create -n railway12606 python=3.11 -y`
    - `conda activate railway12606`
    - `pip install -r requirements.txt`
- 运行数据库迁移：
  - `alembic upgrade head`
- 启动后端服务：
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- 验证：
  - API 文档 `http://localhost:8000/api/docs`
  - 健康检查 `http://localhost:8000/health`

### 详细步骤（零基础友好）

1. 安装 PostgreSQL 并确保可用
  - 前往 PostgreSQL 官方下载安装（建议 16/18）。安装过程会设置超级用户 `postgres` 的密码，请记录。
  - 如果命令行提示找不到 `psql`，将 `C:\Program Files\PostgreSQL\18\bin` 加入系统环境变量 `Path`。
  - 启动服务：`net start postgresql-x64-18`，并用 `Get-Service postgresql-x64-18` 检查状态。

2. 使用 psql 创建数据库与专用用户
  - 连接：`psql -U postgres -h localhost`，输入安装时设定的密码。
  - 执行：
    - `CREATE USER railway_user WITH PASSWORD 'railway_password';`
    - `CREATE DATABASE railway12606 OWNER railway_user;`
    - `GRANT ALL PRIVILEGES ON DATABASE railway12606 TO railway_user;`
  - 退出：`\q`
  - 验证连接：`psql -U railway_user -d railway12606 -h localhost`

3. 在 backend 目录创建 `.env`（推荐直接复制）
  - 将 `backend/.env.example` 复制为 `backend/.env`
  - 默认示例值可直接用于本地运行；如需更改数据库账号密码，请修改：
    - `DATABASE_URL`
    - `POSTGRES_USER`
    - `POSTGRES_PASSWORD`
    - `POSTGRES_DB`
    - `POSTGRES_HOST`
    - `POSTGRES_PORT`
  - `SECRET_KEY` 在本地开发可直接沿用示例值；生产环境再替换即可

4. 创建 Python 虚拟环境并安装依赖
  - venv：`python -m venv .venv` → `./.venv/Scripts/Activate.ps1` → `pip install -r requirements.txt`
  - conda：`conda create -n railway12606 python=3.11 -y` → `conda activate railway12606` → `pip install -r requirements.txt`
  - 如 PowerShell 有执行策略限制：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

5. 初始化数据库并启动后端
  - 迁移：在 `backend` 目录运行 `alembic upgrade head`（会自动创建所有项目表）
  - 启动：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  - 验证：`http://localhost:8000/api/docs` 与 `http://localhost:8000/health`

2) 前端
- 在 `frontend` 目录创建环境文件，指向后端：
  - 建议创建 `frontend/.env.development` 内容：
    - `VITE_API_BASE_URL=http://localhost:8000/api`
- 安装依赖与启动：
  - `cd frontend`
  - `npm install`
  - `npm run dev`
- 访问页面：
  - `http://localhost:5173/`（端口被占用时，Vite 自动切到 `5174` 等）

## 生产部署（单机示例）
- 后端（FastAPI/uvicorn）
  - 启动命令示例：
    - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2`
  - Windows 可用 NSSM/任务计划等方式托管为服务
- 前端（静态构建）
  - `cd frontend && npm run build`
  - 产物位于 `frontend/dist`
  - 使用 `npm run preview` 本地预览：`http://localhost:4173/`
  - 生产环境建议由 Nginx/IIS 托管，反向代理 `/api` 到后端 `http://localhost:8000`
- 反向代理要点
  - 保留接口前缀 `/api`（后端在 `app/core/config.py` 中配置 `API_PREFIX=/api`）
  - 开启 CORS 或确保同域部署避免跨域

## 端口与代理
- 后端：`8000`
- 前端：`5173`（Vite 自动切端口）
- 开发模式下，Vite 代理 `/api` 到后端：
  - `frontend/vite.config.js` 中 `server.proxy['/api']` 会依据 `VITE_API_BASE_URL` 自动指向后端

## 常见问题
- 执行策略限制
  - 现象：激活虚拟环境时报错
  - 解决：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- 端口占用
  - 后端：`netstat -ano | findstr :8000` → 结束相应进程或改端口
  - 前端：Vite 自动切端口；也可在 `vite.config.js` 修改 `server.port`
- 数据库连接失败
  - 确认服务启动：`Get-Service postgresql-x64-18`
  - 测试连接：`psql -U railway_user -d railway12606 -h localhost`
  - 检查 `.env` 的 `DATABASE_URL`
- CORS 报错
  - 确认 `.env` 的 `CORS_ORIGINS` 包含前端地址
  - 或前后端同域部署，移除跨域需求

## 验证清单
- 后端：
  - `http://localhost:8000/api/docs` 可打开
  - 登录/注册等接口返回 `200`
- 前端：
  - 首页与“个人中心”可访问
  - “火车票订单”页调用 `/api/orders` 正常（默认由 `VITE_API_BASE_URL` 指向后端）

## 项目维护
- 代码检查（前端）：
  - `npm run lint:check`
  - `npm run format:check`
- 构建（前端）：
  - `npm run build`
- Postman 脚本：`backend/postman` 目录（本地环境为 `http://localhost:8000`）

## 参考文件
- 后端安全配置：`backend/SECURITY_CONFIG.md`
- PostgreSQL（Windows）详解：`backend/POSTGRES_GUIDE_WINDOWS.md`
- 反向代理与开发代理：`frontend/vite.config.js`
- 接口前缀：`backend/app/core/config.py` 中 `API_PREFIX=/api`