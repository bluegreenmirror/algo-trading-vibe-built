# Architecture — Algo Trading Bot MVP

This document complements the PRD with **component contracts**, **config schemas**, and **Mermaid diagrams** (system context, modules, and sequence flows).

> In GitHub, Mermaid renders automatically. In VS Code, use a Mermaid extension to preview.

---

## 1) System Context Diagram (MVP)

```mermaid
flowchart LR
  Trader[("Trader/Operator")]
  subgraph App["Algo Bot App (single service)"]
    Orchestrator["Scheduler"]
    Strategy["Strategy Engine<br/>(SMA crossover)"]
    LLM["LLM Advisor (optional)"]
    Policy["Policy Engine"]
    Router["Order Router"]
    Portfolio["Portfolio/P&L"]
    Logger["Structured Logging"]
  end

  Data[("OHLCV Store<br/>SQLite/CSV")]
  Alpaca["Alpaca Market Data<br/>& Paper Broker"]
  Secrets[(".env / Secret Store")]
  Audit[("Audit Log File<br/>+ Central Sink*")]

  Trader -->|configure limits & params| App
  Secrets --> App
  Orchestrator --> Strategy
  Strategy -->|fetch bars| Alpaca
  Strategy --> Data
  Strategy -->|optional rationale| LLM
  Policy --> Router
  Router -->|paper orders| Alpaca
  Alpaca -->|fills/positions| Portfolio
  Logger --> Audit
  App -->|append decisions| Audit
  Alpaca -->|prices| Data

  classDef store fill:#eef,stroke:#99f,stroke-width:1px,color:#000;
  class Data,Audit store;
```

---

## 2) Module / Component Diagram

```mermaid
flowchart TB
  subgraph src/
    subgraph strategy/
      rules["rules_engine.py<br/>- SMA crossover"]
      llm["llm_advisor.py (optional)"]
      signals["signals.py"]
    end

    subgraph data/
      providers["providers/alpaca.py"]
      storage["storage.py (SQLite/CSV)"]
    end

    subgraph risk/
      policy["policy_engine.py"]
      checks["checks.py"]
    end

    subgraph broker/
      base["base.py"]
      alpaca_client["alpaca_client.py"]
    end

    subgraph exec/
      router["order_router.py"]
      portfolio["portfolio.py"]
    end

    backtest["backtest/backtester.py"]
    app["app.py (entrypoint)"]
    config["config.py"]
    loggingc["logging_conf.py"]
  end

  app --> rules
  app --> policy
  rules --> providers
  rules --> storage
  rules --> llm
  policy --> router
  router --> alpaca_client
  alpaca_client --> providers
  router --> portfolio
  backtest --> rules
  backtest --> policy
  backtest --> storage
  app --> loggingc
  app --> config
```

---

## 3) Sequence Flows

### 3.1 Paper Trading Loop

```mermaid
sequenceDiagram
  participant "Cron" as "Scheduler"
  participant "Strat" as "Strategy Engine"
  participant "Data" as "Data Provider"
  participant "Policy" as "Policy Engine"
  participant "Router" as "Order Router"
  participant "Broker" as "Alpaca Paper API"
  participant "Port" as "Portfolio"
  participant "Audit" as "Audit Log"

  "Cron"->>"Strat": tick(symbols, params)
  "Strat"->>"Data": getBars(symbol, window)
  "Data"-->>"Strat": OHLCV[]
  "Strat"->>"Strat": compute SMA crossover
  "Strat"-->>"Policy": signal(symbol, side, qty, price_hint)
  "Policy"-->>"Strat": decision(block | needs_approval | ok)

  alt block (violations)
    "Policy"->>"Audit": log{status:"blocked", violations}
  else needs_approval
    "Policy"->>"Audit": log{status:"pending_approval", notional}
    Note over "Strat","Router": Human approval is outside MVP (manual)
  else ok
    "Router"->>"Broker": submitOrder(symbol, side, qty, type:"market")
    "Broker"-->>"Router": orderId, status
    "Router"->>"Port": update positions/P&L
    "Router"->>"Audit": log{status:"placed", orderId}
  end
```

### 3.2 Backtest Run

```mermaid
sequenceDiagram
  participant "User" as "Operator"
  participant "BT" as "Backtester"
  participant "DS" as "Data Store (CSV/SQLite)"
  participant "STR" as "Strategy"
  participant "POL" as "Policy"
  participant "REP" as "Report"

  "User"->>"BT": run_backtest(config)
  "BT"->>"DS": load historical OHLCV
  "DS"-->>"BT": frames
  "BT"->>"STR": generate signals (per bar)
  "STR"-->>"BT": signal stream
  loop per signal
    "BT"->>"POL": check(signal, limits)
    alt blocked
      "POL"-->>"BT": decision(block)
    else ok
      "POL"-->>"BT": decision(ok)
      "BT"->>"BT": simulate fill & pnl
    end
  end
  "BT"->>"REP": compute returns, drawdowns, violations
  "REP"-->>"User": summary tables & metrics
```

### 3.3 (Informational) Manual Approval Path — Post-MVP

```mermaid
sequenceDiagram
  participant "Policy" as "Policy Engine"
  participant "Audit" as "Audit Log"
  participant "Human" as "Trader/Approver"
  participant "Router" as "Order Router"
  participant "Broker" as "Alpaca Paper API"

  "Policy"-->>"Audit": log pending_approval{symbol, notional}
  "Human"->>"Audit": review pending items
  "Human"->>"Router": approve(order_request_id)
  "Router"->>"Broker": submitOrder(...)
  "Broker"-->>"Router": orderId
  "Router"-->>"Audit": log placed{orderId}
```

---

## 4) Component Contracts (LLM-Friendly)

### 4.1 `strategy/rules_engine.py`
```pseudo
fn generate_signal(symbol: str, ohlcv: Frame, params: SMAParams) -> Optional[Signal]
 inputs:
   - symbol: ticker
   - ohlcv: dataframe with columns [timestamp, open, high, low, close, volume]
   - params: {fast:int, slow:int, min_volume:int}
 outputs:
   - Signal {symbol, side: "buy"|"sell", qty: float, price_hint: float, reason: str}
 behavior:
   - compute SMA_fast and SMA_slow
   - if crossover up -> buy; down -> sell; else None
   - qty sizing: fixed-dollar / price_hint rounded
```

### 4.2 `strategy/llm_advisor.py` (optional)
```pseudo
fn advise(context: MarketContext) -> AdvisoryNote
 inputs: {symbol, recent_change_pct, macro_note?}
 outputs: {rationale: str, confidence: float [0..1]}
 note: advisory only; never returns orders
```

### 4.3 `risk/policy_engine.py`
```pseudo
fn check_order(signal: Signal, limits: Limits, day_pl: float) -> Decision
 inputs:
   - signal: {symbol, side, qty, price_hint}
   - limits: {max_symbol_notional, max_gross_notional, daily_max_drawdown, approval_threshold}
   - day_pl: realized + unrealized P&L today
 outputs: Decision {status: "blocked"|"needs_approval"|"ok", violations: [...], notional: float}
 rules:
   - notional = qty * price_hint
   - apply hard caps; if day_pl < -daily_max_drawdown -> blocked
```

### 4.4 `exec/order_router.py`
```pseudo
fn execute(decision: Decision, signal: Signal) -> ExecResult
 if decision.status == "ok":
   - call broker.place_order(symbol, side, qty, type="market", tif="day")
   - return {status:"placed", order_id}
 elif decision.status == "needs_approval":
   - persist pending; return {status:"pending"}
 else:
   - return {status:"blocked", violations}
```

### 4.5 `broker/alpaca_client.py`
```pseudo
class AlpacaClient:
  fn get_bars(symbol: str, tf: str, limit:int) -> Frame
  fn submit_order(symbol:str, side:str, qty:float, type:str, time_in_force:str) -> Order
  fn get_account() -> Account
```

### 4.6 `backtest/backtester.py`
```pseudo
fn run(config: BacktestConfig) -> BacktestReport
 steps:
  - load OHLCV from CSV/SQLite for symbols & date range
  - iterate bars -> generate_signal -> policy check -> simulate fills
  - compute metrics: CAGR, Sharpe (naive), max DD, winrate
  - return report + CSV of equity curve
```

---

## 5) Config Schemas and Logging

### `.env`
```
ENV=dev
ALPACA_KEY_ID=...
ALPACA_SECRET_KEY=...
ALPACA_BASE_URL=https://paper-api.alpaca.markets
SYMBOLS=AAPL,MSFT,SPY
SCHEDULE_CRON=*/5 * * * *
MAX_POSITION_PER_SYMBOL=10000
MAX_GROSS_NOTIONAL=50000
DAILY_MAX_DRAWDOWN=1000
REQUIRE_HUMAN_APPROVAL_OVER=2500
STRAT_SMA_FAST=20
STRAT_SMA_SLOW=50
MIN_VOLUME=100000
DATABASE_URL=sqlite:///./state.db
```

### Structured Log Example
```json
{
  "ts": "2025-08-15T10:03:21Z",
  "component": "policy",
  "event": "decision",
  "symbol": "AAPL",
  "side": "buy",
  "qty": 10,
  "price_hint": 195.2,
  "notional": 1952.0,
  "status": "ok",
  "violations": []
}
```
