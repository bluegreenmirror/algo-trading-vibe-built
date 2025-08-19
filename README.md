[![CI](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml)

# Algo Trading Bot

This repository contains the Algo Trading Bot, an MVP designed for paper trading via the Alpaca API. It features a robust strategy engine, a comprehensive policy engine for risk management, a minimal backtester, and structured logging for auditability.

## Getting Started

To set up your development environment and get a quick overview of the project, please refer to our [Getting Started Guide](GETTING_STARTED.md).

## Key Features

*   **Alpaca Integration**: Connects to Alpaca Market Data and Paper Trading APIs.
*   **Strategy Engine**: Implements an SMA crossover strategy (configurable).
*   **Policy Engine**: Enforces risk controls, including max notional checks, position limits, and daily loss caps.
*   **Backtesting Framework**: Allows for reproducible backtesting with historical data.
*   **Structured Logging**: Provides detailed audit trails of all decisions and actions.
*   **Containerized Development**: Uses Docker and Docker Compose for consistent environments.

## Documentation

*   [**Getting Started**](GETTING_STARTED.md): Your first stop for setting up and understanding the project.
*   [**Key Decisions**](DECISIONS.md): Dive into the architectural and technical decisions that shaped this project.
*   [**Gemini Guidelines**](GEMINI.md): Specific guidelines for interacting with the Gemini AI assistant on this project.
*   [**Architecture**](docs/architecture.md): High-level system architecture and component interactions.
*   [**Technical Design**](docs/technical_design.md): Detailed technical specifications, data models, and algorithms.
*   [**Sprint Plans**](docs/sprint-plan/): Overview of project sprints and development roadmap.
*   [**Contributing**](CONTRIBUTING.md): Guidelines for contributing to the project.
*   [**Agents**](AGENTS.md): Information about the AI agents used in the project.

## Development Workflow

For details on linting, formatting, testing, and commit message conventions, please refer to the [Getting Started Guide](GETTING_STARTED.md) and [Gemini Guidelines](GEMINI.md).

## Key Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `ENV` | `dev` | Execution environment. |
| `ALPACA_KEY_ID` | `None` | Alpaca API key identifier. |
| `ALPACA_SECRET_KEY` | `None` | Alpaca API secret. |
| `ALPACA_BASE_URL` | `https://paper-api.alpaca.markets` | Alpaca API base URL. |
| `SYMBOLS` | `AAPL, MSFT, SPY` | Comma-separated list of symbols. |
| `SCHEDULE_CRON` | `*/5 * * * *` | Cron schedule for automated tasks. |

## Notes
- Secrets are **not** in the repo. Use `.env` locally or a secrets manager.
- Pre-commit hooks provide formatting, linting, and secret scanning.
- CI builds & tests **inside Docker**.
- Tagging a release like `v1.0.0` will build & push a container image to **GHCR**.

Currently provides no license - demo purposes only.