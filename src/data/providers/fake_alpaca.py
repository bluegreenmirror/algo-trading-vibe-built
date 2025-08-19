from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FakeOrder:
    symbol: str
    notional: float
    side: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if self.side not in ["buy", "sell"]:
            raise ValueError(f"Invalid side: {self.side}")


class FakeAlpacaAPI:
    """A mock client that simulates the Alpaca API for testing."""

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def submit_order(self, symbol: str, notional: float, side: str, **kwargs: Any) -> FakeOrder:
        """Simulate submitting an order and return a fake order confirmation."""
        print(f"[FakeAlpacaAPI] Submitting {side} order for {notional} of {symbol}")
        return FakeOrder(symbol=symbol, notional=notional, side=side)
