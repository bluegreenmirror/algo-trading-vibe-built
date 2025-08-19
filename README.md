# Algo Trading Bot MVP — Sprint 1 Implementation

A **guard-railed algo trading bot MVP** that demonstrates automated signal generation, paper trading via Alpaca, enforced risk & compliance policies, and structured logging.

## 🎯 Sprint 1 Status: IMPLEMENTED ✅

**Goal**: Deliver a working bot skeleton that can fetch market data, run SMA strategy, enforce basic policy, and place paper trades.

**Deliverables Completed**:
- ✅ Repo scaffold with Docker & Poetry
- ✅ Alpaca market data + paper trading integration
- ✅ SMA crossover strategy (configurable)
- ✅ Policy engine (max notional check)
- ✅ Structured audit logging
- ✅ Order router and execution flow
- ✅ Main trading bot orchestrator
- ✅ Comprehensive test suite

**Validation**: Bot can run on Alpaca sandbox for 1 day; logs show SMA signals, policy check, and executed trades.

## 🚀 Quick Start

### Option 1: Containerized (Recommended)

```bash
# 1) Build the image
docker compose build

# 2) Create local .env (never commit!)
cp env.example .env
# Fill in ALPACA_KEY_ID and ALPACA_SECRET_KEY

# 3) Run the trading bot
./scripts/run.sh test          # Single trading cycle
./scripts/run.sh run           # Continuous trading
./scripts/run.sh --help        # See all options

# 4) Update image when dependencies change
./scripts/update.sh
```

### Option 2: Poetry (Development)

```bash
# Install dependencies
poetry install

# Run tests
poetry run python test_sprint1.py

# Run the trading bot
poetry run python -m src.trading_bot test    # Single cycle
poetry run python -m src.trading_bot run     # Continuous
```

## 🏗️ Architecture

The bot follows a modular architecture with clear separation of concerns:

```
src/
├── data/providers/     # Market data providers (Alpaca)
├── strategy/           # Trading strategies (SMA crossover)
├── risk/              # Risk management & policy engine
├── broker/            # Broker integration (Alpaca)
├── exec/              # Order execution & portfolio management
├── trading_bot.py     # Main orchestrator
└── config.py          # Configuration management
```

## 🔧 Configuration

Copy `env.example` to `.env` and configure:

- **Alpaca API**: Get free paper trading keys from [Alpaca Markets](https://alpaca.markets/)
- **Risk Limits**: Adjust position sizes, drawdown limits, approval thresholds
- **Strategy**: Configure SMA periods, volume filters
- **Symbols**: Add/remove trading symbols

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test all components
python test_sprint1.py

# Test individual modules
python -m src.strategy.rules_engine
python -m src.risk.policy_engine
python -m src.exec.order_router
```

## 📋 Sprint 1 Ticket Status

| Ticket | Title | Status | Notes |
|--------|-------|--------|-------|
| S1-E1-I1 | Create repo skeleton with Docker & Poetry | ✅ Done | Complete directory structure |
| S1-E1-I2 | Add CI/CD pipeline | ✅ Done | GitHub Actions configured |
| S1-E2-I1 | Connect to Alpaca Market Data API | ✅ Done | Data provider implemented |
| S1-E2-I2 | Connect to Alpaca Paper Trading API | ✅ Done | Order execution implemented |
| S1-E3-I1 | Implement SMA crossover function | ✅ Done | Strategy engine complete |
| S1-E3-I2 | Integrate SMA into bot loop | ✅ Done | Main orchestrator ready |
| S1-E4-I1 | Create policy engine module | ✅ Done | Risk management implemented |
| S1-E4-I2 | Add max notional check | ✅ Done | Policy limits enforced |
| S1-E5-I1 | Wire signal → policy → order | ✅ Done | Complete execution flow |
| S1-E5-I2 | Structured audit logging | ✅ Done | JSON logging implemented |
| S1-E6-I1 | Run 1-day paper demo | 🔄 Ready | Requires Alpaca API keys |
| S1-E6-I2 | Sprint 1 Review & Documentation | ✅ Done | This README |

## 🚀 Next Steps

**Sprint 2** will focus on:
- Backtesting framework
- Enhanced risk controls
- P&L tracking
- Performance metrics

## 📚 Notes
- Secrets are **not** in the repo. Use `.env` locally or a secrets manager.
- Pre-commit hooks provide formatting, linting, and secret scanning.
- CI builds & tests **inside Docker**.
- Tagging a release like `v1.0.0` will build & push a container image to **GHCR**.
