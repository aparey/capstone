# NANDA - Intelligent Investment Advisor

## 🧠 AI-Powered Financial Analysis with Natural Language & MCP Tools

A sophisticated AI agent system that uses Claude with Model Context Protocol (MCP) to provide intelligent stock market analysis and investment recommendations through natural language interaction.

---

## 🌟 Live Demo

**🌐 Web Interface:** http://97.107.135.236:5001

**Try asking:**
- "What's the current price of Apple stock?"
- "Compare Apple, Microsoft, and Google over 6 months"
- "Should I invest in NVIDIA today?"
- "I have $10,000 to invest in tech stocks. What should I buy?"

**Direct API Access:** http://97.107.135.236:6003

---

## ✨ Key Features

### 🗣️ Natural Language Processing
- No rigid command syntax required
- Ask questions naturally like talking to a human advisor
- Claude understands context and intent

### 🔧 MCP Tool Integration
- Claude intelligently decides which tools to call
- Dynamic tool selection based on query context
- Multi-tool orchestration for complex analyses

### 📊 Real-Time Market Data
- Live stock prices via yfinance
- Historical data analysis
- Multi-stock comparisons
- Technical indicators and metrics

### 🎨 Beautiful Web Interface
- Interactive chat UI
- Real-time agent status
- Clickable example queries
- Color-coded financial metrics
- Mobile-friendly design

### ☁️ Cloud Deployment
- Running on Linode infrastructure
- A2A protocol compliance
- MongoDB Atlas integration
- 24/7 availability

---

## 🏗️ Architecture

### System Design
```
┌──────────────────────────────────────────────┐
│          User (Web Browser / API)             │
└───────────────────┬──────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│         Web UI (Flask - Port 5001)            │
│     Beautiful chat interface for users        │
└───────────────────┬──────────────────────────┘
                    │ HTTP/JSON
                    ▼
┌──────────────────────────────────────────────┐
│   Intelligent Report Agent (Port 6003)        │
│         Claude Haiku 4.5 + MCP Tools          │
│                                               │
│  ┌─────────────────────────────────────┐    │
│  │      MCP Financial Tools             │    │
│  │                                       │    │
│  │  🔧 get_stock_info()                 │    │
│  │     • Current price & metrics        │    │
│  │     • Market cap, P/E ratio          │    │
│  │     • Volume, trends                 │    │
│  │                                       │    │
│  │  🔧 get_historical_prices()          │    │
│  │     • Custom date ranges             │    │
│  │     • Price history analysis         │    │
│  │                                       │    │
│  │  🔧 compare_stocks()                 │    │
│  │     • Multi-stock comparison         │    │
│  │     • Relative performance           │    │
│  └─────────────────────────────────────┘    │
│                                               │
│  Decision Flow:                               │
│  1. Understand user query                    │
│  2. Decide which tool(s) to call             │
│  3. Execute tool calls                       │
│  4. Analyze results                          │
│  5. Provide intelligent insights             │
└───────────────────┬──────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   yfinance API       │
         │   (Yahoo Finance)    │
         └──────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   MongoDB Atlas      │
         │   (Telemetry)        │
         └──────────────────────┘
```

### Why MCP Instead of Two Agents?

**Previous Architecture (Two Agents):**
- ❌ Financial Advisor was just a data wrapper (no AI inference)
- ❌ Hardcoded command parsing (`analyze:`, `single:`)
- ❌ Inflexible query syntax
- ❌ Not truly "intelligent"

**Current Architecture (Agent + MCP Tools):**
- ✅ Single intelligent agent with reasoning
- ✅ Claude decides which tools to use
- ✅ Natural language queries
- ✅ True agentic behavior
- ✅ More cost-effective (Haiku vs Sonnet)

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| AI Model | Claude Haiku 4.5 | Cost-effective intelligence |
| Framework | Custom NANDA + python-a2a | Agent infrastructure |
| Tools | MCP (Model Context Protocol) | Tool calling interface |
| Market Data | yfinance | Real-time stock data |
| Web Framework | Flask | HTTP server & UI |
| Database | MongoDB Atlas | Telemetry & metadata |
| Deployment | Linode VPS | Cloud hosting |
| Frontend | HTML/CSS/JavaScript | Interactive UI |

---

## 📖 Usage Examples

### Example 1: Simple Price Query
```
User: "What's Tesla's stock price?"

Agent Process:
🤖 Claude reads query
🔧 Calls: get_stock_info(ticker="TSLA", period="3mo")
📊 Receives: Current price, metrics, trends
💡 Analyzes: Performance, valuation, recommendation
📝 Responds: "Tesla (TSLA) is currently trading at $XXX..."
```

### Example 2: Comparative Analysis
```
User: "Compare Apple, Microsoft, and Google. Which should I buy?"

Agent Process:
🤖 Claude understands: needs comparison of 3 stocks
🔧 Calls: compare_stocks(["AAPL", "MSFT", "GOOGL"], "3mo")
📊 Receives: Performance data for all three
💡 Analyzes: Relative strengths, valuations, trends
📝 Responds: Detailed comparison with recommendation
```

### Example 3: Historical Analysis
```
User: "Show me NVIDIA's performance from January to October 2024"

Agent Process:
🤖 Claude identifies: specific date range needed
🔧 Calls: get_historical_prices("NVDA", "2024-01-01", "2024-10-31")
📊 Receives: Historical price data
💡 Analyzes: Trends, volatility, key events
📝 Responds: Performance summary with insights
```

---

## 🚀 Quick Start

### For Code Reviewers

**Fastest Way (Live Demo):**
1. Open http://97.107.135.236:5001
2. Click any example query
3. See the agent work in real-time!

**API Testing:**
```bash
curl -X POST http://97.107.135.236:6003/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"What stocks should I buy?","type":"text"},"role":"user","conversation_id":"demo"}'
```

**Automated Demo:**
```bash
./demo_agents.sh
```

### For Local Development

See **Installation & Setup** section above.

---

## 📊 Performance & Costs

### API Usage
- **Model:** Claude Haiku 4.5 (most cost-effective)
- **Cost per query:** ~$0.001-0.005 depending on complexity
- **Tool calls:** Multiple tool calls per complex query
- **Response time:** 2-5 seconds average

### Infrastructure
- **Server:** Linode Nanode 1GB ($5/month)
- **Database:** MongoDB Atlas Free Tier (M0)
- **Uptime:** On-demand (can be always-on if needed)

---

## 🔐 Security & Configuration

### Environment Variables

Required in `.env` file:
```env
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-api03-...

# MongoDB (optional for local)
MONGODB_URI=mongodb+srv://...
MONGODB_TELEMETRY_URI=mongodb+srv://...
MONGODB_AGENTFACTS_URI=mongodb+srv://...
```

### Firewall Configuration (Linode)
- Port 6003: Intelligent agent A2A endpoint
- Port 5001: Web UI
- All ports: UFW configured

---

## 🎓 Academic Context

**Course:** ALY 6980 - Advanced AI Systems  
**Institution:** Northeastern University  
**Semester:** Fall 2025  

### Project Objectives

✅ Implement multi-agent architecture  
✅ Deploy to cloud infrastructure  
✅ Integrate real-time data sources  
✅ Use cutting-edge AI capabilities (MCP)  
✅ Create production-ready system  
✅ Professional documentation  

### Key Innovations

1. **MCP Tool Integration** - Among first student projects to use Model Context Protocol
2. **Natural Language Interface** - No rigid command syntax
3. **Agentic AI** - Claude makes intelligent decisions about tool usage
4. **Production Deployment** - Real cloud infrastructure, not just localhost

---

## 🐛 Troubleshooting

### Agent Not Responding
```bash
# Check if agent is running
ssh root@97.107.135.236 'ps aux | grep intelligent | grep -v grep'

# Check logs
ssh root@97.107.135.236 'tail -50 /root/NEST/logs/intelligent-agent.log'

# Restart if needed
ssh root@97.107.135.236
cd /root/NEST/streamlined-adapter/examples/domain_agents
source ../../venv/bin/activate
pkill -f intelligent
PUBLIC_URL="http://97.107.135.236:6003" python3 intelligent_report_agent.py > /root/NEST/logs/intelligent-agent.log 2>&1 &
```

### Web UI Not Loading
```bash
# Check web UI status
ssh root@97.107.135.236 'ps aux | grep web_ui | grep -v grep'

# Check logs
ssh root@97.107.135.236 'tail -50 /root/NEST/logs/web-ui.log'
```

### API Key Issues
- Verify key is valid in Anthropic console
- Check `.env` file has correct key
- Ensure no extra spaces or quotes around key

---

## 📚 Additional Resources

- **Anthropic API Docs:** https://docs.anthropic.com/
- **MCP Documentation:** https://modelcontextprotocol.io/
- **python-a2a:** https://github.com/chrishayuk/python-a2a
- **yfinance:** https://github.com/ranaroussi/yfinance
- **Deployment Guide:** See `DEPLOYMENT.md` in this repository

---

## 🎯 Next Steps

1. **Test the live demo** at http://97.107.135.236:5001
2. **Review the code** - start with `intelligent_report_agent.py`
3. **Run locally** to experiment with modifications
4. **Explore MCP tools** in `tools/financial_tools.py`
5. **Check deployment scripts** for production setup

---

## 💬 Contact

**Aditya Parey**  
📧 parey.a@northeastern.edu  
🔗 GitHub: [@aparey](https://github.com/aparey)  
🏫 Northeastern University - Master's in Analytics

---

**⭐ If you find this project helpful, please star the repository!**

---

*Built with ❤️ using Claude AI, Python, and lots of coffee ☕*