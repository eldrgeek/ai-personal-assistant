#!/bin/bash

echo "🚀 Starting AI Personal Assistant..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Initialize database first
echo "🗄️  Initializing local database..."
cd backend
source venv/bin/activate

# Check if database needs initialization
if [ ! -f "ai_assistant.db" ] || [ ! -s "ai_assistant.db" ]; then
    echo "📊 Creating and seeding database..."
    python init_local_db.py
else
    echo "✅ Database already exists, checking data..."
    python -c "
from core.database import get_db_session
from models import Project, Ritual
try:
    db = get_db_session()
    project_count = db.query(Project).count()
    ritual_count = db.query(Ritual).count()
    db.close()
    print(f'📊 Database contains {project_count} projects and {ritual_count} rituals')
    if project_count == 0 or ritual_count == 0:
        print('⚠️  Database exists but missing data, re-seeding...')
        from utils.seed_data import seed_all_data
        seed_all_data()
        print('✅ Data re-seeded successfully')
except Exception as e:
    print(f'❌ Database check failed: {e}')
    print('🔄 Re-initializing database...')
    from init_local_db import main
    main()
"
fi

# Start backend
echo "🐍 Starting Python backend..."
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting React frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ AI Personal Assistant is starting up!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait
