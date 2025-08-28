# Plasmo Automation Scripts Organization Guide

This document provides a comprehensive overview of how Python automation scripts are organized within the Plasmo project directory.

## 📍 **Directory Structure**

The Plasmo project is located at: `/Users/MikeWolf/Projects/Plasmo`

## 🗂️ **Primary Organization Patterns**

### 1. **Root Directory - Individual Automation Scripts**
Most standalone Python automation scripts are stored directly in the root of the Plasmo directory.

**Location**: `/Users/MikeWolf/Projects/Plasmo/`

#### **Key Automation Scripts:**
- [`auto_click_automation.py`](https://github.com/eldrgeek/Plasmo/blob/main/auto_click_automation.py) - Automated clicking functionality
- [`auto_click_simple.py`](https://github.com/eldrgeek/Plasmo/blob/main/auto_click_simple.py) - Simplified clicking automation
- [`bolt_automation_mcp.py`](https://github.com/eldrgeek/Plasmo/blob/main/bolt_automation_mcp.py) - Bolt integration via MCP
- [`bolt_automation_playwright.py`](https://github.com/eldrgeek/Plasmo/blob/main/bolt_automation_playwright.py) - Bolt integration via Playwright
- [`chrome_debug_launcher.py`](https://github.com/eldrgeek/Plasmo/blob/main/chrome_debug_launcher.py) - Chrome debugging launcher
- [`cursor_ai_injector.py`](https://github.com/eldrgeek/Plasmo/blob/main/cursor_ai_injector.py) - Cursor AI injection automation
- [`discord_export_automation.py`](https://github.com/eldrgeek/Plasmo/blob/main/discord_export_automation.py) - Discord export automation
- [`gemini_native_injector.py`](https://github.com/eldrgeek/Plasmo/blob/main/gemini_native_injector.py) - Gemini integration
- [`yabai_mapper.py`](https://github.com/eldrgeek/Plasmo/blob/main/yabai_mapper.py) - Yabai window management automation

### 2. **Organized Service Structure**
Reusable automation services are organized in a dedicated services directory.

**Location**: `/Users/MikeWolf/Projects/Plasmo/shared/python-common/services/`

#### **Service Files:**
- [`chrome_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/chrome_service.py) - Chrome automation service
- [`mcp_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/mcp_service.py) - MCP protocol service
- [`mcp_tester_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/mcp_tester_service.py) - MCP testing service
- [`plasmo_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/plasmo_service.py) - Core Plasmo service
- [`service_base.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/service_base.py) - Base service class
- [`socketio_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/socketio_service.py) - Socket.IO service
- [`testing_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/testing_service.py) - Testing automation service
- [`tunneling_service.py`](https://github.com/eldrgeek/Plasmo/blob/main/shared/python-common/services/tunneling_service.py) - Tunneling automation service

### 3. **Package-Based Organization**
Complex automation modules are organized into packages.

**Location**: `/Users/MikeWolf/Projects/Plasmo/packages/`

#### **Key Packages:**
- [`mcp-server/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/mcp-server) - MCP server implementation
- [`firebase-chat/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/firebase-chat) - Firebase chat automation
- [`dashboard-framework/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/dashboard-framework) - Dashboard automation framework
- [`chrome-extension/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/chrome-extension) - Chrome extension automation
- [`socketio-server/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/socketio-server) - Socket.IO server automation
- [`testing-framework/`](https://github.com/eldrgeek/Plasmo/tree/main/packages/testing-framework) - Testing automation framework

### 4. **Agent System**
AI agent automation system for complex workflows.

**Location**: `/Users/MikeWolf/Projects/Plasmo/agents/`

#### **Agent Files:**
- [`agent_spawner.py`](https://github.com/eldrgeek/Plasmo/blob/main/agents/agent_spawner.py) - Agent spawning automation
- [`agent_templates/`](https://github.com/eldrgeek/Plasmo/tree/main/agents/agent_templates) - Agent template definitions
- [`founder_agent.md`](https://github.com/eldrgeek/Plasmo/blob/main/agents/founder_agent.md) - Founder agent configuration
- [`project_creation_template.md`](https://github.com/eldrgeek/Plasmo/blob/main/agents/project_creation_template.md) - Project creation automation
- [`recruiter_agent.md`](https://github.com/eldrgeek/Plasmo/blob/main/agents/recruiter_agent.md) - Recruiter agent configuration

## 🎯 **Usage Guidelines**

### **Where to Place New Scripts:**

1. **Individual Automation Scripts** → Root directory (`/Users/MikeWolf/Projects/Plasmo/`)
2. **Reusable Services** → `shared/python-common/services/`
3. **Complex Modules** → `packages/`
4. **AI Agent Automations** → `agents/`

### **Naming Conventions:**
- Individual scripts: `{function}_automation.py`
- Services: `{function}_service.py`
- Packages: `{function}-{type}/`

## 🔗 **Related Documentation**

- [Plasmo README](https://github.com/eldrgeek/Plasmo/blob/main/README.md)
- [MCP Testing Checklist](https://github.com/eldrgeek/Plasmo/blob/main/MCP_TESTING_CHECKLIST.md)
- [Service Orchestration Guide](https://github.com/eldrgeek/Plasmo/blob/main/SERVICE_ORCHESTRATION_README.md)
- [Bolt Integration Guide](https://github.com/eldrgeek/Plasmo/blob/main/BOLT_INTEGRATION_GUIDE.md)

## 📝 **Notes**

- There is **no single dedicated directory** specifically for "individual automations"
- The organization follows a **hybrid approach** based on complexity and reusability
- Most standalone automation scripts are in the root directory for easy access
- Complex, reusable automation services are properly organized in the services directory
- Package-based organization is used for larger automation frameworks

---

*Last Updated: August 28, 2025*  
*Location: `/Users/MikeWolf/Projects/AI Copilot/docs/plasmo-automation-scripts-guide.md`*
