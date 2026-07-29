#!/usr/bin/env bash
# Monitors the app's /health endpoint every 30 seconds.
# Usage: ./monitor.sh [base_url] [interval_seconds]

BASE_URL="${1:-http://localhost:8080}"
INTERVAL="${2:-30}"

echo "Monitoring ${BASE_URL}/health every ${INTERVAL}s (Ctrl+C to stop)..."

while true; do
  START=$(date +%s%N)
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${BASE_URL}/health")
  END=$(date +%s%N)
  ELAPSED_MS=$(( (END - START) / 1000000 ))
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [ "$HTTP_CODE" == "200" ]; then
    STATUS="UP"
  else
    STATUS="DOWN"
  fi

  echo "[${TIMESTAMP}] ${STATUS} | ${ELAPSED_MS}ms | HTTP ${HTTP_CODE}"

  sleep "$INTERVAL"
done

