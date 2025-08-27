# 🤖 AI Personal Assistant

An intelligent, AI-powered personal assistant built with React, TypeScript, and Python FastAPI. This application helps you manage sprints, track projects, maintain daily rituals, stay connected with family, and execute MCP (Model Context Protocol) tools.

## ✨ Features

### 🎯 Sprint Management
- **Time-boxed sprints** with customizable durations (15 min to 2 hours)
- **Real-time countdown** and progress tracking
- **Distraction logging** to maintain focus
- **Sprint retrospectives** for continuous improvement
- **Victory lap celebrations** upon completion

### 📋 Project Dashboard
- **Project organization** with priority and status tracking
- **Filtering and sorting** by priority and status
- **Real-time updates** and project management
- **Project creation and editing** capabilities

### 🧘 Ritual Tracker
- **Morning ritual checklist** (cold shower, pendant, journaling, etc.)
- **Evening ritual tracking** (device charging, retro journaling, planning)
- **Progress visualization** with completion percentages
- **Time-aware suggestions** based on current time of day

### 👨‍👩‍👧‍👦 Family Reminders
- **Daily family check-ins** (6:00 PM reminder)
- **Family member profiles** with relationship tracking
- **Contact history** and last interaction dates
- **Customizable family member management**

### 🔧 MCP Integration
- **WhatsApp messaging** via MCP tools
- **Google Calendar** event management
- **Google Drive** file operations
- **Email sending** capabilities
- **Reminder creation** and management

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-personal-assistant
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd ../backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

5. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## 🏗️ Project Structure

```
ai-personal-assistant/
├── docs/initial/                    # Initial documentation
│   ├── assistant_v_0_full_context_log.md
│   ├── mcp_integration_brief.md
│   └── anchor_chat_summary.md
├── frontend/                        # React + TypeScript frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── SprintManager.tsx
│   │   │   ├── ProjectDashboard.tsx
│   │   │   ├── RitualTracker.tsx
│   │   │   ├── FamilyReminders.tsx
│   │   │   └── MCPIntegration.tsx
│   │   ├── App.tsx                 # Main application
│   │   └── App.css                 # Styles
│   ├── package.json
│   └── vite.config.ts
├── backend/                         # Python FastAPI backend
│   ├── api/
│   │   └── routes/                 # API endpoints
│   │       ├── assistant.py        # Sprint and ritual endpoints
│   │       ├── auth.py             # Authentication
│   │       └── projects.py         # Project management
│   ├── core/
│   │   ├── config.py               # Configuration
│   │   └── database.py             # Database setup
│   ├── main.py                     # FastAPI application
│   └── requirements.txt            # Python dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the `backend/` directory:

```env
# Application
DEBUG=true
SECRET_KEY=your-secret-key-change-in-production

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# MCP Integration
MCP_SERVER_URL=http://localhost:3001
MCP_AUTH_TOKEN=your-mcp-auth-token

# External Services
GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
WHATSAPP_API_KEY=your-whatsapp-api-key
```

### MCP Server Setup
To use MCP tools, you'll need to set up an MCP server. The application is configured to connect to an MCP server at `http://localhost:3001` by default.

## 📱 Usage

### Starting a Sprint
1. Navigate to the **Sprint Manager** tab
2. Enter your task description
3. Select sprint duration
4. Click **Start Sprint**
5. Use distraction logging during the sprint
6. Complete the retrospective when finished

### Managing Projects
1. Go to the **Projects** tab
2. View all your projects with status and priority
3. Filter by priority or status
4. Create new projects or update existing ones
5. Track progress and completion

### Daily Rituals
1. Visit the **Rituals** tab
2. Check off completed ritual steps
3. Monitor progress with visual progress bars
4. Get time-aware ritual suggestions

### Family Connections
1. Access the **Family** tab
2. View daily family check-in reminders
3. Manage family member profiles
4. Track last contact dates

### MCP Tools
1. Navigate to **MCP Tools**
2. Select a tool from the available options
3. Fill in required parameters
4. Execute the tool and view results

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
cd backend
source venv/bin/activate
python main.py       # Start development server
```

### API Documentation
Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest
```

## 🚀 Deployment

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy the dist/ folder to your hosting service
```

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
# Deploy to your preferred hosting service (Heroku, AWS, etc.)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sprint Methodology** - Based on time-boxed productivity techniques
- **Ritual Framework** - Inspired by morning/evening routine optimization
- **MCP Protocol** - Model Context Protocol for AI tool integration
- **FastAPI** - Modern Python web framework
- **React + TypeScript** - Frontend development stack
- **Vite** - Fast build tool and development server

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the component documentation in the code

---

**Built with ❤️ for productivity and personal growth**
