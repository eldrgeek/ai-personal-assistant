import { useState, useEffect } from 'react'

interface Sprint {
  id: string
  task: string
  duration_minutes: number
  start_time: string
  end_time: string
  status: string
  distractions: string[]
}

interface SprintManagerProps {
  currentSprint: Sprint | null
  onSprintUpdate: (sprint: Sprint | null) => void
}

const SprintManager: React.FC<SprintManagerProps> = ({ currentSprint, onSprintUpdate }) => {
  const [task, setTask] = useState('')
  const [duration, setDuration] = useState(30)
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [distraction, setDistraction] = useState('')
  const [retro, setRetro] = useState('')

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>
    if (currentSprint && currentSprint.status === 'active') {
      interval = setInterval(() => {
        const remaining = Math.max(0, Math.ceil((new Date(currentSprint.end_time).getTime() - Date.now()) / 60000))
        setTimeRemaining(remaining)
        
        if (remaining <= 0) {
          // Sprint time is up
          clearInterval(interval)
        }
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [currentSprint])

  const startSprint = async () => {
    if (!task.trim()) return

    try {
      const response = await fetch('http://localhost:8000/api/assistant/sprint/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task: task.trim(),
          duration_minutes: duration,
        }),
      })

      if (response.ok) {
        const sprint = await response.json()
        onSprintUpdate(sprint)
        setTask('')
      }
    } catch (error) {
      console.error('Failed to start sprint:', error)
    }
  }

  const logDistraction = async () => {
    if (!distraction.trim() || !currentSprint) return

    try {
      await fetch(`http://localhost:8000/api/assistant/sprint/${currentSprint.id}/distraction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ distraction: distraction.trim() }),
      })

      // Update local sprint with distraction
      const updatedSprint = {
        ...currentSprint,
        distractions: [...currentSprint.distractions, distraction.trim()]
      }
      onSprintUpdate(updatedSprint)
      setDistraction('')
    } catch (error) {
      console.error('Failed to log distraction:', error)
    }
  }

  const completeSprint = async () => {
    if (!retro.trim() || !currentSprint) return

    try {
      await fetch(`http://localhost:8000/api/assistant/sprint/${currentSprint.id}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ retro: retro.trim() }),
      })

      // Clear current sprint
      onSprintUpdate(null)
      setRetro('')
      setTimeRemaining(0)
    } catch (error) {
      console.error('Failed to complete sprint:', error)
    }
  }

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}m`
  }

  return (
    <div className="sprint-manager">
      <h2>⏱️ Sprint Manager</h2>
      
      {!currentSprint ? (
        <div className="sprint-setup">
          <h3>Start New Sprint</h3>
          <div className="form-group">
            <label htmlFor="task">Task:</label>
            <input
              id="task"
              type="text"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="What are you working on?"
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="duration">Duration (minutes):</label>
            <select
              id="duration"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="form-select"
            >
              <option value={15}>15 minutes</option>
              <option value={30}>30 minutes</option>
              <option value={45}>45 minutes</option>
              <option value={60}>1 hour</option>
              <option value={90}>1.5 hours</option>
              <option value={120}>2 hours</option>
            </select>
          </div>
          <button onClick={startSprint} className="btn btn-primary">
            🚀 Start Sprint
          </button>
        </div>
      ) : (
        <div className="sprint-active">
          <h3>Active Sprint</h3>
          <div className="sprint-info">
            <p><strong>Task:</strong> {currentSprint.task}</p>
            <p><strong>Duration:</strong> {currentSprint.duration_minutes} minutes</p>
            <p><strong>Time Remaining:</strong> {formatTime(timeRemaining)}</p>
            <p><strong>Status:</strong> {currentSprint.status}</p>
          </div>

          <div className="sprint-controls">
            <div className="form-group">
              <label htmlFor="distraction">Log Distraction:</label>
              <input
                id="distraction"
                type="text"
                value={distraction}
                onChange={(e) => setDistraction(e.target.value)}
                placeholder="What distracted you?"
                className="form-input"
              />
              <button onClick={logDistraction} className="btn btn-secondary">
                📌 Log Distraction
              </button>
            </div>

            {timeRemaining <= 0 && (
              <div className="form-group">
                <label htmlFor="retro">Sprint Retrospective:</label>
                <textarea
                  id="retro"
                  value={retro}
                  onChange={(e) => setRetro(e.target.value)}
                  placeholder="What worked? What didn't? One improvement?"
                  className="form-textarea"
                  rows={3}
                />
                <button onClick={completeSprint} className="btn btn-success">
                  🎉 Complete Sprint
                </button>
              </div>
            )}
          </div>

          {currentSprint.distractions.length > 0 && (
            <div className="distractions-list">
              <h4>Distractions Logged:</h4>
              <ul>
                {currentSprint.distractions.map((d, index) => (
                  <li key={index}>📌 {d}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SprintManager
