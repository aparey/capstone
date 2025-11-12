#!/usr/bin/env python3
"""
Financial Advisor Agent - Uses yfinance for market data and analysis
"""

import os
import json
import sys
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add parent directory to path to import nanda_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from nanda_core.core.adapter import NANDA

# Load environment variables
load_dotenv()

def get_stock_data(ticker: str, period: str = "1mo") -> dict:
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical data
        hist = stock.history(period=period)
        
        # Get company info
        info = stock.info
        
        # Calculate key metrics
        current_price = hist['Close'].iloc[-1] if not hist.empty else None
        price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100) if not hist.empty else None
        
        # Get volume data
        avg_volume = hist['Volume'].mean() if not hist.empty else None
        
        return {
            "ticker": ticker.upper(),
            "current_price": round(float(current_price), 2) if current_price else None,
            "price_change_pct": round(float(price_change), 2) if price_change else None,
            "period": period,
            "avg_volume": int(avg_volume) if avg_volume else None,
            "company_name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "recommendation": info.get("recommendationKey", "N/A"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "ticker": ticker,
            "timestamp": datetime.now().isoformat()
        }

def analyze_multiple_stocks(tickers: list, period: str = "1mo") -> dict:
    """Analyze multiple stocks and provide comparative analysis"""
    results = {}
    
    for ticker in tickers:
        print(f"📊 Analyzing {ticker}...")
        results[ticker] = get_stock_data(ticker, period)
    
    # Generate summary
    summary = {
        "total_stocks_analyzed": len(tickers),
        "successful_analyses": sum(1 for r in results.values() if "error" not in r),
        "failed_analyses": sum(1 for r in results.values() if "error" in r),
        "analysis_timestamp": datetime.now().isoformat(),
        "stocks": results
    }
    
    return summary

def process_message(message: str, conversation_id: str) -> str:
    """Process incoming messages and return analysis"""
    text = message.strip()
    
    # Parse the request
    if text.lower().startswith("analyze:"):
        # Format: "analyze: AAPL,GOOGL,MSFT [period]"
        parts = text[8:].strip().split()
        tickers = parts[0].split(",")
        period = parts[1] if len(parts) > 1 else "1mo"
        
        print(f"📈 Received analysis request for: {', '.join(tickers)}")
        
        # Perform analysis
        analysis = analyze_multiple_stocks(tickers, period)
        
        # Format response
        return json.dumps(analysis, indent=2)
    
    elif text.lower().startswith("single:"):
        # Format: "single: AAPL [period]"
        parts = text[7:].strip().split()
        ticker = parts[0]
        period = parts[1] if len(parts) > 1 else "1mo"
        
        print(f"📊 Single stock analysis for: {ticker}")
        
        data = get_stock_data(ticker, period)
        return json.dumps(data, indent=2)
    
    else:
        # Help message
        return """
Financial Advisor Agent - Available Commands:

1. Multiple Stock Analysis:
   analyze: AAPL,GOOGL,MSFT [period]
   Example: analyze: AAPL,GOOGL 3mo

2. Single Stock Analysis:
   single: AAPL [period]
   Example: single: TSLA 6mo

Supported periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
"""

if __name__ == "__main__":
    # Configuration
    AGENT_ID = "financial-advisor-001"
    PORT = 6001
    PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")
    
    print("💰 Starting Financial Advisor Agent...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Port: {PORT}")
    print(f"   Public URL: {PUBLIC_URL}")
    
    # Create NANDA agent
    agent = NANDA(
        agent_id=AGENT_ID,
        agent_logic=process_message,
        port=PORT,
        public_url=PUBLIC_URL,
        enable_telemetry=False,
        agent_name="Financial Advisor",
        agent_description="Financial Advisor specializing in stock analysis and investment insights",
        agent_capabilities={
        "streaming": True,
        "pushNotifications": False,
        "stateTransitionHistory": False,
        "google_a2a_compatible": True,
        "parts_array_format": True,
        "skills": [
            "stock_analysis",
            "market_research",
            "financial_modeling",
            "trend_analysis",
            "yfinance_integration"
        ]
      }
    )

    print(f"\n🚀 Financial Advisor Agent running on {PUBLIC_URL}")
    print(f"📡 Endpoint: {PUBLIC_URL}/a2a")
    print("\n💡 Test with:")
    print(f"   curl -X POST {PUBLIC_URL}/a2a -H 'Content-Type: application/json' \\")
    print(f"   -d '{{\"content\":{{\"text\":\"analyze: AAPL,GOOGL,MSFT\",\"type\":\"text\"}},\"role\":\"user\",\"conversation_id\":\"test\"}}'")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Financial Advisor Agent...")
