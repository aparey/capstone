#!/usr/bin/env python3
"""
NANDA Intelligent Agent - Web UI
=================================
Simple web interface for interacting with the intelligent report agent.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
AGENT_URL = os.getenv("AGENT_URL", "http://localhost:6003")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query_agent():
    """Proxy requests to the intelligent agent"""
    try:
        user_message = request.json.get('message', '')
        conversation_id = request.json.get('conversation_id', f"web-{datetime.now().timestamp()}")
        
        # Send to agent
        response = requests.post(
            f"{AGENT_URL}/a2a",
            json={
                "content": {
                    "text": user_message,
                    "type": "text"
                },
                "role": "user",
                "conversation_id": conversation_id
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            agent_response = data['parts'][0]['text']
            return jsonify({
                "success": True,
                "response": agent_response,
                "metadata": data.get('metadata', {})
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Agent returned status {response.status_code}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/health')
def health():
    """Check agent health"""
    try:
        response = requests.get(f"{AGENT_URL}/health", timeout=5)
        return jsonify({
            "agent_healthy": response.status_code == 200,
            "agent_url": AGENT_URL
        })
    except:
        return jsonify({
            "agent_healthy": False,
            "agent_url": AGENT_URL
        }), 503

if __name__ == '__main__':
    port = int(os.getenv('WEB_UI_PORT', 5001))
    print(f"\n🌐 Starting NANDA Web UI on http://localhost:{port}")
    print(f"🤖 Connected to agent: {AGENT_URL}")
    print(f"\n📱 Open your browser to: http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=True)