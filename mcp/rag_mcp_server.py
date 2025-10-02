from mcp.server.fastmcp import FastMCP
from fastapi import Request
import os, sys
import uvicorn
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from local_rag import query_local_rag
load_dotenv()

mcp = FastMCP(name="get_skills")

# Register tool
@mcp.tool(name="get_skills")
async def get_skills(user_input: str, conversation_id: str) -> str:
    try:
        print(f"Local RAG get_skills: {user_input}")

        # Use local RAG instead of Azure Function
        answer = query_local_rag(user_input, conversation_id)

        print(f"Local RAG Output: {answer}")
        if not answer or "no relevant skills" in answer.lower():
           return "[NO_CV_SKILLS_FOUND]"
        return answer

    except Exception as e:
        return f"[Local RAG Error] {e}"

# Run server
if __name__ == "__main__":
    try:
        print("🎯 MCP Stdio started", file=sys.stderr, flush=True)
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"❌ MCP crashed on startup: {e}", flush=True)
