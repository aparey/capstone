import json
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

print("📝 Loading configuration...")
agentfacts_uri = os.getenv('MONGODB_AGENTFACTS_URI')

if not agentfacts_uri:
    print("❌ ERROR: MONGODB_AGENTFACTS_URI not found in .env file!")
    exit(1)

from nanda_core.embeddings.embedding_manager import create_embedding

# Connect directly to MongoDB
print("🔌 Connecting to MongoDB...")
client = MongoClient(agentfacts_uri)
db = client['nanda_agentfacts']
collection = db['agents']

print(f"✅ Connected! Database: {db.name}")

# Config file
config_file = 'scripts/agent_configs/100-agents-config.json'

print(f"📂 Loading agents from {config_file}...\n")

try:
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    # The JSON is an array of groups, each containing agents
    all_agents = []
    
    if isinstance(data, list):
        # Flatten: extract agents from each group
        for group_item in data:
            group_name = group_item.get('group', 'Unknown Group')
            agents_in_group = group_item.get('agents', [])
            print(f"📦 Found group: {group_name} with {len(agents_in_group)} agents")
            
            # Add group info to each agent and collect them
            for agent in agents_in_group:
                agent['group'] = group_name
                all_agents.append(agent)
    else:
        print(f"❌ Unexpected JSON structure")
        exit(1)
    
    print(f"\n✨ Total agents to load: {len(all_agents)}\n")
    
    # Show sample agent
    print("🔍 Sample agent:")
    print(json.dumps(all_agents[0], indent=2))
    print("\n" + "="*50 + "\n")
    
    # Add each agent with embeddings
    loaded_count = 0
    for i, agent in enumerate(all_agents, 1):
        try:
            agent_id = agent.get('agent_id', f"agent-{i}")
            agent_name = agent.get('agent_name', agent_id)
            
            print(f"⚙️  [{i}/{len(all_agents)}] Processing: {agent_name}")
            
            # Create embedding text
            specialization = agent.get('specialization', '')
            description = agent.get('description', '')
            domain = agent.get('domain', '')
            embedding_text = f"{domain} {specialization} {description}".strip()
            
            if not embedding_text:
                print(f"   ⚠️  No text found for embedding, skipping...")
                continue
            
            # Create embedding
            print(f"   🔨 Creating embedding...")
            agent['embedding'] = create_embedding(embedding_text)
            
            # Insert into MongoDB
            result = collection.insert_one(agent)
            loaded_count += 1
            print(f"   ✅ Added successfully!")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Successfully loaded {loaded_count}/{len(all_agents)} agents!")
    
    # Verify
    count = collection.count_documents({})
    print(f"📊 Total agents in database: {count}")
    
    # Show sample by group
    if count > 0:
        print("\n📋 Sample agents by group:")
        groups = collection.distinct('group')
        for group in groups[:3]:  # Show first 3 groups
            sample = collection.find({'group': group}).limit(2)
            print(f"\n  {group}:")
            for agent in sample:
                print(f"    - {agent.get('agent_name')} ({agent.get('agent_id')})")
    
    client.close()

except FileNotFoundError:
    print(f"❌ Config file not found: {config_file}")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()