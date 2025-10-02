#!/usr/bin/env python3
import os
import sys
import asyncio
import json
from mcp.server.stdio import stdio_server
from mcp.server import Server

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from local_rag import query_local_rag

# Create MCP server
app = Server("rag-skills-server")

@app.call_tool()
async def get_skills(user_input: str, conversation_id: str) -> list[str]:
    """Get skills from local RAG system"""
    try:
        print(f"🎯 [RAG MCP] Processing: {user_input}", file=sys.stderr)
        result = query_local_rag(user_input, conversation_id)
        print(f"✅ [RAG MCP] Result: {len(result)} chars", file=sys.stderr)
        return [result]
    except Exception as e:
        error_msg = f"[RAG Error] {str(e)}"
        print(f"❌ [RAG MCP] {error_msg}", file=sys.stderr)
        return [error_msg]

async def main():
    print("🎯 RAG MCP Stdio Server starting...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())