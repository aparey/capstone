#!/bin/bash

# Usage: ./deploy-to-linode-test.sh <SERVER_IP> <ANTHROPIC_API_KEY>

SERVER_IP="$1"
API_KEY="$2"
CONFIG_FILE="my-nanda-agents-config.json"

if [ -z "$SERVER_IP" ] || [ -z "$API_KEY" ]; then
    echo "Usage: $0 <SERVER_IP> <ANTHROPIC_API_KEY>"
    exit 1
fi

echo "🚀 Deploying NANDA agents to $SERVER_IP (TEST MODE - No Registry)..."

# Copy configuration file
echo "📋 Copying configuration..."
scp "$CONFIG_FILE" root@$SERVER_IP:/root/agent-config.json

# Run deployment on server
echo "⚙️  Setting up server..."
ssh root@$SERVER_IP << 'ENDSSH'
#!/bin/bash
set -e

echo "→ Updating system packages..."
apt update -qq
apt install -y -qq git python3 python3-pip python3-venv curl jq net-tools

echo "→ Cloning NEST framework..."
cd /root
rm -rf NEST
mkdir -p NEST && cd NEST
git clone https://github.com/DataWorksAI-com/NEST.git .

echo "→ Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install anthropic flask requests pyyaml python-a2a pymongo > /dev/null 2>&1

echo "→ Creating directories..."
mkdir -p logs scripts/agent_configs

echo "→ Moving configuration..."
mv /root/agent-config.json scripts/agent_configs/my-agents-config.json

echo "✅ Server setup complete!"
ENDSSH

echo ""
echo "🎯 Deploying agents..."
ssh root@$SERVER_IP << PYEOF
cd /root/NEST
source venv/bin/activate
python3 << 'INNERPY'
import json
import subprocess
import time
import os

with open('scripts/agent_configs/my-agents-config.json') as f:
    agents = json.load(f)

# Stop existing agents
subprocess.run(['pkill', '-f', 'nanda_agent'], check=False)
time.sleep(3)

print(f"Deploying {len(agents)} agents...\n")

for agent in agents:
    env = os.environ.copy()
    env.update({
        'ANTHROPIC_API_KEY': '$API_KEY',
        'AGENT_ID': agent['agent_id'],
        'AGENT_NAME': agent['agent_name'],
        'AGENT_DOMAIN': agent['domain'],
        'AGENT_SPECIALIZATION': agent['specialization'],
        'AGENT_DESCRIPTION': agent['description'],
        'AGENT_CAPABILITIES': agent['capabilities'],
        'SYSTEM_PROMPT': agent['system_prompt'],
        'PUBLIC_URL': f'http://$SERVER_IP:{agent["port"]}',
        'PORT': str(agent['port'])
    })
    
    log_file = f'logs/agent_{agent["agent_id"]}.log'
    with open(log_file, 'w') as log:
        subprocess.Popen(
            ['python3', 'examples/nanda_agent.py'],
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT
        )
    
    print(f"✅ Started {agent['agent_name']} on port {agent['port']}")
    time.sleep(2)

print(f"\n🎉 All {len(agents)} agents deployed successfully!")
INNERPY
PYEOF

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔍 Verify deployment:"
echo "  curl http://$SERVER_IP:6000/health"
echo "  curl http://$SERVER_IP:6001/health"
echo ""
echo "📊 Check agent status:"
echo "  ssh root@$SERVER_IP 'ps aux | grep nanda_agent | grep -v grep'"
echo ""
echo "📝 View logs:"
echo "  ssh root@$SERVER_IP 'tail -f /root/NEST/logs/agent_*.log'"
