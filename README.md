# AI Career Assistant with Distributed MCP Microservices

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-Free%20Tier-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI career assistant that analyzes your current skills and provides personalized career development advice. Built with **FastAPI**, **Groq AI**, and **MCP Protocol** for a modern, distributed microservices architecture.

## Features

- **RAG-powered CV Analysis** - Local skill extraction and analysis
- **Real-time Web Search** - DuckDuckGo integration for current resources
- **AI-powered Recommendations** - Groq LLM for intelligent career advice
- **MCP Protocol** - Distributed microservice architecture

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Teay2026/AI-career-assistant-with-MCP-.git
   cd AI-career-assistant-with-MCP-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

4. **Start the server**
   ```bash
   python client/client_agent.py
   ```

5. **Open the demo interface**
   - Open `demo_ui.html` in your browser
   - Or use the API directly at `http://localhost:7081`

## Demo

### Web Interface
Open `demo_ui.html` for a modern chat interface with:
- Real-time AI conversations
- Pre-built example questions
- Professional UI with animations
- Mobile-responsive design

### Example Questions
- "What programming skills do I have?"
- "How can I become a data scientist?"
- "What cloud computing skills should I learn?"
- "How do I improve my machine learning expertise?"

### API Usage
```bash
curl -X POST http://localhost:7081/api/agtchat \
  -H "Content-Type: application/json" \
  -d '{"Question": "What skills should I learn for DevOps?", "conversation_id": "demo"}'
```

## Architecture

```
User Question
     ↓
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ MCP RAG Server  │    │ MCP Search Server│    │   Groq AI       │
│ (Skills Analysis)│    │ (Web Resources)  │    │ (Intelligence)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
     ↓                          ↓                        ↓
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Client Orchestrator                       │
│                (MCP Protocol Communication)                     │
└─────────────────────────────────────────────────────────────────┘
     ↓
  AI-Powered Career Advice
```

### Components

1. **MCP RAG Server** - Analyzes skills from CV data using keyword matching
2. **MCP Search Server** - DuckDuckGo API for real-time resource discovery
3. **FastAPI Client** - Orchestrates MCP services and Groq AI integration
4. **MCP Protocol** - Modular, extensible microservice communication
5. **Fallback System** - Resilient architecture with automatic fallback

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: Groq (Llama 3.1), Local RAG
- **Search**: DuckDuckGo (free API)
- **Protocol**: MCP (Model Context Protocol)
- **Frontend**: HTML/CSS/JS with Tailwind CSS
- **Architecture**: Distributed microservices, RESTful APIs

## Cost Breakdown

- **Groq API**: Free tier (30 req/min, 6K tokens/min)
- **DuckDuckGo**: Completely free
- **Hosting**: Self-hosted (no cloud costs)
- **Total**: $0 to run and deploy

## Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
PORT=7081
HOST=0.0.0.0
```

### Customization
- **Skills Database**: Edit `local_rag.py` to add your own skill sets
- **MCP Servers**: Modify `mcp/rag_mcp_stdio.py` and `mcp/search_mcp_stdio.py`
- **AI Model**: Change `GROQ_MODEL` in `client/client_agent.py`


