"""
NANDA Agent Demo Script
=======================
Tests the deployed Financial Advisor and Report Summarizer agents.

Requirements:
- Both agents must be running on the Linode server
- No additional setup needed - just run this script
"""

import requests
import json
from datetime import datetime

# Configuration
FINANCIAL_ADVISOR_URL = "http://97.107.135.236:6001"
REPORT_SUMMARIZER_URL = "http://97.107.135.236:6002"

def test_agent_health(agent_name, url):
    """Test if an agent is responding"""
    print(f"\n{'='*60}")
    print(f"Testing {agent_name}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {agent_name} is healthy and responding")
            return True
        else:
            print(f"❌ {agent_name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {agent_name} is not reachable: {e}")
        return False

def get_agent_card(agent_name, url):
    """Retrieve and display agent card"""
    try:
        response = requests.get(f"{url}/a2a/agent.json", timeout=5)
        if response.status_code == 200:
            card = response.json()
            print(f"\n📋 {agent_name} Agent Card:")
            print(f"   Name: {card.get('name')}")
            print(f"   Description: {card.get('description')}")
            print(f"   URL: {card.get('url')}")
            print(f"   Capabilities: {list(card.get('capabilities', {}).keys())}")
            return True
    except Exception as e:
        print(f"❌ Could not retrieve agent card: {e}")
        return False

def test_stock_analysis(ticker="AAPL", period="3mo"):
    """Test Financial Advisor with stock analysis"""
    print(f"\n{'='*60}")
    print(f"Testing Financial Advisor - Stock Analysis")
    print(f"{'='*60}")
    print(f"Analyzing {ticker} for {period}...")
    
    try:
        response = requests.post(
            f"{FINANCIAL_ADVISOR_URL}/a2a",
            headers={"Content-Type": "application/json"},
            json={
                "content": {
                    "text": f"single: {ticker} {period}",
                    "type": "text"
                },
                "role": "user",
                "conversation_id": f"demo-{datetime.now().isoformat()}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            text_response = result['parts'][0]['text']
            
            # Parse the response
            print(f"\n✅ Financial Analysis Results:")
            if 'ticker' in text_response:
                lines = text_response.split('\n')
                for line in lines[:15]:  # Show first 15 lines
                    if line.strip():
                        print(f"   {line}")
                print("   ...")
            else:
                print(f"   {text_response[:500]}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing stock analysis: {e}")
        return False

def test_report_generation(tickers="AAPL,GOOGL", period="3mo"):
    """Test Report Summarizer"""
    print(f"\n{'='*60}")
    print(f"Testing Report Summarizer")
    print(f"{'='*60}")
    print(f"Requesting report for {tickers} ({period})...")
    
    try:
        response = requests.post(
            f"{REPORT_SUMMARIZER_URL}/a2a",
            headers={"Content-Type": "application/json"},
            json={
                "content": {
                    "text": f"summarize: {tickers} {period}",
                    "type": "text"
                },
                "role": "user",
                "conversation_id": f"demo-{datetime.now().isoformat()}"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            text_response = result['parts'][0]['text']
            print(f"\n✅ Report Summarizer Response:")
            print(f"   {text_response[:500]}")
            if len(text_response) > 500:
                print("   ...")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing report generation: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("NANDA Multi-Agent System Demo")
    print("Testing deployed agents on Linode")
    print("="*60)
    
    results = []
    
    # Test 1: Health checks
    results.append(test_agent_health("Financial Advisor", FINANCIAL_ADVISOR_URL))
    results.append(test_agent_health("Report Summarizer", REPORT_SUMMARIZER_URL))
    
    # Test 2: Agent cards
    results.append(get_agent_card("Financial Advisor", FINANCIAL_ADVISOR_URL))
    results.append(get_agent_card("Report Summarizer", REPORT_SUMMARIZER_URL))
    
    # Test 3: Stock analysis
    results.append(test_stock_analysis("AAPL", "3mo"))
    
    # Test 4: Report generation
    results.append(test_report_generation("AAPL,GOOGL", "3mo"))
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Both agents are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n" + "="*60)
    print("Agent URLs:")
    print(f"  Financial Advisor: {FINANCIAL_ADVISOR_URL}")
    print(f"  Report Summarizer: {REPORT_SUMMARIZER_URL}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()