# NANDA Agent Deployment - Code Review Guide

## Quick Start for Reviewers

### Deployed Agents (Live)
- **Financial Advisor:** http://97.107.135.236:6001/
- **Report Summarizer:** http://97.107.135.236:6002/

### Test the Agents

#### Option 1: Run the demo script
```bash
python demo.py
```

#### Option 2: Test via curl
```bash
# Test Financial Advisor
curl -X POST http://97.107.135.236:6001/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"single: AAPL 3mo","type":"text"},"role":"user","conversation_id":"review-test"}'

# Test Report Summarizer  
curl -X POST http://97.107.135.236:6002/a2a \
  -H "Content-Type: application/json" \
  -d '{"content":{"text":"summarize: AAPL,GOOGL 3mo","type":"text"},"role":"user","conversation_id":"review-test"}'
```

## Key Files
- `streamlined-adapter/examples/domain_agents/financial_advisor_agent.py` - Stock analysis agent
- `streamlined-adapter/examples/domain_agents/report_summarizer_agent.py` - Report generation agent
- `streamlined-adapter/nanda_core/core/adapter.py` - NANDA framework core
- `streamlined-adapter/nanda_core/core/agent_bridge.py` - A2A protocol bridge
- `demo.py
