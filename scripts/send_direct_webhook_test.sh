#!/usr/bin/env sh
set -eu

curl -sS -X POST http://localhost:5000/webhook/alertmanager \
  -H 'Content-Type: application/json' \
  -d '{
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "PortfolioDemoAlert",
          "severity": "warning"
        },
        "annotations": {
          "summary": "Demo alert received successfully",
          "description": "This verifies the Alertmanager-compatible webhook and dashboard alert flow."
        },
        "startsAt": "2026-09-11T00:00:00Z"
      }
    ]
  }'

echo
