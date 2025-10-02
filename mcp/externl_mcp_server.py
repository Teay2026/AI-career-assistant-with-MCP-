from mcp.server.fastmcp import FastMCP
from fastapi import Request
import os, sys
import uvicorn
from dotenv import load_dotenv
from duckduckgo_search import DDGS
load_dotenv()

# Initialize MCP app
mcp = FastMCP(name="websearch_resources", host="0.0.0.0", port=8080)

# Free DuckDuckGo search - no API key needed
ddgs = DDGS()

# Register tool
@mcp.tool(name="websearch_resources")
async def websearch_resources(refined_query: str, skill_summary: str = "") -> str:
    try:
        # Enhance query with skill context
        search_query = f"{refined_query} skills training courses resources"
        print(f"FastMCP DuckDuckGo search: {search_query}")

        # DuckDuckGo search (free)
        results = ddgs.text(search_query, max_results=5)

        if not results:
            return "No search results found."

        # Format results
        formatted_results = []
        for result in results:
            title = result.get('title', 'No title')
            body = result.get('body', 'No description')
            url = result.get('href', 'No URL')
            formatted_results.append(f"**{title}**\n{body}\nSource: {url}\n")

        answer = f"Based on your query '{refined_query}', here are relevant skill resources:\n\n" + "\n".join(formatted_results)

        print(f"FastMCP Output: Found {len(results)} results")
        return answer

    except Exception as e:
        return f"[DuckDuckGo Search Error] {str(e)}"


# Run server
if __name__ == "__main__":
    try:
        print("🎯 MCP Search Stdio started", file=sys.stderr, flush=True)
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"❌ MCP Search crashed on startup: {e}", flush=True)
