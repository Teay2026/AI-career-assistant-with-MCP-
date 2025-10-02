from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
import sys
import os
import uvicorn
from fastapi.responses import JSONResponse
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from groq import Groq
from client import clientagt_cache
# from semantic_kernel.functions import kernel_function  # Not needed in simplified version
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # Updated free model



# ------------------ Groq Client ------------------
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


# ------------------ Refiner Plugin ------------------
class QueryRefinerPlugin:
    def __init__(self):
        self.client = get_groq_client()
        self.model = GROQ_MODEL

    async def refine_query(self, query: str) -> str:
        try:
            prompt = f"""
            You are a smart assistant that refines casual or vague user queries into clear, structured intent statements.
            Rephrase the input for clarity and remove filler words.

            Original Query: "{query.strip()}"
            Refined Intent:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a query refiner that restructures raw user questions into clean, intent-focused queries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=60
            )

            refined_query = response.choices[0].message.content.strip()
            print(f"\n[QueryRefinerPlugin] Refined: {refined_query}")
            return refined_query

        except Exception as e:
            fallback = f"Refined intent from user: {query.strip().capitalize()}."
            print(f"[QueryRefinerPlugin] ⚠️ Fallback due to error: {e}")
            return fallback
        

# MCP Client Integration
import subprocess
import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

# ------------------ MCP Client Functions ------------------
class MCPSkillsClient:
    """MCP client for skills analysis server"""

    async def get_skills(self, user_input: str, conversation_id: str) -> str:
        """Call the RAG MCP server for skills analysis"""
        try:
            print(f"🔍 [MCP] Starting RAG server process...")

            # Start the RAG MCP server process
            server_process = await asyncio.create_subprocess_exec(
                "python", "mcp/rag_mcp_stdio.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd="/Users/youness/Desktop/MCP_Project"
            )

            print(f"✅ [MCP] RAG server process started with PID {server_process.pid}")

            # Create MCP client session
            print(f"🔗 [MCP] Creating stdio client...")
            async with stdio_client(server_process.stdout, server_process.stdin) as (read_stream, write_stream):
                print(f"🔗 [MCP] Created stdio streams")

                async with ClientSession(read_stream, write_stream) as session:
                    print(f"🚀 [MCP] Initializing session...")
                    # Initialize the session
                    await session.initialize()
                    print(f"✅ [MCP] Session initialized successfully")

                    print(f"📞 [MCP] Calling get_skills tool with: {user_input}")
                    # Call the get_skills tool
                    result = await session.call_tool(
                        "get_skills",
                        arguments={
                            "user_input": user_input,
                            "conversation_id": conversation_id
                        }
                    )
                    print(f"✅ [MCP] Tool call completed successfully")

                    # Cleanup
                    server_process.terminate()
                    await server_process.wait()
                    print(f"🧹 [MCP] Server process cleaned up")

                    return result.content[0].text if result.content else "No skills found"

        except Exception as e:
            print(f"❌ [MCP Skills Error] {str(e)}")
            return f"[MCP Skills Error] {str(e)}"

class MCPSearchClient:
    """MCP client for web search server"""

    async def search_resources(self, refined_query: str, skill_summary: str = "") -> str:
        """Call the search MCP server for web resources via stdio"""
        try:
            print(f"🔍 [MCP Search] Starting search server process...")

            # Start the search MCP server process
            server_process = await asyncio.create_subprocess_exec(
                "python", "mcp/search_mcp_stdio.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd="/Users/youness/Desktop/MCP_Project"
            )

            print(f"✅ [MCP Search] Server process started with PID {server_process.pid}")

            # Create MCP client session
            print(f"🔗 [MCP Search] Creating stdio client...")
            async with stdio_client(server_process.stdout, server_process.stdin) as (read_stream, write_stream):
                print(f"🔗 [MCP Search] Created stdio streams")

                async with ClientSession(read_stream, write_stream) as session:
                    print(f"🚀 [MCP Search] Initializing session...")
                    # Initialize the session
                    await session.initialize()
                    print(f"✅ [MCP Search] Session initialized successfully")

                    print(f"📞 [MCP Search] Calling websearch_resources tool with: {refined_query}")
                    # Call the websearch_resources tool
                    result = await session.call_tool(
                        "websearch_resources",
                        arguments={
                            "refined_query": refined_query,
                            "skill_summary": skill_summary
                        }
                    )
                    print(f"✅ [MCP Search] Tool call completed successfully")

                    # Cleanup
                    server_process.terminate()
                    await server_process.wait()
                    print(f"🧹 [MCP Search] Server process cleaned up")

                    return result.content[0].text if result.content else "No search results"

        except Exception as e:
            print(f"❌ [MCP Search Error] {str(e)}")
            return f"[MCP Search Error] {str(e)}"

# ------------------ Run Agent ------------------
async def run_mcp_agent(user_input, conversation_id):
    """MCP-based agent using distributed microservices"""
    answer_cache_key = f"answer:{conversation_id}:{user_input}"
    cached_answer = clientagt_cache.get(answer_cache_key)
    if cached_answer:
        return cached_answer

    try:
        groq_client = get_groq_client()

        # Step 1: Refine query
        refine_plugin = QueryRefinerPlugin()
        refined_query = await refine_plugin.refine_query(user_input)

        # Step 2: Get skills from MCP RAG server
        skills_client = MCPSkillsClient()
        skills_result = await skills_client.get_skills(refined_query, conversation_id)

        # Step 3: Get external resources from MCP search server
        search_client = MCPSearchClient()
        search_summary = await search_client.search_resources(refined_query, skills_result)

        # Step 4: Generate response with Groq
        final_prompt = f"""You are a career assistant. Based on the following information, provide helpful career advice:

User Question: {refined_query}
Current Skills: {skills_result}
External Resources: {search_summary}

Provide a concise response with actionable advice."""

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
            max_tokens=500
        )

        agent_response = response.choices[0].message.content.strip()

        # Cache the results
        clientagt_cache.append(conversation_id, "user", user_input)
        clientagt_cache.append(conversation_id, "assistant", agent_response)
        clientagt_cache.set(answer_cache_key, agent_response)

        return agent_response

    except Exception as e:
        return f"Error processing request: {str(e)}"

# Keep old function as fallback
async def run_simple_agent(user_input, conversation_id):
    """Fallback to direct integration if MCP fails"""
    try:
        return await run_mcp_agent(user_input, conversation_id)
    except Exception as e:
        print(f"MCP failed, falling back to direct integration: {e}")
        # Original direct implementation as fallback
        from local_rag import query_local_rag
        from duckduckgo_search import DDGS

        groq_client = get_groq_client()
        refine_plugin = QueryRefinerPlugin()
        refined_query = await refine_plugin.refine_query(user_input)

        skills_result = query_local_rag(refined_query, conversation_id)
        ddgs = DDGS()
        search_results = ddgs.text(f"{refined_query} skills training courses resources", max_results=3)
        search_summary = "\n".join([f"• {r.get('title', 'No title')}: {r.get('href', 'No URL')}" for r in search_results[:3]])

        final_prompt = f"""Career advice based on:
User Question: {refined_query}
Skills: {skills_result}
Resources: {search_summary}"""

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

# ------------------ FastAPI App ------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    Question: str
    conversation_id: str = None

@app.post("/api/agtchat")
async def chat(req: ChatRequest):
    answer = await run_simple_agent(req.Question, req.conversation_id)
    return JSONResponse(content={"answer": answer})

if __name__ == "__main__":
    uvicorn.run("client_agent:app", host="0.0.0.0", port=7081, reload=True)
