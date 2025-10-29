## Quick resume checklist (tomorrow)

1) Activate virtual environment
```bash
source "/Users/parey69/Desktop/ALY 6980/venv/bin/activate"
```

2) Load env vars and enable MongoDB discovery
```bash
export USE_MONGODB_DISCOVERY=1
```

3) Ensure env vars are set (edit if needed)
- Edit `streamlined-adapter/test.env` (or `.env`) to include:
  - `MONGODB_AGENTFACTS_URI`
  - `ANTHROPIC_API_KEY` (optional for LLM responses)
  - `PUBLIC_URL` (optional; defaults to http://localhost:6000)

4) Run the quick test agent
```bash
cd "/Users/parey69/Desktop/ALY 6980/streamlined-adapter"
python test_agent.py
```

5) Optional: run the LLM example agent
```bash
python examples/nanda_agent.py
```

6) Start the Financial Advisor and Report Summarizer agents
```bash
cd "/Users/parey69/Desktop/ALY 6980/streamlined-adapter"
chmod +x scripts/run_financial_agents.sh
scripts/run_financial_agents.sh
```

6) If search returns no results, confirm agents exist and index is present
```bash
python load_agents.py   # loads agents into MongoDB
python - <<'PY'
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv('streamlined-adapter/test.env')
col = MongoClient(os.getenv('MONGODB_AGENTFACTS_URI'))['nanda_agentfacts']['agents']
col.create_index([('agent_id','text'),('agent_name','text'),('description','text'),('specialization','text'),('domain','text')])
print('✅ Text index ensured on nanda_agentfacts.agents')
PY
```

7) Dependency snapshot (today)
- Saved at `requirements.lock.txt` (created with `pip freeze`) for reproducibility.

Notes
- To stop: Ctrl+C in the terminal.
- To deactivate venv: `deactivate`.


