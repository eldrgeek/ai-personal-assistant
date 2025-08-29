# Local Development Setup Guide

**Date**: August 28, 2025  
**Status**: ✅ **FULLY CONFIGURED** - Local development with persistent data working

## 🚀 **Quick Start**

### **Option 1: Use the Start Script (Recommended)**
```bash
# From project root directory
./start.sh
```

This script will:
1. ✅ Initialize the database if needed
2. ✅ Seed initial data (10 projects, 2 rituals)
3. ✅ Start the Python backend
4. ✅ Start the React frontend

### **Option 2: Manual Setup**
```bash
# 1. Initialize database
cd backend
source venv/bin/activate
python init_local_db.py

# 2. Start backend
python main.py

# 3. In another terminal, start frontend
cd frontend
npm run dev
```

## 🗄️ **Database Configuration**

### **Local Database Path**
- **File**: `backend/ai_assistant.db`
- **Type**: SQLite
- **Path Resolution**: Automatically configured to work from any directory
- **Initial Data**: 10 sample projects + 2 rituals (morning/evening)

### **Database Initialization**
The database is automatically initialized when:
- Running `./start.sh`
- Running `python init_local_db.py`
- Starting the app for the first time

### **Data Persistence**
- ✅ Data persists between app restarts
- ✅ Database file is located at `backend/ai_assistant.db`
- ✅ Initial seed data includes real project examples

## 🔧 **Configuration Files**

### **Backend Configuration**
- **File**: `backend/core/config.py`
- **Database Path**: Automatically resolved based on working directory
- **Environment**: Development mode with debug enabled

### **Frontend Configuration**
- **API Base URL**: `http://localhost:8000` (local development)
- **Environment Variables**: Loaded from `.env` if present

## 📊 **Available Data**

### **Sample Projects (10 total)**
- MCP connection to assistant
- Assistant v0 (rituals, sprints, logging)
- Improve Reminder Attention-Grabbing
- Inbox Zero (daily)
- Advertisements for Chi Life
- Flyers, cards, etc. for Chi Life
- CJ Clarke for City Council
- NBA Connect for Greg Foster
- Discord+ with Mark and James
- Build the Personal Assistant app

### **Sample Rituals (2 total)**
- **Morning Ritual** (20 minutes)
  - Cold shower (5 min)
  - Put on Limitless AI pendant (1 min)
  - Quick projects/meetings review (5 min)
  - Journaling (9 min)

- **Evening Ritual** (15 minutes)
  - Charge all devices (2 min)
  - Retro journaling (10 min)
  - Looking ahead: pick tomorrow's focus (3 min)

## 🌐 **Local URLs**

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 **Testing Local Features**

### **Backend API Endpoints**
```bash
# Health check
curl http://localhost:8000/health

# Get all projects
curl http://localhost:8000/api/projects/

# Get all rituals
curl http://localhost:8000/api/assistant/rituals/
```

### **Frontend Components**
- **SprintManager**: Test sprint creation and management
- **ProjectDashboard**: Test project CRUD operations
- **RitualTracker**: Test ritual tracking
- **FamilyReminders**: Test reminder system
- **MCPIntegration**: Test MCP tool integration (stubbed)

## 🔍 **Troubleshooting**

### **Database Issues**
```bash
# Re-initialize database
cd backend
python init_local_db.py

# Check database contents
python -c "
from core.database import get_db_session
from models import Project, Ritual
db = get_db_session()
print(f'Projects: {db.query(Project).count()}')
print(f'Rituals: {db.query(Ritual).count()}')
db.close()
"
```

### **Port Conflicts**
- **Backend**: Change port in `backend/core/config.py` or set `PORT` environment variable
- **Frontend**: Change port in `frontend/vite.config.ts`

### **Database Path Issues**
- Ensure you're running from the project root directory
- Check that `backend/ai_assistant.db` exists
- Verify database permissions

## 📝 **Development Notes**

### **Database Schema**
- **Models**: Defined in `backend/models/`
- **Migrations**: Alembic support ready
- **Seed Data**: Located in `backend/utils/seed_data.py`

### **API Structure**
- **Authentication**: JWT-based auth system
- **Routes**: Organized by feature in `backend/api/routes/`
- **Middleware**: CORS configured for local development

### **Frontend Structure**
- **Components**: React components in `frontend/src/components/`
- **API Integration**: Centralized in `frontend/src/utils/api.ts`
- **State Management**: Local component state (can be enhanced with Redux/Context)

## 🚀 **Next Development Steps**

1. **Test All Features**: Verify each component works with local data
2. **Add New Features**: Implement additional functionality
3. **Enhance UI/UX**: Improve the user interface
4. **Implement MCP**: Connect to actual MCP server
5. **Add Tests**: Create unit and integration tests

---

**Status**: ✅ **Ready for Development**  
**Last Updated**: August 28, 2025  
**Next Action**: Test local features and begin development
