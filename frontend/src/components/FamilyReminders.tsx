import { useState, useEffect } from 'react'

interface FamilyMember {
  name: string
  relationship: string
  lastContact?: string
  nextContact?: string
  notes?: string
}

interface DailyTask {
  time: string
  task: string
  completed: boolean
}

const FamilyReminders: React.FC = () => {
  const [familyMembers, setFamilyMembers] = useState<FamilyMember[]>([])
  const [dailyTasks, setDailyTasks] = useState<DailyTask[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddMember, setShowAddMember] = useState(false)
  const [newMember, setNewMember] = useState({
    name: '',
    relationship: '',
    notes: ''
  })

  useEffect(() => {
    fetchFamilyData()
  }, [])

  const fetchFamilyData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/assistant/family/reminders')
      if (response.ok) {
        const data = await response.json()
        
        // Set up daily tasks
        setDailyTasks([
          {
            time: '6:00 PM',
            task: 'Reach out to kids (Daniel, Mira, Alyssa) and granddaughter Kaya',
            completed: false
          }
        ])

        // Set up family members based on the API response
        const members: FamilyMember[] = [
          { name: 'Dana', relationship: 'Eldest daughter', notes: 'Married to Daniel; kids Kyra, Siena' },
          { name: 'Mira', relationship: 'Middle daughter', notes: 'Married to John; kids Kaya, Luke, Taz' },
          { name: 'Alyssa', relationship: 'Youngest daughter', notes: 'Married to Konrad; kids Michael, Sylvia' },
          { name: 'Mark', relationship: 'Brother', notes: 'Panama City, retired OB-GYN; married to Sandi; kids David, Sam' },
          { name: 'Zorina', relationship: 'Sister', notes: 'Married to Terrance' }
        ]

        setFamilyMembers(members)
      }
    } catch (error) {
      console.error('Failed to fetch family data:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleTask = (index: number) => {
    setDailyTasks(prev => 
      prev.map((task, i) => 
        i === index ? { ...task, completed: !task.completed } : task
      )
    )
  }

  const addFamilyMember = () => {
    if (!newMember.name.trim() || !newMember.relationship.trim()) return

    const member: FamilyMember = {
      name: newMember.name.trim(),
      relationship: newMember.relationship.trim(),
      notes: newMember.notes.trim() || undefined
    }

    setFamilyMembers(prev => [...prev, member])
    setNewMember({ name: '', relationship: '', notes: '' })
    setShowAddMember(false)
  }

  const updateLastContact = (memberName: string) => {
    const today = new Date().toISOString().split('T')[0]
    setFamilyMembers(prev => 
      prev.map(member => 
        member.name === memberName 
          ? { ...member, lastContact: today }
          : member
      )
    )
  }

  const getTimeUntilTask = (taskTime: string) => {
    const [hours, minutes] = taskTime.split(':').map(Number)
    const now = new Date()
    const taskDate = new Date()
    taskDate.setHours(hours, minutes, 0, 0)
    
    if (taskDate <= now) {
      taskDate.setDate(taskDate.getDate() + 1)
    }
    
    const diff = taskDate.getTime() - now.getTime()
    const hoursRemaining = Math.floor(diff / (1000 * 60 * 60))
    const minutesRemaining = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    
    if (hoursRemaining > 0) {
      return `${hoursRemaining}h ${minutesRemaining}m`
    }
    return `${minutesRemaining}m`
  }

  if (loading) {
    return <div className="loading">Loading family reminders...</div>
  }

  return (
    <div className="family-reminders">
      <h2>👨‍👩‍👧‍👦 Family Reminders</h2>
      <p className="family-intro">
        Stay connected with your family and never miss important moments.
      </p>

      <div className="daily-tasks-section">
        <h3>📅 Daily Tasks</h3>
        <div className="tasks-list">
          {dailyTasks.map((task, index) => (
            <div key={index} className="task-item">
              <label className="task-checkbox">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(index)}
                />
                <span className={`task-text ${task.completed ? 'completed' : ''}`}>
                  <span className="task-time">{task.time}</span>
                  <span className="task-description">{task.task}</span>
                </span>
              </label>
              {!task.completed && (
                <span className="time-until">
                  ⏰ {getTimeUntilTask(task.time)}
                </span>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="family-members-section">
        <div className="section-header">
          <h3>👥 Family Members</h3>
          <button 
            onClick={() => setShowAddMember(!showAddMember)}
            className="btn btn-primary"
          >
            {showAddMember ? 'Cancel' : '+ Add Member'}
          </button>
        </div>

        {showAddMember && (
          <div className="add-member-form">
            <div className="form-group">
              <label htmlFor="memberName">Name:</label>
              <input
                id="memberName"
                type="text"
                value={newMember.name}
                onChange={(e) => setNewMember({...newMember, name: e.target.value})}
                placeholder="Enter name"
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="memberRelationship">Relationship:</label>
              <input
                id="memberRelationship"
                type="text"
                value={newMember.relationship}
                onChange={(e) => setNewMember({...newMember, relationship: e.target.value})}
                placeholder="e.g., Daughter, Brother, etc."
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label htmlFor="memberNotes">Notes:</label>
              <textarea
                id="memberNotes"
                value={newMember.notes}
                onChange={(e) => setNewMember({...newMember, notes: e.target.value})}
                placeholder="Additional information"
                className="form-textarea"
                rows={2}
              />
            </div>
            <button onClick={addFamilyMember} className="btn btn-success">
              Add Family Member
            </button>
          </div>
        )}

        <div className="family-grid">
          {familyMembers.map((member, index) => (
            <div key={index} className="family-member-card">
              <div className="member-header">
                <h4>{member.name}</h4>
                <span className="relationship">{member.relationship}</span>
              </div>
              
              {member.notes && (
                <p className="member-notes">{member.notes}</p>
              )}
              
              <div className="member-actions">
                <button 
                  onClick={() => updateLastContact(member.name)}
                  className="btn btn-secondary"
                >
                  📞 Contact Today
                </button>
              </div>
              
              <div className="member-meta">
                {member.lastContact && (
                  <small>Last contact: {member.lastContact}</small>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="family-tips">
        <h3>💡 Family Connection Tips</h3>
        <ul>
          <li>Set a daily reminder to reach out to family members</li>
          <li>Keep notes about recent conversations and important dates</li>
          <li>Schedule regular check-ins for different family members</li>
          <li>Remember birthdays, anniversaries, and special occasions</li>
        </ul>
      </div>
    </div>
  )
}

export default FamilyReminders
