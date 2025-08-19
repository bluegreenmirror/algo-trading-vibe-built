"""Order Router for Executing Trading Signals"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.data.providers.alpaca import AlpacaDataProvider
from src.risk.policy_engine import Decision
from src.strategy.rules_engine import Signal


@dataclass
class ExecResult:
    """Order execution result"""
    status: str  # 'placed', 'pending', 'blocked'
    order_id: Optional[str] = None
    violations: Optional[list] = None
    notional: float = 0.0


class OrderRouter:
    """Routes trading signals through policy checks to execution"""

    def __init__(self, alpaca_provider: AlpacaDataProvider):
        self.alpaca_provider = alpaca_provider

    def execute(
        self,
        decision: Decision,
        signal: Signal
    ) -> ExecResult:
        """
        Execute a trading signal based on policy decision

        Args:
            decision: Policy decision from PolicyEngine
            signal: Original trading signal

        Returns:
            ExecResult with execution status and details
        """
        if decision.status == "blocked":
            return ExecResult(
                status="blocked",
                violations=decision.violations,
                notional=decision.notional
            )

        elif decision.status == "needs_approval":
            # For MVP, we'll mark as pending (manual approval outside scope)
            return ExecResult(
                status="pending",
                notional=decision.notional
            )

        elif decision.status == "ok":
            # Execute the order
            try:
                # Convert side string to Alpaca enum
                from alpaca.trading.enums import OrderSide
                side = OrderSide.BUY if signal.side == "buy" else OrderSide.SELL

                order_id = self.alpaca_provider.place_market_order(
                    symbol=signal.symbol,
                    side=side,
                    qty=signal.qty
                )

                if order_id:
                    return ExecResult(
                        status="placed",
                        order_id=order_id,
                        notional=decision.notional
                    )
                else:
                    return ExecResult(
                        status="blocked",
                        violations=["Failed to place order with broker"],
                        notional=decision.notional
                    )

            except Exception as e:
                return ExecResult(
                    status="blocked",
                    violations=[f"Execution error: {str(e)}"],
                    notional=decision.notional
                )

        else:
            # Unknown status
            return ExecResult(
                status="blocked",
                violations=[f"Unknown policy status: {decision.status}"],
                notional=decision.notional
            )


def main():
    """Test the order router with sample data"""
    import os

    import pandas as pd

    from src.risk.policy_engine import Decision, Limits, PolicyEngine
    from src.strategy.rules_engine import Signal

    # This is a test function - in real usage, you'd have actual API keys
    print("Order Router Test (Mock Mode)")
    print("=" * 40)

    # Create mock components
    limits = Limits()
    policy = PolicyEngine(limits)

    # Create test signal
    signal = Signal(
        symbol="AAPL",
        side="buy",
        qty=10,
        price_hint=150.0,
        reason="Test signal",
        timestamp=pd.Timestamp.now()
    )

    # Check policy
    decision = policy.check_order(signal)
    print(f"Policy Decision: {decision.status}")
    print(f"Reason: {decision.reason}")

    # Note: We can't test actual execution without API keys
    print("\nNote: Actual order execution requires valid Alpaca API keys")
    print("Set ALPACA_KEY_ID and ALPACA_SECRET_KEY environment variables to test")


if __name__ == "__main__":
    main()
