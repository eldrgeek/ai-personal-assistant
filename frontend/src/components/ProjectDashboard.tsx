import { useState } from 'react'
import { apiUrl } from '../utils/api'

interface Project {
  id: string
  name: string
  description: string
  priority: string
  status: string
  created_at: string
  updated_at: string
}

interface ProjectDashboardProps {
  projects: Project[]
  onProjectsUpdate: (projects: Project[]) => void
}

const ProjectDashboard: React.FC<ProjectDashboardProps> = ({ projects, onProjectsUpdate }) => {
  const [filterPriority, setFilterPriority] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [showNewProjectForm, setShowNewProjectForm] = useState(false)
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    priority: 'medium'
  })

  const filteredProjects = projects.filter(project => {
    if (filterPriority !== 'all' && project.priority !== filterPriority) return false
    if (filterStatus !== 'all' && project.status !== filterStatus) return false
    return true
  })

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'priority-high'
      case 'medium': return 'priority-medium'
      case 'low': return 'priority-low'
      default: return ''
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'status-active'
      case 'in_progress': return 'status-progress'
      case 'completed': return 'status-completed'
      case 'planned': return 'status-planned'
      case 'daily': return 'status-daily'
      default: return ''
    }
  }

  const createProject = async () => {
    if (!newProject.name.trim() || !newProject.description.trim()) return

    try {
      const response = await fetch(apiUrl('api/projects/'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newProject),
      })

      if (response.ok) {
        const createdProject = await response.json()
        onProjectsUpdate([...projects, createdProject])
        setNewProject({ name: '', description: '', priority: 'medium' })
        setShowNewProjectForm(false)
      }
    } catch (error) {
      console.error('Failed to create project:', error)
    }
  }

  const updateProjectStatus = async (projectId: string, newStatus: string) => {
    try {
      const response = await fetch(apiUrl(`api/projects/${projectId}`), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      })

      if (response.ok) {
        const updatedProject = await response.json()
        const updatedProjects = projects.map(p => 
          p.id === projectId ? updatedProject : p
        )
        onProjectsUpdate(updatedProjects)
      }
    } catch (error) {
      console.error('Failed to update project:', error)
    }
  }

  return (
    <div className="project-dashboard">
      <div className="dashboard-header">
        <h2>📋 Project Dashboard</h2>
        <button 
          onClick={() => setShowNewProjectForm(!showNewProjectForm)}
          className="btn btn-primary"
        >
          {showNewProjectForm ? 'Cancel' : '+ New Project'}
        </button>
      </div>

      {showNewProjectForm && (
        <div className="new-project-form">
          <h3>Create New Project</h3>
          <div className="form-group">
            <label htmlFor="projectName">Project Name:</label>
            <input
              id="projectName"
              type="text"
              value={newProject.name}
              onChange={(e) => setNewProject({...newProject, name: e.target.value})}
              placeholder="Enter project name"
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="projectDescription">Description:</label>
            <textarea
              id="projectDescription"
              value={newProject.description}
              onChange={(e) => setNewProject({...newProject, description: e.target.value})}
              placeholder="Enter project description"
              className="form-textarea"
              rows={3}
            />
          </div>
          <div className="form-group">
            <label htmlFor="projectPriority">Priority:</label>
            <select
              id="projectPriority"
              value={newProject.priority}
              onChange={(e) => setNewProject({...newProject, priority: e.target.value})}
              className="form-select"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <button onClick={createProject} className="btn btn-success">
            Create Project
          </button>
        </div>
      )}

      <div className="filters">
        <div className="filter-group">
          <label>Priority:</label>
          <select 
            value={filterPriority} 
            onChange={(e) => setFilterPriority(e.target.value)}
            className="form-select"
          >
            <option value="all">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Status:</label>
          <select 
            value={filterStatus} 
            onChange={(e) => setFilterStatus(e.target.value)}
            className="form-select"
          >
            <option value="all">All Statuses</option>
            <option value="active">Active</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="planned">Planned</option>
            <option value="daily">Daily</option>
          </select>
        </div>
      </div>

      <div className="projects-grid">
        {filteredProjects.map(project => (
          <div key={project.id} className="project-card">
            <div className="project-header">
              <h3>{project.name}</h3>
              <div className="project-badges">
                <span className={`badge priority ${getPriorityColor(project.priority)}`}>
                  {project.priority}
                </span>
                <span className={`badge status ${getStatusColor(project.status)}`}>
                  {project.status}
                </span>
              </div>
            </div>
            <p className="project-description">{project.description}</p>
            <div className="project-actions">
              <select
                value={project.status}
                onChange={(e) => updateProjectStatus(project.id, e.target.value)}
                className="form-select status-select"
              >
                <option value="planned">Planned</option>
                <option value="active">Active</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="daily">Daily</option>
              </select>
            </div>
            <div className="project-meta">
              <small>Created: {new Date(project.created_at).toLocaleDateString()}</small>
              <small>Updated: {new Date(project.updated_at).toLocaleDateString()}</small>
            </div>
          </div>
        ))}
      </div>

      {filteredProjects.length === 0 && (
        <div className="no-projects">
          <p>No projects match the current filters.</p>
        </div>
      )}
    </div>
  )
}

export default ProjectDashboard
