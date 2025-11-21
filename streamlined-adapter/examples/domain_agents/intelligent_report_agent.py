#!/usr/bin/env python3
"""
Intelligent Report Agent with MCP Tool Integration
==================================================
This agent uses Claude with MCP tools to provide intelligent financial analysis.
Claude can call yfinance tools as needed based on natural language queries.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import anthropic
import json
import requests as requests

# Add parent directory to path to import nanda_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from nanda_core.core.adapter import NANDA
from tools.financial_tools import (
    get_stock_info, 
    get_historical_prices, 
    compare_stocks,
    FINANCIAL_TOOLS
)

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)
print(f"🔑 Loading .env from: {env_path}")
print(f"🔑 API Key loaded: {os.getenv('ANTHROPIC_API_KEY')[:20]}...")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def call_risk_assessment_agent(stock_data: dict) -> str:
    """
    Call the Risk Assessment Agent via A2A protocol.
    
    Args:
        stock_data: Stock information to assess
    
    Returns:
        Risk assessment response from the specialist agent
    """
    RISK_AGENT_URL = os.getenv("RISK_AGENT_URL", "http://localhost:6004")
    
    try:
        response = requests.post(
            f"{RISK_AGENT_URL}/a2a",
            json={
                "content": {
                    "text": json.dumps(stock_data, indent=2),
                    "type": "text"
                },
                "role": "user",
                "conversation_id": f"risk-{datetime.now().timestamp()}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['parts'][0]['text']
        else:
            return f"Risk agent unavailable (status {response.status_code})"
            
    except Exception as e:
        return f"Could not reach risk assessment agent: {str(e)}"

# Tool function mapping
TOOL_FUNCTIONS = {
    "get_stock_info": get_stock_info,
    "get_historical_prices": get_historical_prices,
    "compare_stocks": compare_stocks,
    "call_risk_assessment_agent": call_risk_assessment_agent
}

def process_message_with_tools(message: str, conversation_id: str) -> str:
    """
    Process messages using Claude with MCP tool calling.
    Claude decides when and how to use financial tools.
    """
    
    print(f"\n📨 [{conversation_id}] User: {message}")
    
    # System prompt for the intelligent agent
    system_prompt = """You are an expert financial investment advisor and analyst. 

You have access to real-time stock market data through tools AND a specialized Risk Assessment Agent. When users ask about stocks, investments, or market analysis:

1. Use the available tools to fetch relevant stock data
2. For investment decisions, ALWAYS consult the Risk Assessment Agent using assess_investment_risk
3. Analyze the data comprehensively including risk factors
4. Provide clear, actionable investment insights
5. Include risk assessments in your recommendations
6. Give specific recommendations with reasoning

The Risk Assessment Agent is a specialist - use it whenever evaluating investment decisions or recommendations.

Always be helpful, accurate, and professional.

IMPORTANT: Include a disclaimer that this is for educational purposes only and not professional financial advice. Please consult with a qualified financial advisor before making any investment decisions."""

    # Start conversation with Claude
    messages = [{"role": "user", "content": message}]
    
    # First API call
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Using Haiku as recommended
        max_tokens=4096,
        system=system_prompt,
        tools=FINANCIAL_TOOLS,
        messages=messages
    )
    
    print(f"🤖 Claude initial response - Stop reason: {response.stop_reason}")
    
    # Handle tool calls in a loop
    while response.stop_reason == "tool_use":
        # Extract tool calls
        tool_results = []
        
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                
                print(f"🔧 Claude is calling tool: {tool_name}")
                print(f"   Input: {json.dumps(tool_input, indent=2)}")
                
                # Execute the tool
                if tool_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[tool_name](**tool_input)
                    print(f"   Result: {json.dumps(result, indent=2)[:200]}...")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })
                else:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps({"error": f"Unknown tool: {tool_name}"})
                    })
        
        # Add assistant response and tool results to conversation
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
        
        # Continue conversation with tool results
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system=system_prompt,
            tools=FINANCIAL_TOOLS,
            messages=messages
        )
        
        print(f"🤖 Claude continued - Stop reason: {response.stop_reason}")
    
    # Extract final text response
    final_response = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_response += block.text
    
    print(f"✅ Final response generated ({len(final_response)} chars)")
    
    return f"[intelligent-report-agent]\n\n{final_response}"


if __name__ == "__main__":
    # Configuration
    AGENT_ID = "intelligent-report-agent"
    PORT = 6003
    PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")
    
    print("🧠 Starting Intelligent Report Agent with MCP Tools...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Port: {PORT}")
    print(f"   Public URL: {PUBLIC_URL}")
    print(f"   Model: claude-haiku-4-5-20251001")
    print(f"   Available Tools: {len(FINANCIAL_TOOLS)}")
    
    # Create NANDA agent
    agent = NANDA(
        agent_id=AGENT_ID,
        agent_logic=process_message_with_tools,
        port=PORT,
        public_url=PUBLIC_URL,
        enable_telemetry=False,
        agent_name="Intelligent Investment Advisor",
        agent_description="AI-powered investment advisor using Claude with real-time market data tools. Provides comprehensive stock analysis and investment recommendations using natural language.",
        agent_capabilities={
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": False,
            "google_a2a_compatible": True,
            "parts_array_format": True,
            "skills": [
                "natural_language_queries",
                "intelligent_stock_analysis",
                "comparative_analysis",
                "investment_recommendations",
                "risk_assessment",
                "portfolio_advice",
                "market_trend_analysis"
            ]
        }
    )
    
    print(f"\n🚀 Intelligent Report Agent running on {PUBLIC_URL}")
    print(f"📡 Endpoint: {PUBLIC_URL}/a2a")
    print("\n💡 Example queries (natural language!):")
    print("   - What's the current price of Apple stock?")
    print("   - Compare AAPL, MSFT, and GOOGL performance over 6 months")
    print("   - Should I buy Tesla stock today?")
    print("   - Get historical prices for NVDA from January to November 2024")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Intelligent Report Agent...")