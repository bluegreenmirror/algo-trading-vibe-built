#!/usr/bin/env bash
set -euo pipefail

echo "== Rebuild image =="
docker compose build

echo
echo "== CLI help includes 'trade' =="
if docker compose run -T --rm app --help | grep -q "trade"; then
  echo "OK: trade command found"
else
  echo "ERROR: trade command missing" >&2
  exit 1
fi

echo
echo "== Execute mock trade =="
OUTPUT=$(docker compose run -T --rm app trade --symbol TEST --notional 100 --side buy)

if echo "$OUTPUT" | grep -q "Order submitted"; then
  echo "OK: Mock trade submitted successfully"
else
  echo "ERROR: Mock trade submission failed" >&2
  echo "Output: $OUTPUT" >&2
  exit 1
fi

echo
echo "== Summary =="
echo "✔ CLI command present"
echo "✔ Mock trade executed successfully"
