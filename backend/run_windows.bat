@echo off
chcp 65001 >nul
echo ========================================
echo   Railway 12306 后端启动脚本 (Windows)
echo ========================================
echo.

:: 检查是否在正确的目录
if not exist "app\main.py" (
    echo ❌ 错误：请在 backend 目录下运行此脚本
    echo 当前目录：%cd%
    pause
    exit /b 1
)

:: 检查 .env 文件
if not exist ".env" (
    echo ❌ 错误：.env 文件不存在
    echo 正在从 .env.example 创建 .env 文件...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ .env 文件已创建，请配置后重新运行脚本
        echo 配置文件位置：%cd%\.env
        pause
        exit /b 1
    ) else (
        echo ❌ .env.example 文件不存在，请手动创建 .env 文件
        pause
        exit /b 1
    )
)

:: 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo 📦 创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败，请检查 Python 安装
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

:: 激活虚拟环境
echo 🔄 激活虚拟环境...
call .venv\Scripts\activate.bat

:: 检查并安装依赖
echo 📦 检查依赖包...
pip list | findstr "fastapi" >nul
if errorlevel 1 (
    echo 📦 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已安装
)

:: 检查 PostgreSQL 服务
echo 🗄️ 检查 PostgreSQL 服务...
sc query postgresql-x64-18 | findstr "RUNNING" >nul
if errorlevel 1 (
    echo ⚠️ PostgreSQL 服务未运行，尝试启动...
    net start postgresql-x64-18 >nul 2>&1
    if errorlevel 1 (
        echo ❌ PostgreSQL 服务启动失败
        echo 请手动启动 PostgreSQL 服务：
        echo   net start postgresql-x64-18
        pause
        exit /b 1
    )
    echo ✅ PostgreSQL 服务已启动
) else (
    echo ✅ PostgreSQL 服务正在运行
)

:: 测试数据库连接
echo 🔗 测试数据库连接...
python -c "
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('✅ 数据库连接成功')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    exit(1)
"
if errorlevel 1 (
    echo ⚠️ 数据库连接失败，请检查 .env 配置
    echo 配置文件位置：%cd%\.env
    pause
    exit /b 1
)

:: 运行数据库迁移
echo 🔄 运行数据库迁移...
alembic upgrade head
if errorlevel 1 (
    echo ❌ 数据库迁移失败
    pause
    exit /b 1
)
echo ✅ 数据库迁移完成

:: 启动服务器
echo.
echo 🚀 启动 FastAPI 服务器...
echo 📖 API 文档：http://localhost:8000/api/docs
echo 🏥 健康检查：http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务器
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000