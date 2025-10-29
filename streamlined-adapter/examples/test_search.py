from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MONGODB_AGENTFACTS_URI'))
db = client['nanda_agentfacts']
collection = db['agents']

# Test the exact query that's failing
results = list(collection.find(
    {"$text": {"$search": "Warren Insights"}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})]).limit(5))

print(f"📊 Found {len(results)} results\n")

for i, result in enumerate(results, 1):
    print(f"{i}. Type: {type(result)}")
    if isinstance(result, dict):
        print(f"   Agent Name: {result.get('agent_name')}")
        print(f"   Agent ID: {result.get('agent_id')}")
    else:
        print(f"   ERROR: Expected dict, got {type(result)}: {result}")
    print()