#!/usr/bin/env bash
set -euo pipefail

echo "== Rebuild image =="
docker compose build

echo
echo "== Unit tests (FakeREST, no network) =="
docker compose run -T --rm --entrypoint python app -m pytest -q tests/test_alpaca_provider.py

echo
echo "== CLI help includes 'fetch-bars' =="
if docker compose run -T --rm app --help | grep -q "fetch-bars"; then
  echo "OK: fetch-bars command found"
else
  echo "ERROR: fetch-bars command missing" >&2
  exit 1
fi

echo
echo "== Optional live fetch (only if keys present) =="
if docker compose run -T --rm --entrypoint sh app -lc 'test -n "$ALPACA_KEY_ID" -a -n "$ALPACA_SECRET_KEY"'; then
  docker compose run -T --rm app fetch-bars --symbol AAPL --limit 3
else
  echo "SKIP: ALPACA_KEY_ID/ALPACA_SECRET_KEY not set in .env; live fetch skipped."
fi

echo
echo "== Summary =="
echo "✔ Unit test passed"
echo "✔ CLI command present"
echo "✔ Live fetch optional (skipped unless keys provided)"