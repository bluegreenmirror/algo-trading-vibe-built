# Progress Report - Algo Trading Bot MVP

## Current Status Snapshot
- **Sprint 1** is in progress: foundational repository scaffolding and CI are complete, but trading features remain outstanding.
- **Sprints 2 and 3** have not started and depend on Sprint 1 delivering the core trading loop and risk controls.

## Completed Work
- Repository skeleton, Docker and Poetry setup, and CI/CD automation are finished per the Sprint 1 plan.
- Command-line scaffolding (`hello` and `fetch-bars`) and Alpaca helper functions exist, providing the basis for market data retrieval and order submission stubs.

## Remaining Gaps
- Alpaca integration is only partially implemented: the fetch CLI entrypoint defined in the Sprint plan is missing and the order helper lacks an automated demo, so the epic remains in progress.
- Strategy, policy, execution loop, logging, and validation epics in Sprint 1 have not started; corresponding modules are absent from the current `src/` layout.
- The README advertises strategy, policy, backtester, and logging features that are not yet implemented, risking stakeholder confusion until documentation is updated post-delivery.

## Plan and Next Steps
1. **Finish Sprint 1 core loop**
   - Implement SMA strategy module and integrate it into a scheduled trading loop.
   - Build the policy engine with max-notional enforcement and add structured logging around the execution path.
   - Deliver a paper-trading demo run and reconcile README claims with actual capabilities.
2. **Prepare for Sprint 2** (blocked until Sprint 1 closes)
   - Start database schema and migration work along with historical data loaders to unblock backtesting epics.
   - Define interfaces for policy extensions and PnL tracking to ensure continuity into Sprint 3.
3. **Refine roadmap checkpoints**
   - Revisit Sprint 2 and Sprint 3 entry criteria once Sprint 1 is feature-complete to avoid cascading delays.

## Risks and Mitigations
- **Schedule risk**: With most Sprint 1 epics untouched, downstream sprints will slip. *Mitigation*: focus the next iteration on closing Sprint 1 acceptance criteria before starting parallel work.
- **Documentation drift**: Public docs overstate functionality. *Mitigation*: schedule README and doc revisions as part of the Sprint 1 review to align expectations.
