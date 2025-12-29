from collections import deque
from .base import Strategy, Signal


class MovingAverageStrategy(Strategy):

    def __init__(self, fast=10, slow=30, qty=50):
        self.fast = fast
        self.slow = slow
        self.qty = qty

        self.fast_q = deque(maxlen=fast)
        self.slow_q = deque(maxlen=slow)

        self.position = 0

    def on_bar(self, bar):

        price = bar["close"]

        self.fast_q.append(price)
        self.slow_q.append(price)

        if len(self.slow_q) < self.slow:
            return []

        fast_ma = sum(self.fast_q) / len(self.fast_q)
        slow_ma = sum(self.slow_q) / len(self.slow_q)

        signals = []

        # ENTRY
        if self.position == 0 and fast_ma > slow_ma:
            signals.append(Signal(
                side="BUY",
                symbol=bar["Symbol"],
                timestamp=bar["timestamp"],
                qty=self.qty,
                strategy_name="MovingAverage",
                reason="BullishCross"
            ))
            self.position = 1

        # EXIT
        elif self.position == 1 and fast_ma < slow_ma:
            signals.append(Signal(
                side="EXIT",
                symbol=bar["Symbol"],
                timestamp=bar["timestamp"],
                qty=self.qty,
                strategy_name="MovingAverage",
                reason="BearishCross"
            ))
            self.position = 0

        return signals
