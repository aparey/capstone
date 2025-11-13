#!/bin/bash
# ==========================================
# NANDA Multi-Agent System Demo
# Agent-to-Agent Communication Test
# ==========================================

echo "🚀 Starting NANDA Agent Communication Demo..."
echo ""

# Test 1: Check both agents are healthy
echo "📊 Step 1: Health Check"
echo "========================"
curl http://97.107.135.236:6001/health
echo ""
curl http://97.107.135.236:6002/health
echo ""
echo ""

# Test 2: Financial Advisor analyzes multiple stocks
echo "💰 Step 2: Financial Advisor - Analyze Top Tech Stocks"
echo "======================================================="
curl -X POST http://97.107.135.236:6001/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "analyze: AAPL,GOOGL,MSFT,TSLA 6mo",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo-investment-001"
  }' | jq '.parts[0].text'
echo ""
echo ""

# Test 3: Report Summarizer requests data and creates report
echo "📈 Step 3: Report Summarizer - Generate Investment Report"
echo "=========================================================="
curl -X POST http://97.107.135.236:6002/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "summarize: AAPL,GOOGL,MSFT 3mo",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo-investment-002"
  }' | jq '.parts[0].text'
echo ""
echo ""

# Test 4: Ask for specific recommendation
echo "🎯 Step 4: Get Today's Buy Recommendations"
echo "==========================================="
curl -X POST http://97.107.135.236:6001/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "single: NVDA 1mo",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo-recommendation"
  }' | jq '.parts[0].text'
echo ""
echo ""

# Test 5: Agent Card Information
echo "📋 Step 5: View Agent Capabilities"
echo "==================================="
echo "Financial Advisor Agent Card:"
curl -s http://97.107.135.236:6001/a2a/agent.json | jq '{name, description, url, capabilities}'
echo ""
echo "Report Summarizer Agent Card:"
curl -s http://97.107.135.236:6002/a2a/agent.json | jq '{name, description, url, capabilities}'
echo ""
echo ""

echo "✅ Demo Complete!"
echo ""
echo "🌐 Access agents in browser:"
echo "   Financial Advisor: http://97.107.135.236:6001/"
echo "   Report Summarizer: http://97.107.135.236:6002/"
