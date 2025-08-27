import { useState, useEffect } from 'react'
import './App.css'
import SprintManager from './components/SprintManager'
import ProjectDashboard from './components/ProjectDashboard'
import RitualTracker from './components/RitualTracker'
import FamilyReminders from './components/FamilyReminders'
import MCPIntegration from './components/MCPIntegration'

interface Sprint {
  id: string
  task: string
  duration_minutes: number
  start_time: string
  end_time: string
  status: string
  distractions: string[]
}

interface Project {
  id: string
  name: string
  description: string
  priority: string
  status: string
  created_at: string
  updated_at: string
}

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [currentSprint, setCurrentSprint] = useState<Sprint | null>(null)
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    // Fetch projects on component mount
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/projects/')
      if (response.ok) {
        const data = await response.json()
        setProjects(data)
      }
    } catch (error) {
      console.error('Failed to fetch projects:', error)
    }
  }

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'sprints', label: 'Sprint Manager', icon: '⏱️' },
    { id: 'projects', label: 'Projects', icon: '📋' },
    { id: 'rituals', label: 'Rituals', icon: '🧘' },
    { id: 'family', label: 'Family', icon: '👨‍👩‍👧‍👦' },
    { id: 'mcp', label: 'MCP Tools', icon: '🔧' }
  ]

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 AI Personal Assistant</h1>
        <p>Your intelligent companion for productivity and life management</p>
      </header>

      <nav className="app-nav">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </nav>

      <main className="app-main">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>Welcome to Your AI Assistant</h2>
            <div className="dashboard-grid">
              <div className="dashboard-card">
                <h3>Current Sprint</h3>
                {currentSprint ? (
                  <div className="sprint-status">
                    <p><strong>Task:</strong> {currentSprint.task}</p>
                    <p><strong>Time Remaining:</strong> {Math.max(0, Math.ceil((new Date(currentSprint.end_time).getTime() - Date.now()) / 60000))} minutes</p>
                  </div>
                ) : (
                  <p>No active sprint</p>
                )}
              </div>
              <div className="dashboard-card">
                <h3>Today's Focus</h3>
                <p>Complete MCP integration setup</p>
              </div>
              <div className="dashboard-card">
                <h3>Family Reminders</h3>
                <p>6:00 PM - Reach out to kids and granddaughter Kaya</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sprints' && (
          <SprintManager 
            currentSprint={currentSprint}
            onSprintUpdate={setCurrentSprint}
          />
        )}

        {activeTab === 'projects' && (
          <ProjectDashboard 
            projects={projects}
            onProjectsUpdate={setProjects}
          />
        )}

        {activeTab === 'rituals' && (
          <RitualTracker />
        )}

        {activeTab === 'family' && (
          <FamilyReminders />
        )}

        {activeTab === 'mcp' && (
          <MCPIntegration />
        )}
      </main>
    </div>
  )
}

export default App
