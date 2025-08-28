# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Personal Assistant - A full-stack web application with React/TypeScript frontend and Python FastAPI backend. The app provides sprint management, project tracking, ritual monitoring, family reminders, and MCP (Model Context Protocol) integration capabilities.

## Tech Stack

### Frontend
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7
- **Dev Server**: Port 5173
- **Styling**: CSS modules

### Backend  
- **Framework**: FastAPI with Python 3.11+
- **Server**: Uvicorn on port 8000
- **Database**: SQLite (dev), PostgreSQL ready (prod)
- **AI**: OpenAI and Anthropic API integrations via LangChain

## Common Development Commands

### Quick Start
```bash
# Start both frontend and backend (recommended)
./start.sh

# Or use npm from root
npm run dev
```

### Frontend Commands
```bash
cd frontend
npm run dev          # Start dev server on port 5173
npm run build        # Build for production
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

### Backend Commands
```bash
cd backend
source venv/bin/activate     # Activate virtual environment
python main.py               # Start FastAPI server on port 8000
python -m pytest             # Run tests
```

### Project-Wide Commands (from root)
```bash
npm run install:all   # Install all dependencies (frontend + backend)
npm run dev          # Start both frontend and backend concurrently
npm run test         # Run tests for both frontend and backend
npm run build        # Build frontend for production
npm run clean        # Remove node_modules, __pycache__, and .db files
```

## Architecture

### Frontend Structure
- **Components**: Located in `frontend/src/components/`
  - `SprintManager.tsx` - Sprint tracking with timers and distraction logging
  - `ProjectDashboard.tsx` - Project CRUD with filtering/sorting
  - `RitualTracker.tsx` - Morning/evening ritual checklists
  - `FamilyReminders.tsx` - Family contact tracking
  - `MCPIntegration.tsx` - External tool execution interface

### Backend Structure  
- **API Routes**: Located in `backend/api/routes/`
  - `/api/assistant/*` - Sprint and ritual endpoints
  - `/api/projects/*` - Project management endpoints
  - `/api/auth/*` - Authentication endpoints
- **Core**: Located in `backend/core/`
  - `config.py` - Settings and environment configuration
  - `database.py` - Database initialization and session management
- **Entry Point**: `backend/main.py` - FastAPI application with CORS and routing

### API Communication
- Frontend fetches from `http://localhost:8000/api/*`
- CORS configured for `localhost:5173` (dev) and production URLs
- API documentation available at `http://localhost:8000/docs`

## Key Patterns

### State Management
- React hooks (`useState`, `useEffect`) for local state
- Direct API calls from components (no global state management)
- Real-time updates via polling or event-driven fetches

### Data Flow
1. User interaction in React component
2. API call to FastAPI backend
3. Backend processes request (DB operations, AI calls, MCP tools)
4. JSON response to frontend
5. Component state update and re-render

### Error Handling
- Try-catch blocks around API calls
- Backend returns appropriate HTTP status codes
- Frontend displays error messages to users

## Environment Configuration

Backend requires `.env` file with:
- `DEBUG` - Development mode flag
- `SECRET_KEY` - JWT authentication key
- `OPENAI_API_KEY` - For AI features
- `ANTHROPIC_API_KEY` - For AI features
- `MCP_SERVER_URL` - MCP server endpoint
- Database connection strings (if using PostgreSQL)

## Testing

- Frontend: Tests would use Vitest (config present but no tests yet)
- Backend: Tests use pytest (test directory exists but empty)

## Deployment

- **Frontend**: Build with `npm run build`, deploy `dist/` to Netlify
- **Backend**: Deploy to Render with `render.yaml` configuration
- **CI/CD**: GitHub Actions workflow configured for automatic deployments
- Setup script: `setup-deployment.sh` for initial deployment configuration