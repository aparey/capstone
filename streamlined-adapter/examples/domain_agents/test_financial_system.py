#!/usr/bin/env python3
"""
Test script for Financial Analysis Multi-Agent System
"""

import asyncio
import json
from python_a2a import A2AClient, Message, TextContent, MessageRole

async def test_financial_advisor():
    """Test the Financial Advisor agent directly"""
    print("\n" + "="*60)
    print("TEST 1: Financial Advisor Agent (Direct)")
    print("="*60)
    
    client = A2AClient()
    advisor_url = "http://localhost:6001/a2a"
    
    # Test multiple stock analysis
    message = Message(
        role=MessageRole.USER,
        content=TextContent(text="analyze: AAPL,GOOGL,MSFT 1mo"),
        conversation_id="test-advisor"
    )
    
    try:
        print("📡 Sending request to Financial Advisor...")
        print("   Request: analyze: AAPL,GOOGL,MSFT 1mo")
        
        response = await client.send_message(advisor_url, message)
        
        if isinstance(response.content, TextContent):
            data = json.loads(response.content.text)
            print("\n✅ Response received!")
            print(f"\n📊 Analysis Summary:")
            print(f"   Total stocks: {data.get('total_stocks_analyzed', 0)}")
            print(f"   Successful: {data.get('successful_analyses', 0)}")
            print(f"   Failed: {data.get('failed_analyses', 0)}")
            
            # Show brief info for each stock
            for ticker, stock_data in data.get('stocks', {}).items():
                if 'error' not in stock_data:
                    print(f"\n   {ticker}:")
                    print(f"      Price: ${stock_data.get('current_price', 'N/A')}")
                    print(f"      Change: {stock_data.get('price_change_pct', 'N/A')}%")
                    print(f"      Sector: {stock_data.get('sector', 'N/A')}")
                else:
                    print(f"\n   {ticker}: ❌ {stock_data['error']}")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_report_summarizer():
    """Test the Report Summarizer agent (A2A communication)"""
    print("\n" + "="*60)
    print("TEST 2: Report Summarizer Agent (A2A Communication)")
    print("="*60)
    
    client = A2AClient()
    summarizer_url = "http://localhost:6002/a2a"
    
    # Request summary report
    message = Message(
        role=MessageRole.USER,
        content=TextContent(text="summarize: AAPL,TSLA,NVDA 3mo"),
        conversation_id="test-summarizer"
    )
    
    try:
        print("📡 Sending request to Report Summarizer...")
        print("   Request: summarize: AAPL,TSLA,NVDA 3mo")
        print("\n⏳ This will:")
        print("   1. Contact Financial Advisor agent")
        print("   2. Fetch stock data via A2A")
        print("   3. Generate comprehensive report")
        print("\n   Please wait...")
        
        response = await client.send_message(summarizer_url, message)
        
        if isinstance(response.content, TextContent):
            print("\n✅ Report generated successfully!")
            print("\n" + "─"*60)
            print(response.content.text)
            print("─"*60)
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_single_stock():
    """Test single stock analysis"""
    print("\n" + "="*60)
    print("TEST 3: Single Stock Deep Dive")
    print("="*60)
    
    client = A2AClient()
    advisor_url = "http://localhost:6001/a2a"
    
    message = Message(
        role=MessageRole.USER,
        content=TextContent(text="single: TSLA 6mo"),
        conversation_id="test-single"
    )
    
    try:
        print("📡 Requesting deep dive for TSLA (6 months)...")
        
        response = await client.send_message(advisor_url, message)
        
        if isinstance(response.content, TextContent):
            data = json.loads(response.content.text)
            print("\n✅ Analysis complete!")
            print(f"\n📈 {data.get('company_name', 'N/A')} ({data.get('ticker', 'N/A')})")
            print(f"   Current Price: ${data.get('current_price', 'N/A')}")
            print(f"   6-Month Change: {data.get('price_change_pct', 'N/A')}%")
            print(f"   Sector: {data.get('sector', 'N/A')}")
            print(f"   Market Cap: ${data.get('market_cap', 'N/A'):,}" if isinstance(data.get('market_cap'), (int, float)) else f"   Market Cap: {data.get('market_cap', 'N/A')}")
            print(f"   P/E Ratio: {data.get('pe_ratio', 'N/A')}")
            print(f"   Dividend Yield: {data.get('dividend_yield', 'N/A')}")
            print(f"   Analyst Rec: {data.get('recommendation', 'N/A').upper()}")
            
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("\n🚀 Financial Analysis Multi-Agent System - Test Suite")
    print("="*60)
    print("\n📋 Prerequisites:")
    print("   ✓ Financial Advisor running on port 6001")
    print("   ✓ Report Summarizer running on port 6002")
    print("\nStarting tests...\n")
    
    # Run tests
    test1 = await test_financial_advisor()
    await asyncio.sleep(2)
    
    test2 = await test_single_stock()
    await asyncio.sleep(2)
    
    test3 = await test_report_summarizer()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Financial Advisor Direct:        {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Single Stock Analysis:           {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Report Summarizer (A2A):         {'✅ PASS' if test3 else '❌ FAIL'}")
    print("="*60)
    
    if test1 and test2 and test3:
        print("\n🎉 All tests passed! Your multi-agent system is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Check that both agents are running.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted")