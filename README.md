[![CI](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml)

# algo-trading-vibe-built
Currently provides no license - demo purposes only

# Algo Trading Bot — Sprint 1 (Day 1)

Minimal, **secure** scaffold to start Sprint 1 without leaking secrets.

## Containerized Quickstart (no Poetry on host required)

```bash
# 1) Build the image
docker compose build

# 2) Create local .env (never commit!)
cp .env.example .env
# fill ALPACA_... later

# 3) Run CLI via Docker
./scripts/run.sh --help
./scripts/run.sh hello

# 4) Update image when dependencies change
./scripts/update.sh
```

## Quickstart with Poetry (optional)

```bash
# Install Poetry if you don't have it
# pipx install poetry

poetry install
poetry run pre-commit install

# Create your local env file (never commit .env)
cp .env.example .env
# Fill in ALPACA_KEY_ID / ALPACA_SECRET_KEY later (Day 3–4)

# Run tests
poetry run pytest -q

# CLI
poetry run python -m src.app --help
poetry run python -m src.app hello
```

## Notes
- Secrets are **not** in the repo. Use `.env` locally or a secrets manager.
- Pre-commit hooks provide formatting, linting, and secret scanning.
- CI builds & tests **inside Docker**.
- Tagging a release like `v1.0.0` will build & push a container image to **GHCR**.
