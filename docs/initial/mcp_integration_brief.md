# MCP Integration Project Brief

This document seeds a project chat for integrating an MCP server with the personal assistant.

---

## Project Goal
- Integrate an MCP server with ChatGPT to extend assistant capabilities (e.g., WhatsApp messaging, Google Drive/Calendar access, automation bridges).

---

## Context
- From Anchor Chat (Assistant v0): sprints, rituals, and distraction logging are defined separately. This project focuses **only** on MCP integration.

- MCP integration is marked **High Priority** in the projects list.

- Anchor Chat retains meta-organization and rituals; this project chat will handle technical details.


---

## Desired Capabilities

1. **Tool Extension via MCP:** Example tools could include `send_whatsapp(to, text)` or Google Drive search.

2. **Transport:** Use SSE or Streamable HTTP for server <-> ChatGPT (stdio is local only).

3. **Connector Setup:** Register server in ChatGPT (Settings → Connectors → Add custom connector → MCP).

4. **Security:** Support headers (Authorization: Bearer …).

5. **Testing Flow:**

   - Prototype minimal MCP server exposing 1–2 tools.

   - Connect to ChatGPT web via custom connector.

   - Run a sprint to test usage.


---

## Tasks / Next Steps

- Draft minimal MCP server (Python or Node) with a single test tool.

- Configure ChatGPT connector (auth, URL, transport).

- Run test sprint inside this project chat.

- Expand to useful tools (WhatsApp messaging, Drive/Calendar).


---

## Continuity

- Keep MCP technical logs here (project chat).

- Report outcomes and key learnings back to Anchor Chat.

