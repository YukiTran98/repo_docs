# CHANGELOG — agent_basic

## [update] 2026-04-12

**Cập nhật metadata docs.**

- CHANGELOG [init]: thêm `Tags: AI, Multi-Agent, MCP, FastAPI, WebSocket`

---

## [init] 2026-04-12

**Docs khởi tạo lần đầu.**

- Analyzed 8 files · ~380 lines
- Stack: Python, openai-agents, FastMCP, LangChain, FAISS, FastAPI, httpx
- Tags: AI, Multi-Agent, MCP, FastAPI, WebSocket
- 14 functions/classes mapped
- Top functions: `MCPAgent.run`, `init_main_agent`, `start_chat`
- Pattern: Multi-Agent Orchestration — 1 Main Agent + 3 MCP-backed sub-agents
- Hai entry points: CLI REPL (`main.py`) và Web UI WebSocket (`web_main_agent.py`)
