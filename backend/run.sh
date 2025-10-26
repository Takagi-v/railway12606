#!/bin/bash

# Railway 12306 Backend Startup Script
set -e  # Exit on error

echo "🚀 Starting Railway 12306 Backend..."
echo ""

# Set PostgreSQL path
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/postgresql@16/lib"
export CPPFLAGS="-I/opt/homebrew/opt/postgresql@16/include"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found."
    echo "Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please configure it before continuing."
        exit 1
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check PostgreSQL service
echo "🗄️  Checking PostgreSQL service..."
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running. Starting it..."
    brew services start postgresql@16
    echo "⏳ Waiting for PostgreSQL to start..."
    sleep 3
fi

# Check database connection
echo "🔌 Checking database connection..."
if ! python -c "from app.db.session import engine; engine.connect()" 2>/dev/null; then
    echo "⚠️  Database connection failed. Please check your .env configuration."
fi

# Run database migrations
echo "🔄 Running database migrations..."
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "📝 Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

echo "⬆️  Applying migrations..."
alembic upgrade head

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "🌐 Starting FastAPI server..."
echo "📖 API Documentation: http://localhost:8000/api/docs"
echo "🔍 ReDoc: http://localhost:8000/api/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

