# mcp-db-debugger

**Overview**

MCP Database Debugger is a database troubleshooting tool that combines the power of OpenAI's GPT-4 with database interactions through the MCP. It analyzes database errors, executes safe diagnostic queries, and provides actionable recommendations to resolve issues quickly.

**Integration Flow:**

User Input → Streamlit UI
AI Analysis → OpenAI processes error and generates diagnostic queries
Security Check → MCP validates queries are safe(no DML operations)
Database Execution → MCP runs approved queries
Result Synthesis → Combined AI analysis + database results = actionable recommendations

