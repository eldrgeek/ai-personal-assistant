import { useState, useEffect } from 'react'

interface Ritual {
  id: string
  name: string
  steps: string[]
  estimated_duration: string
  completed_steps: string[]
}

const RitualTracker: React.FC = () => {
  const [rituals, setRituals] = useState<Ritual[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRituals()
  }, [])

  const fetchRituals = async () => {
    try {
      const [morningResponse, eveningResponse] = await Promise.all([
        fetch('http://localhost:8000/api/assistant/rituals/morning'),
        fetch('http://localhost:8000/api/assistant/rituals/evening')
      ])

      if (morningResponse.ok && eveningResponse.ok) {
        const morningRitual = await morningResponse.json()
        const eveningRitual = await eveningResponse.json()
        
        setRituals([
          {
            id: 'morning',
            name: morningRitual.ritual,
            steps: morningRitual.steps,
            estimated_duration: morningRitual.estimated_duration,
            completed_steps: []
          },
          {
            id: 'evening',
            name: eveningRitual.ritual,
            steps: eveningRitual.steps,
            estimated_duration: eveningRitual.estimated_duration,
            completed_steps: []
          }
        ])
      }
    } catch (error) {
      console.error('Failed to fetch rituals:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleStep = (ritualId: string, step: string) => {
    setRituals(prevRituals => 
      prevRituals.map(ritual => {
        if (ritual.id === ritualId) {
          const isCompleted = ritual.completed_steps.includes(step)
          if (isCompleted) {
            return {
              ...ritual,
              completed_steps: ritual.completed_steps.filter(s => s !== step)
            }
          } else {
            return {
              ...ritual,
              completed_steps: [...ritual.completed_steps, step]
            }
          }
        }
        return ritual
      })
    )
  }

  const getRitualProgress = (ritual: Ritual) => {
    return Math.round((ritual.completed_steps.length / ritual.steps.length) * 100)
  }

  const getTimeOfDay = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'morning'
    if (hour < 18) return 'afternoon'
    return 'evening'
  }

  if (loading) {
    return <div className="loading">Loading rituals...</div>
  }

  return (
    <div className="ritual-tracker">
      <h2>🧘 Ritual Tracker</h2>
      <p className="ritual-intro">
        Track your daily rituals to maintain consistency and mindfulness.
      </p>

      <div className="rituals-container">
        {rituals.map(ritual => {
          const progress = getRitualProgress(ritual)
          const isCurrentTime = 
            (ritual.id === 'morning' && getTimeOfDay() === 'morning') ||
            (ritual.id === 'evening' && getTimeOfDay() === 'evening')

          return (
            <div key={ritual.id} className={`ritual-card ${isCurrentTime ? 'current-time' : ''}`}>
              <div className="ritual-header">
                <h3>{ritual.name}</h3>
                <div className="ritual-meta">
                  <span className="duration">⏱️ {ritual.estimated_duration}</span>
                  <span className="progress">📊 {progress}%</span>
                </div>
              </div>

              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>

              <div className="ritual-steps">
                {ritual.steps.map((step, index) => {
                  const isCompleted = ritual.completed_steps.includes(step)
                  return (
                    <div key={index} className="ritual-step">
                      <label className="step-checkbox">
                        <input
                          type="checkbox"
                          checked={isCompleted}
                          onChange={() => toggleStep(ritual.id, step)}
                        />
                        <span className={`step-text ${isCompleted ? 'completed' : ''}`}>
                          {step}
                        </span>
                      </label>
                    </div>
                  )
                })}
              </div>

              {progress === 100 && (
                <div className="ritual-complete">
                  🎉 {ritual.name} completed for today!
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="ritual-tips">
        <h3>💡 Ritual Tips</h3>
        <ul>
          <li>Start with the morning ritual to set a positive tone for the day</li>
          <li>Use the evening ritual to reflect and prepare for tomorrow</li>
          <li>Be consistent but flexible - adapt rituals to your schedule</li>
          <li>Celebrate small wins and progress</li>
        </ul>
      </div>
    </div>
  )
}

export default RitualTracker
