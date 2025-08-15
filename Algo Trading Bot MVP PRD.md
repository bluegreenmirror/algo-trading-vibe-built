# Algo Trading Bot MVP — Product Requirements Document (PRD)

## 1. Purpose
Build a **guard-railed algo trading bot MVP** that demonstrates:
- Automated signal generation (rules-based + optional LLM advisory)
- Paper trading via **Alpaca’s paper API**
- Enforced **risk & compliance policies** before any trade
- Logging, monitoring, and auditability
- A simple backtesting engine to validate strategies

This MVP will provide a safe, auditable environment to validate strategies, policies, and operational readiness **before live trading**.

---

## 2. Goals & Success Criteria

**Goals**
- Enable fully automated **paper trading** with Alpaca.
- Prove safety via a **Policy Engine**: no orders bypass limits.
- Provide **basic strategy hooks**: simple moving average crossover.
- Run **backtests** against historical data.
- Produce **audit logs** for every decision.
- Deployable via **Docker Compose** with update scripts.

**Success Criteria**
- Bot can run unattended for 2 weeks in paper mode without policy violations.
- Logs capture 100% of decisions (signal → policy → order).
- Backtests reproducible and outperform SPY baseline in at least one test.
- Non-technical user can configure limits & strategies via `.env` or YAML.

---

## 3. Scope

### In Scope (MVP)
1. **Data ingestion**
   - Market data from Alpaca API.
   - Store OHLCV locally (SQLite or CSV).

2. **Strategies**
   - At least one **deterministic rules-based strategy** (e.g., SMA crossover).
   - Optional: **LLM Advisor** that generates natural language “rationale” only (no direct trading power).

3. **Policy Engine**
   - Enforce limits:
     - Max position per symbol
     - Max gross notional
     - Daily max drawdown
     - Human approval threshold
   - Block or mark orders as `needs_approval`.

4. **Execution**
   - Place paper trades via Alpaca’s order API.
   - Order Router integrates with Policy Engine.

5. **Backtester**
   - Input: CSV of historical prices.
   - Run strategy logic + policy checks.
   - Output: returns, drawdowns, violation counts.

6. **Observability**
   - Structured logs (JSON).
   - Audit file of all trades, reasons, and outcomes.

7. **Deployment**
   - Docker Compose setup.
   - Scripts for build, deploy, update.
   - Documentation: README, SECURITY, RUNBOOK.

---

### Out of Scope (MVP)
- Live trading with real funds.
- Advanced ML/LLM-driven trading strategies.
- Multi-broker integration (IBKR, Robinhood, etc.).
- Options, futures, or crypto instruments.
- Complex portfolio optimization.
- Real-time distributed event bus (Kafka, Pulsar).
- Production-grade monitoring stack (Prometheus/Grafana).
- Automated approval routing (Slack/email integration).

---

## 4. Phases

### Phase 1 — Foundation (Weeks 1–3)
- Repo setup: Docker, scripts, docs.
- Alpaca paper trading integration.
- Policy Engine with hardcoded limits.
- Simple SMA crossover strategy.
- Logging & audit trail.

**Deliverable**: Bot can place safe paper trades under strict limits.

---

### Phase 2 — Backtesting & Validation (Weeks 3–6)
- Backtester implemented.
- Run baseline strategy against historical data.
- Compare performance to SPY buy-and-hold.
- Validate Policy Engine blocks violations during backtests.

**Deliverable**: Documented backtest results, reproducible runs.

---

### Phase 3 — Enhancements & Observability (Weeks 6–9)
- Config via `.env` or YAML (limits, symbols, strategy params).
- Structured JSON logs.
- Audit log export.
- Optional: LLM Advisor stub (advisory notes only).
- Final polish of documentation (README, RUNBOOK).

**Deliverable**: Complete MVP system, ready for demo.

---

## 5. Users & Roles

- **Trader/Operator (human)**  
  - Configures limits & strategies.  
  - Reviews audit logs.  
  - Approves high-notional trades (manual step, outside MVP).  

- **Developer**  
  - Extends strategies.  
  - Integrates new brokers or markets (future phases).  

---

## 6. Non-Functional Requirements
- **Safety first**: No order bypasses Policy Engine.
- **Auditability**: Every action logged with timestamp.
- **Portability**: All services containerized.
- **Simplicity**: Must be maintainable by a small team.

---

## 7. Risks & Mitigations
- **Risk**: LLM generates unsafe signals → Mitigation: Policy Engine blocks.
- **Risk**: Broker API downtime → Mitigation: fail gracefully, retry with backoff.
- **Risk**: Strategy underperformance → Mitigation: backtests, paper trades only.

---

## 8. Future Roadmap (Post-MVP)
- Multi-broker support (IBKR, Robinhood).
- More advanced ML/LLM-driven strategies.
- Portfolio optimization & risk parity.
- Slack/email approval workflow.
- Metrics dashboard (Grafana).
- Compliance features for regulated trading.

---

## 9. Appendix
- [Alpaca API Docs](https://alpaca.markets/docs/) — paper/live trading API.
- [NIST Audit Logging Guidelines](https://csrc.nist.gov/publications/) — for compliance alignment.
