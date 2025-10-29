#!/usr/bin/env python3
"""
Report Summarizer Agent - Synthesizes financial data and generates investment recommendations
"""

import os
import json
import sys
import anthropic
import requests
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path to import nanda_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from nanda_core.core.adapter import NANDA

# Load environment variables
load_dotenv()

# Financial Advisor agent endpoint
ADVISOR_URL = "http://localhost:6001/a2a"

# Initialize Anthropic client
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    client = anthropic.Anthropic(api_key=api_key)
    USE_LLM = True
else:
    print("⚠️  No ANTHROPIC_API_KEY found - using template-based summaries")
    USE_LLM = False

def fetch_financial_data(tickers: list, period: str = "1mo") -> dict:
    """Request financial data from the Financial Advisor agent"""
    try:
        # Format request
        request_text = f"analyze: {','.join(tickers)} {period}"
        
        # Send HTTP POST to Financial Advisor
        payload = {
            "content": {
                "text": request_text,
                "type": "text"
            },
            "role": "user",
            "conversation_id": f"summarizer-{datetime.now().timestamp()}"
        }
        
        print(f"📡 Requesting data from Financial Advisor: {request_text}")
        response = requests.post(ADVISOR_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Parse the nested response structure
            if "parts" in result and len(result["parts"]) > 0:
                text_content = result["parts"][0].get("text", "")
                
                # Remove agent prefix if present (e.g., "[financial-advisor-001] ")
                if text_content.startswith("["):
                    text_content = text_content.split("] ", 1)[1] if "] " in text_content else text_content
                
                # Parse the JSON data
                return json.loads(text_content)
        
        return {"error": f"HTTP {response.status_code}: {response.text}"}
        
    except Exception as e:
        print(f"❌ Error fetching data from Financial Advisor: {e}")
        return {"error": str(e)}

def generate_llm_summary(financial_data: dict) -> str:
    """Generate investment summary using Claude"""
    
    # Create prompt
    prompt = f"""You are a financial analyst assistant. Analyze the following stock market data and provide a comprehensive investment report.

Financial Data:
{json.dumps(financial_data, indent=2)}

Please provide:
1. Executive Summary (2-3 sentences)
2. Individual Stock Analysis (key metrics and trends)
3. Comparative Analysis (if multiple stocks)
4. Investment Recommendations (buy/hold/avoid suggestions with reasoning)
5. Risk Factors to consider

IMPORTANT: Include this disclaimer at the end:
"⚠️ DISCLAIMER: This analysis is for informational purposes only and does not constitute financial advice. We are not Chartered Financial Analysts (CFA) or licensed financial advisors. Always consult with a qualified financial professional before making investment decisions."

Format the report in a clear, professional manner with sections and bullet points."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"❌ Error generating LLM summary: {e}")
        return generate_template_summary(financial_data)

def generate_template_summary(financial_data: dict) -> str:
    """Generate a template-based summary (fallback)"""
    
    stocks = financial_data.get("stocks", {})
    
    report = "# INVESTMENT ANALYSIS REPORT\n\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Stocks Analyzed:** {financial_data.get('total_stocks_analyzed', 0)}\n\n"
    
    report += "## Executive Summary\n\n"
    report += f"Analyzed {len(stocks)} stock(s) to provide investment insights.\n\n"
    
    report += "## Individual Stock Analysis\n\n"
    
    for ticker, data in stocks.items():
        if "error" in data:
            report += f"### {ticker}\n"
            report += f"❌ Analysis failed: {data['error']}\n\n"
            continue
        
        report += f"### {data.get('company_name', ticker)} ({ticker})\n\n"
        report += f"- **Current Price:** ${data.get('current_price', 'N/A')}\n"
        report += f"- **Price Change:** {data.get('price_change_pct', 'N/A')}%\n"
        report += f"- **Sector:** {data.get('sector', 'N/A')}\n"
        report += f"- **P/E Ratio:** {data.get('pe_ratio', 'N/A')}\n"
        report += f"- **52-Week Range:** ${data.get('52_week_low', 'N/A')} - ${data.get('52_week_high', 'N/A')}\n"
        report += f"- **Analyst Recommendation:** {data.get('recommendation', 'N/A').upper()}\n\n"
        
        # Simple recommendation logic
        price_change = data.get('price_change_pct', 0)
        if price_change and price_change > 5:
            report += f"📈 **Trending:** Strong upward momentum ({price_change}%)\n"
        elif price_change and price_change < -5:
            report += f"📉 **Note:** Significant decline ({price_change}%)\n"
        
        report += "\n"
    
    report += "## Investment Recommendations\n\n"
    report += "Based on the analyzed data:\n\n"
    
    for ticker, data in stocks.items():
        if "error" not in data:
            recommendation = data.get('recommendation', 'hold')
            report += f"- **{ticker}:** Consider the analyst recommendation of '{recommendation.upper()}'\n"
    
    report += "\n## Risk Factors\n\n"
    report += "- Market volatility may impact short-term performance\n"
    report += "- Sector-specific risks should be evaluated\n"
    report += "- Economic conditions may affect overall market sentiment\n\n"
    
    report += "---\n\n"
    report += "⚠️ **DISCLAIMER:** This analysis is for informational purposes only and does not constitute financial advice. "
    report += "We are not Chartered Financial Analysts (CFA) or licensed financial advisors. "
    report += "Always consult with a qualified financial professional before making investment decisions.\n"
    
    return report

def process_message(message: str, conversation_id: str) -> str:
    """Process incoming messages and generate reports"""
    text = message.strip()
    
    # Parse request: "summarize: AAPL,GOOGL,MSFT [period]"
    if text.lower().startswith("summarize:"):
        parts = text[10:].strip().split()
        tickers = parts[0].split(",")
        period = parts[1] if len(parts) > 1 else "1mo"
        
        print(f"📊 Generating report for: {', '.join(tickers)}")
        
        # Fetch data from Financial Advisor
        financial_data = fetch_financial_data(tickers, period)
        
        if "error" in financial_data and "stocks" not in financial_data:
            return f"❌ Error: {financial_data['error']}\n\nMake sure the Financial Advisor agent is running on {ADVISOR_URL}"
        
        # Generate summary
        if USE_LLM:
            summary = generate_llm_summary(financial_data)
        else:
            summary = generate_template_summary(financial_data)
        
        return summary
    
    else:
        # Help message
        return """
Report Summarizer Agent - Available Commands:

Summarize stocks and generate investment report:
  summarize: AAPL,GOOGL,MSFT [period]
  Example: summarize: AAPL,TSLA 3mo

This agent will:
1. Request data from the Financial Advisor agent
2. Analyze the financial data
3. Generate a comprehensive investment report with recommendations
4. Include appropriate disclaimers

Supported periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

Note: Financial Advisor must be running on http://localhost:6001
"""

if __name__ == "__main__":
    # Configuration
    AGENT_ID = "report-summarizer-001"
    PORT = 6002
    PUBLIC_URL = os.getenv("PUBLIC_URL_SUMMARIZER", f"http://localhost:{PORT}")
    
    print("📝 Starting Report Summarizer Agent...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Port: {PORT}")
    print(f"   Public URL: {PUBLIC_URL}")
    print(f"   Financial Advisor: {ADVISOR_URL}")
    print(f"   LLM Enabled: {USE_LLM}")
    
    # Create NANDA agent
    agent = NANDA(
        agent_id=AGENT_ID,
        agent_logic=process_message,
        port=PORT,
        public_url=PUBLIC_URL,
        enable_telemetry=False
    )
    
    print(f"\n🚀 Report Summarizer Agent running on {PUBLIC_URL}")
    print(f"📡 Endpoint: {PUBLIC_URL}/a2a")
    print("\n💡 Test with:")
    print(f"   curl -X POST {PUBLIC_URL}/a2a -H 'Content-Type: application/json' \\")
    print(f"   -d '{{\"content\":{{\"text\":\"summarize: AAPL,GOOGL,MSFT\",\"type\":\"text\"}},\"role\":\"user\",\"conversation_id\":\"test\"}}'")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Report Summarizer Agent...")