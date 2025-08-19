"""Risk Policy Engine for Trading Decisions"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.strategy.rules_engine import Signal


@dataclass
class Limits:
    """Risk limits configuration"""
    max_position_per_symbol: float = 10000.0
    max_gross_notional: float = 50000.0
    daily_max_drawdown: float = 1000.0
    require_human_approval_over: float = 2500.0


@dataclass
class Decision:
    """Policy decision result"""
    status: str  # 'blocked', 'needs_approval', 'ok'
    violations: List[str]
    notional: float
    reason: str


class PolicyEngine:
    """Risk management policy engine"""

    def __init__(self, limits: Limits):
        self.limits = limits

    def check_order(
        self,
        signal: Signal,
        current_positions: Optional[Dict[str, float]] = None,
        day_pnl: float = 0.0
    ) -> Decision:
        """
        Check if a trading signal complies with risk policies

        Args:
            signal: Trading signal to evaluate
            current_positions: Current position sizes by symbol
            day_pnl: Realized + unrealized P&L for the day

        Returns:
            Decision object with status and violations
        """
        if current_positions is None:
            current_positions = {}

        violations = []
        notional = signal.qty * signal.price_hint

        # Check daily drawdown limit
        if day_pnl < -self.limits.daily_max_drawdown:
            violations.append(f"Daily P&L ({day_pnl:.2f}) below drawdown limit ({-self.limits.daily_max_drawdown:.2f})")

        # Check per-symbol position limit
        current_symbol_position = current_positions.get(signal.symbol, 0.0)
        if signal.side == "buy":
            new_position = current_symbol_position + notional
        else:  # sell
            new_position = current_symbol_position - notional

        if abs(new_position) > self.limits.max_position_per_symbol:
            violations.append(
                f"Position size ({new_position:.2f}) exceeds per-symbol limit ({self.limits.max_position_per_symbol:.2f})"
            )

        # Check gross notional limit
        total_gross = sum(abs(pos) for pos in current_positions.values()) + notional
        if total_gross > self.limits.max_gross_notional:
            violations.append(
                f"Gross notional ({total_gross:.2f}) exceeds limit ({self.limits.max_gross_notional:.2f})"
            )

        # Determine decision based on violations
        if violations:
            status = "blocked"
            reason = f"Policy violations: {', '.join(violations)}"
        elif notional > self.limits.require_human_approval_over:
            status = "needs_approval"
            reason = f"Notional ({notional:.2f}) requires human approval (threshold: {self.limits.require_human_approval_over:.2f})"
        else:
            status = "ok"
            reason = "All policy checks passed"

        return Decision(
            status=status,
            violations=violations,
            notional=notional,
            reason=reason
        )


def main():
    """Test the policy engine with sample signals"""
    import pandas as pd

    from src.strategy.rules_engine import Signal, SMAParams

    # Create sample limits
    limits = Limits(
        max_position_per_symbol=10000.0,
        max_gross_notional=50000.0,
        daily_max_drawdown=1000.0,
        require_human_approval_over=2500.0
    )

    policy = PolicyEngine(limits)

    # Test signals
    test_signals = [
        Signal(
            symbol="AAPL",
            side="buy",
            qty=10,
            price_hint=150.0,
            reason="Test signal 1",
            timestamp=pd.Timestamp.now()
        ),
        Signal(
            symbol="MSFT",
            side="buy",
            qty=20,
            price_hint=300.0,
            reason="Test signal 2",
            timestamp=pd.Timestamp.now()
        )
    ]

    current_positions = {"AAPL": 5000.0, "MSFT": 3000.0}
    day_pnl = -500.0

    print("Policy Engine Test Results:")
    print("=" * 50)

    for i, signal in enumerate(test_signals, 1):
        decision = policy.check_order(signal, current_positions, day_pnl)
        print(f"\nSignal {i}: {signal.symbol} {signal.side} {signal.qty} @ {signal.price_hint}")
        print(f"Status: {decision.status}")
        print(f"Notional: ${decision.notional:.2f}")
        print(f"Reason: {decision.reason}")
        if decision.violations:
            print(f"Violations: {decision.violations}")


if __name__ == "__main__":
    main()
