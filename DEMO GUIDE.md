# NANDA Multi-Agent System - Code Review Guide

## Overview
NANDA is a multi-agent financial intelligence system with two specialized agents:
- **Financial Advisor Agent** - Analyzes stocks using yfinance and Claude API
- **Report Summarizer Agent** - Generates comprehensive investment reports

## Architecture
- **Framework:** Custom NANDA framework built on python-a2a protocol
- **Deployment:** Linode cloud server (Ubuntu 22.04)
- **Database:** MongoDB Atlas for agent metadata and telemetry
- **AI:** Anthropic Claude API (Sonnet 4)

---

## Option 1: Test Live Deployed Agents (Easiest)

**Note:** Agents may not be running 24/7 to conserve API costs.

If agents are live, run:
```bash
./demo_agents.sh
```

Or test manually:
```bash
# Health check
curl http://97.107.135.236:6001/health
curl http://97.107.135.236:6002/health

# Analyze stocks
curl -X POST http://97.107.135.236:6001/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"single: AAPL 3mo","type":"text"},"role":"user","conversation_id":"test"}'
```

**Web Interface:**
- Financial Advisor: http://97.107.135.236:6001/
- Report Summarizer: http://97.107.135.236:6002/

---

## Option 2: Run Locally (Full Setup Required)

### Prerequisites
- Python 3.10+
- Anthropic API key
- MongoDB Atlas account (or local MongoDB)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/aparey/capstone.git
cd capstone/streamlined-adapter
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install anthropic flask requests pyyaml python-a2a pymongo yfinance python-dotenv pandas numpy
```

4. **Configure environment**
Create `.env` file in `streamlined-adapter/` directory:
```
ANTHROPIC_API_KEY=your-api-key-here
MONGODB_URI=your-mongodb-connection-string
```

5. **Run the agents**

Terminal 1 - Financial Advisor:
```bash
cd examples/domain_agents
python3 financial_advisor_agent.py
```

Terminal 2 - Report Summarizer:
```bash
cd examples/domain_agents
python3 report_summarizer_agent.py
```

6. **Test locally**
```bash
# Financial Advisor (default port 6001)
curl -X POST http://localhost:6001/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"single: AAPL 3mo","type":"text"},"role":"user","conversation_id":"local-test"}'

# Report Summarizer (default port 6002)
curl -X POST http://localhost:6002/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"summarize: AAPL,GOOGL 3mo","type":"text"},"role":"user","conversation_id":"local-test"}'
```

---

## Option 3: Code Review Without Running

### Key Files to Review

1. **Agent Implementation**
   - `streamlined-adapter/examples/domain_agents/financial_advisor_agent.py`
   - `streamlined-adapter/examples/domain_agents/report_summarizer_agent.py`

2. **Core Framework**
   - `streamlined-adapter/nanda_core/core/adapter.py` - NANDA wrapper class
   - `streamlined-adapter/nanda_core/core/agent_bridge.py` - A2A protocol bridge

3. **Configuration**
   - `my-nanda-agents-config.json` - Agent deployment configuration
   - `deploy-to-linode-test.sh` - Deployment automation script

### Architecture Highlights

**Agent Communication Flow:**
```
User Request
    ↓
Report Summarizer Agent (Port 6002)
    ↓ (A2A Protocol)
Financial Advisor Agent (Port 6001)
    ↓ (yfinance API)
Real-time Stock Data
    ↓
Financial Analysis
    ↓ (A2A Response)
Report Summarizer
    ↓
Comprehensive Report
```

**Technology Stack:**
- Python 3.12
- Anthropic Claude API (Sonnet 4.5)
- python-a2a (Agent-to-Agent protocol)
- yfinance (Stock market data)
- Flask (Web server)
- MongoDB Atlas (Data persistence)

---

## Video Demo 
https://drive.google.com/file/d/1Do5dqSGZRgCndO3Ctud6qP85QMXP3GQN/view?usp=sharing

---

## Contact
For questions or to request live agent access:
- Email: parey.a@northeastern.edu
- Note: Agents run on-demand to manage API costs
