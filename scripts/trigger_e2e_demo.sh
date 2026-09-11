#!/usr/bin/env sh
set -eu

curl -sS -X POST http://localhost:5000/api/demo/alert \
  -H 'Content-Type: application/json'
echo
