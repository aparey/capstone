#!/usr/bin/env python3
"""
Risk Assessment Agent
=====================
Specialized agent for analyzing investment risks using A2A protocol.
Provides risk scores, volatility analysis, and risk mitigation strategies.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import anthropic
# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from nanda_core.core.adapter import NANDA

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def process_risk_assessment(message: str, conversation_id: str) -> str:
    """
    Assess investment risks using Claude.
    Expects stock data in JSON format.
    """
    
    print(f"\n🛡️ [{conversation_id}] Risk Assessment Request")
    
    # System prompt for risk assessment specialist
    system_prompt = """You are a specialized Risk Assessment Analyst for investments.

Your role is to:
1. Analyze stock data and identify ALL potential risks
2. Calculate risk scores (1-10 scale, 10 being highest risk)
3. Assess volatility and market exposure
4. Identify sector-specific risks
5. Evaluate valuation risks (overvaluation concerns)
6. Consider macro-economic factors
7. Provide risk mitigation strategies

Be thorough, objective, and conservative in your risk assessments.

Format your response with:
- Overall Risk Score (1-10)
- Key Risk Factors (bullet points)
- Volatility Assessment
- Risk Mitigation Recommendations
- Conservative Investment Sizing Suggestion

Always err on the side of caution."""

    try:
        # Call Claude for risk analysis
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Analyze the investment risks for this stock data:\n\n{message}"
            }]
        )
        
        risk_analysis = response.content[0].text
        
        print(f"✅ Risk assessment completed ({len(risk_analysis)} chars)")
        
        return f"""[risk-assessment-agent]

RISK ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{risk_analysis}

---
⚠️ Risk Disclaimer: This risk assessment is for educational purposes only. 
Past performance does not guarantee future results. Always consult with a 
qualified financial advisor before making investment decisions.
"""
        
    except Exception as e:
        print(f"❌ Error in risk assessment: {e}")
        return f"[risk-assessment-agent]\n\nError performing risk assessment: {str(e)}"


if __name__ == "__main__":
    # Configuration
    AGENT_ID = "risk-assessment-agent"
    PORT = 6004
    PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")
    
    print("🛡️ Starting Risk Assessment Agent...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Port: {PORT}")
    print(f"   Public URL: {PUBLIC_URL}")
    print(f"   Model: claude-haiku-4-5-20251001")
    
    # Create NANDA agent
    agent = NANDA(
        agent_id=AGENT_ID,
        agent_logic=process_risk_assessment,
        port=PORT,
        public_url=PUBLIC_URL,
        enable_telemetry=False,
        agent_name="Risk Assessment Specialist",
        agent_description="Specialized agent for analyzing investment risks, volatility, and providing risk mitigation strategies",
        agent_capabilities={
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": False,
            "google_a2a_compatible": True,
            "parts_array_format": True,
            "skills": [
                "risk_analysis",
                "volatility_assessment",
                "risk_scoring",
                "risk_mitigation",
                "portfolio_risk_evaluation",
                "sector_risk_analysis"
            ]
        }
    )
    
    print(f"\n🚀 Risk Assessment Agent running on {PUBLIC_URL}")
    print(f"📡 Endpoint: {PUBLIC_URL}/a2a")
    print("\n💡 This agent receives stock data and provides risk analysis")
    print("   It's designed to be called by other agents via A2A protocol\n")
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Risk Assessment Agent...")