#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Activate venv
source "../venv/bin/activate"

export USE_MONGODB_DISCOVERY=1

echo "Starting Financial Advisor on :6001..."
python examples/domain_agents/financial_advisor_agent.py &
ADVISOR_PID=$!

sleep 2

echo "Starting Report Summarizer on :6002..."
python examples/domain_agents/report_summarizer_agent.py &
SUMMARIZER_PID=$!

echo "\nAgents started. PIDs: advisor=${ADVISOR_PID}, summarizer=${SUMMARIZER_PID}"
echo "Advisor:    http://localhost:6001/a2a"
echo "Summarizer: http://localhost:6002/a2a"
echo "\nTo stop: kill ${ADVISOR_PID} ${SUMMARIZER_PID} or Ctrl+C here."

wait

