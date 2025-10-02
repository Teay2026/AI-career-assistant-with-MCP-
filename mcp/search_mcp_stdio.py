#!/usr/bin/env python3
import os
import sys
import asyncio
from mcp.server.stdio import stdio_server
from mcp.server import Server
from duckduckgo_search import DDGS

# Create MCP server
app = Server("search-resources-server")

@app.call_tool()
async def websearch_resources(refined_query: str, skill_summary: str = "") -> list[str]:
    """Search for web resources using DuckDuckGo"""
    try:
        print(f"🎯 [Search MCP] Processing: {refined_query}", file=sys.stderr)

        # Initialize DuckDuckGo search
        ddgs = DDGS()
        search_query = f"{refined_query} skills training courses resources"

        # Perform search
        results = ddgs.text(search_query, max_results=3)

        if not results:
            return ["No search results found."]

        # Format results
        formatted_results = []
        for result in results:
            title = result.get('title', 'No title')
            body = result.get('body', 'No description')
            url = result.get('href', 'No URL')
            formatted_results.append(f"**{title}**\n{body}\nSource: {url}\n")

        answer = f"Based on your query '{refined_query}', here are relevant skill resources:\n\n" + "\n".join(formatted_results)

        print(f"✅ [Search MCP] Found {len(results)} results", file=sys.stderr)
        return [answer]

    except Exception as e:
        error_msg = f"[Search Error] {str(e)}"
        print(f"❌ [Search MCP] {error_msg}", file=sys.stderr)
        return [error_msg]

async def main():
    print("🎯 Search MCP Stdio Server starting...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())