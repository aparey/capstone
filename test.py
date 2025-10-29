import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('streamlined-adapter/test.env')

# Test telemetry connection
print('🔍 Testing telemetry database...')
telemetry_uri = os.getenv('MONGODB_TELEMETRY_URI')
telemetry_client = MongoClient(telemetry_uri)
try:
    telemetry_client.admin.command('ping')
    print('✅ Telemetry database connected!')
    print(f'   Database: nanda_telemetry')
except Exception as e:
    print(f'❌ Telemetry connection failed: {e}')

# Test agent facts connection
print('\n🔍 Testing agent facts database...')
agentfacts_uri = os.getenv('MONGODB_AGENTFACTS_URI')
agentfacts_client = MongoClient(agentfacts_uri)
try:
    agentfacts_client.admin.command('ping')
    print('✅ Agent facts database connected!')
    print(f'   Database: nanda_agentfacts')
except Exception as e:
    print(f'❌ Agent facts connection failed: {e}')

print('\n🎉 Both databases ready to use!')