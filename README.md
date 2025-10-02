# 🤖 Skill Assistant AI

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-Free%20Tier-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent **Skill Assistant AI** that analyzes your current skills and provides personalized career development advice. Built with **FastAPI**, **Groq AI**, and **MCP Protocol** for a modern, scalable architecture.

> 🎯 **Perfect for AI Software Engineer portfolios** - Demonstrates RAG, LLM integration, and modern AI architecture patterns.

## ✨ Features

- 🧠 **RAG-powered CV Analysis** - Local skill extraction and analysis
- 🌐 **Real-time Web Search** - DuckDuckGo integration for current resources
- 🤖 **AI-powered Recommendations** - Groq LLM for intelligent career advice
- 🔌 **MCP Protocol** - Modern microservice architecture
- 💰 **100% Free** - No API costs, runs entirely on free tiers
- 🚀 **Demo Ready** - Professional web interface included

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skill-assistant-ai.git
   cd skill-assistant-ai
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

## 🎬 Demo

### Web Interface
Open `demo_ui.html` for a beautiful, modern chat interface with:
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

## 🏗️ Architecture

```
User Question
     ↓
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local RAG     │    │  DuckDuckGo      │    │   Groq AI       │
│  (CV Analysis)  │    │   (Web Search)   │    │ (Intelligence)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
     ↓                          ↓                        ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI + MCP Protocol                      │
└─────────────────────────────────────────────────────────────────┘
     ↓
  AI-Powered Career Advice
```

### Components

1. **🧠 Local RAG System** - Analyzes skills from CV data using keyword matching
2. **🌐 Web Search Integration** - DuckDuckGo API for real-time resource discovery
3. **🤖 Groq AI Integration** - Fast, intelligent response generation
4. **🔌 MCP Protocol** - Modular, extensible architecture
5. **💾 In-Memory Caching** - Conversation persistence without external dependencies

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: Groq (Llama 3.1), Local RAG
- **Search**: DuckDuckGo (free API)
- **Protocol**: MCP (Model Context Protocol)
- **Frontend**: HTML/CSS/JS with Tailwind CSS
- **Architecture**: Microservices, RESTful APIs

## 💰 Cost Breakdown

- **Groq API**: Free tier (30 req/min, 6K tokens/min)
- **DuckDuckGo**: Completely free
- **Hosting**: Self-hosted (no cloud costs)
- **Total**: $0 to run and deploy

## 🔧 Configuration

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
- **Search Keywords**: Modify search terms in `mcp/externl_mcp_server.py`
- **AI Model**: Change `GROQ_MODEL` in `client/client_agent.py`

## 🧪 Testing

Run the test suite:
```bash
# Test API endpoints
curl -X POST http://localhost:7081/api/agtchat \
  -H "Content-Type: application/json" \
  -d '{"Question": "test", "conversation_id": "test"}'

# Test individual components
python local_rag.py
python -c "from duckduckgo_search import DDGS; print('Search OK')"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Why This Project?

Perfect for **AI Software Engineer portfolios** because it demonstrates:

- ✅ **Modern AI Architecture** - RAG, LLM integration, microservices
- ✅ **Production-Ready Code** - FastAPI, proper error handling, caching
- ✅ **Cost-Effective Design** - Runs entirely on free tiers
- ✅ **Real Business Value** - Solves actual career development needs
- ✅ **Full-Stack Skills** - Backend APIs + Frontend UI
- ✅ **Latest Technologies** - MCP Protocol, Groq, modern Python

## 📞 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/yourusername/skill-assistant-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/skill-assistant-ai/discussions)
- 📖 **Documentation**: See `DEMO_GUIDE.md` for detailed usage

---

**Made with ❤️ for the AI community**
