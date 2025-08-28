import { useState } from 'react'
import { apiUrl } from '../utils/api'

interface MCPTool {
  name: string
  description: string
  parameters: Record<string, any>
}

interface MCPResponse {
  success: boolean
  data?: any
  error?: string
}

const MCPIntegration: React.FC = () => {
  const [selectedTool, setSelectedTool] = useState<string>('')
  const [toolParameters, setToolParameters] = useState<Record<string, any>>({})
  const [response, setResponse] = useState<MCPResponse | null>(null)
  const [loading, setLoading] = useState(false)

  // Predefined MCP tools based on your documentation
  const availableTools: MCPTool[] = [
    {
      name: 'send_whatsapp',
      description: 'Send a WhatsApp message to a contact',
      parameters: {
        to: 'phone_number',
        text: 'message_content'
      }
    },
    {
      name: 'google_calendar_search',
      description: 'Search Google Calendar for events',
      parameters: {
        query: 'search_term',
        start_date: 'YYYY-MM-DD',
        end_date: 'YYYY-MM-DD'
      }
    },
    {
      name: 'google_drive_search',
      description: 'Search Google Drive for files',
      parameters: {
        query: 'search_term',
        file_type: 'document, spreadsheet, etc.'
      }
    },
    {
      name: 'send_email',
      description: 'Send an email via configured email service',
      parameters: {
        to: 'recipient@email.com',
        subject: 'email_subject',
        body: 'email_body'
      }
    },
    {
      name: 'create_reminder',
      description: 'Create a new reminder or task',
      parameters: {
        title: 'reminder_title',
        description: 'reminder_description',
        due_date: 'YYYY-MM-DD HH:MM',
        priority: 'high, medium, low'
      }
    }
  ]

  const handleToolSelect = (toolName: string) => {
    setSelectedTool(toolName)
    const tool = availableTools.find(t => t.name === toolName)
    if (tool) {
      // Initialize parameters with empty values
      const initialParams: Record<string, any> = {}
      Object.keys(tool.parameters).forEach(key => {
        initialParams[key] = ''
      })
      setToolParameters(initialParams)
    }
    setResponse(null)
  }

  const handleParameterChange = (key: string, value: string) => {
    setToolParameters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const executeTool = async () => {
    if (!selectedTool) return

    setLoading(true)
    setResponse(null)

    try {
      const response = await fetch(apiUrl('api/assistant/mcp/tool'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tool_name: selectedTool,
          parameters: toolParameters
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setResponse({ success: true, data })
      } else {
        const errorData = await response.json()
        setResponse({ success: false, error: errorData.detail || 'Failed to execute tool' })
      }
    } catch (error) {
      setResponse({ 
        success: false, 
        error: error instanceof Error ? error.message : 'Network error' 
      })
    } finally {
      setLoading(false)
    }
  }

  const getSelectedTool = () => {
    return availableTools.find(t => t.name === selectedTool)
  }

  const resetForm = () => {
    setSelectedTool('')
    setToolParameters({})
    setResponse(null)
  }

  return (
    <div className="mcp-integration">
      <h2>🔧 MCP Tools Integration</h2>
      <p className="mcp-intro">
        Execute MCP (Model Context Protocol) tools to extend your assistant's capabilities.
        These tools can interact with external services like WhatsApp, Google Calendar, and more.
      </p>

      <div className="mcp-container">
        <div className="tool-selection">
          <h3>Select MCP Tool</h3>
          <div className="tools-grid">
            {availableTools.map(tool => (
              <div 
                key={tool.name}
                className={`tool-card ${selectedTool === tool.name ? 'selected' : ''}`}
                onClick={() => handleToolSelect(tool.name)}
              >
                <h4>{tool.name}</h4>
                <p>{tool.description}</p>
              </div>
            ))}
          </div>
        </div>

        {selectedTool && (
          <div className="tool-execution">
            <h3>Execute: {selectedTool}</h3>
            <div className="tool-description">
              <p><strong>Description:</strong> {getSelectedTool()?.description}</p>
            </div>

            <div className="parameters-form">
              <h4>Parameters</h4>
              {Object.entries(toolParameters).map(([key, value]) => (
                <div key={key} className="form-group">
                  <label htmlFor={key}>{key}:</label>
                  <input
                    id={key}
                    type="text"
                    value={value}
                    onChange={(e) => handleParameterChange(key, e.target.value)}
                    placeholder={getSelectedTool()?.parameters[key] || 'Enter value'}
                    className="form-input"
                  />
                  <small className="parameter-hint">
                    {getSelectedTool()?.parameters[key]}
                  </small>
                </div>
              ))}

              <div className="tool-actions">
                <button 
                  onClick={executeTool} 
                  disabled={loading}
                  className="btn btn-primary"
                >
                  {loading ? 'Executing...' : '🚀 Execute Tool'}
                </button>
                <button onClick={resetForm} className="btn btn-secondary">
                  Reset
                </button>
              </div>
            </div>
          </div>
        )}

        {response && (
          <div className="tool-response">
            <h3>Response</h3>
            <div className={`response-content ${response.success ? 'success' : 'error'}`}>
              {response.success ? (
                <div>
                  <p className="response-status">✅ Tool executed successfully</p>
                  <pre className="response-data">
                    {JSON.stringify(response.data, null, 2)}
                  </pre>
                </div>
              ) : (
                <div>
                  <p className="response-status">❌ Tool execution failed</p>
                  <p className="response-error">{response.error}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="mcp-info">
        <h3>ℹ️ About MCP Integration</h3>
        <p>
          MCP (Model Context Protocol) allows your AI assistant to interact with external tools and services.
          This integration enables capabilities like:
        </p>
        <ul>
          <li>📱 WhatsApp messaging</li>
          <li>📅 Google Calendar management</li>
          <li>📁 Google Drive file operations</li>
          <li>📧 Email sending</li>
          <li>⏰ Reminder creation</li>
        </ul>
        <p>
          <strong>Note:</strong> Make sure your MCP server is running and properly configured.
          The server should be accessible at the URL specified in your backend configuration.
        </p>
      </div>
    </div>
  )
}

export default MCPIntegration
