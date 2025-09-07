# mcp-db-debugger

**Overview**

MCP Database Debugger is a database troubleshooting tool that combines the power of OpenAI's GPT-4 with database interactions through the MCP. It analyzes database errors, executes safe diagnostic queries, and provides actionable recommendations to resolve issues quickly.

**Integration Flow:**

1. User Input → Streamlit UI
2. AI Analysis → OpenAI processes error and generates diagnostic queries
3. Security Check → MCP validates queries are safe(no DML operations)
4. Database Execution → MCP runs approved queries
5. Result Synthesis → Combined AI analysis + database results = actionable recommendations

