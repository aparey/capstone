import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Check environment variables
print("🔍 Checking environment variables...")
api_key = os.getenv('ANTHROPIC_API_KEY')
mongo_uri = os.getenv('MONGODB_AGENTFACTS_URI')
public_url = os.getenv('PUBLIC_URL', 'http://localhost:6000')

if not api_key:
    print("❌ ANTHROPIC_API_KEY not found in .env")
    exit(1)
if not mongo_uri:
    print("❌ MONGODB_AGENTFACTS_URI not found in .env")
    exit(1)

print(f"✅ API Key: {api_key[:20]}...")
print(f"✅ MongoDB: Connected")
print(f"✅ Public URL: {public_url}")

from nanda_core.core.adapter import NANDA

# Simple agent logic
def my_agent_logic(message: str, conversation_id: str) -> str:
    return f"Echo: {message}"

print("\n🚀 Starting test agent...")

try:
    nanda = NANDA(
        agent_id="test-agent-001",
        agent_logic=my_agent_logic,
        port=6000,
        public_url=public_url,  # Use public_url parameter
        enable_telemetry=False
    )
    
    print("✅ Agent created successfully!")
    print(f"🌐 Starting server on {public_url}")
    print("\n💡 Test with:")
    print(f"   curl -X POST {public_url}/a2a -H 'Content-Type: application/json' -d '{{\"content\":{{\"text\":\"Hello\",\"type\":\"text\"}},\"role\":\"user\",\"conversation_id\":\"test\"}}'")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    nanda.start()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()