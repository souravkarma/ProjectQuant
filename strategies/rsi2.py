import pandas as pd
from .base import Strategy, Signal


class RSI2LongStrategy(Strategy):

    def __init__(self, qty=50):
        self.qty = qty

        self.prev_close = None
        self.position = 0  # 0 = flat, 1 = long

        # Wilder running averages
        self.avg_gain = None
        self.avg_loss = None

        self.period = 2

    def update_rsi(self, close):

        if self.prev_close is None:
            self.prev_close = close
            return None

        change = close - self.prev_close
        self.prev_close = close

        gain = max(change, 0)
        loss = max(-change, 0)

        # first warmup
        if self.avg_gain is None:
            self.avg_gain = gain
            self.avg_loss = loss
            return None

        # Wilder smoothing
        self.avg_gain = (self.avg_gain * (self.period - 1) + gain) / self.period
        self.avg_loss = (self.avg_loss * (self.period - 1) + loss) / self.period

        if self.avg_loss == 0:
            return 100

        rs = self.avg_gain / self.avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def on_bar(self, bar):

        close = bar["close"]

        rsi = self.update_rsi(close)

        if rsi is None:
            return []

        signals = []

        # ===== LONG ENTRY =====
        if self.position == 0 and rsi < 10:

            signals.append(
                Signal(
                    side="BUY",
                    timestamp=bar["timestamp"].replace(tzinfo=None),
                    symbol=bar["Symbol"],
                    qty=self.qty,
                    reason="RSI2_Long_Entry",
                    strategy_name="RSI2"
                )
            )

            self.position = 1

        # ===== EXIT LONG =====
        elif self.position == 1 and rsi > 70:

            signals.append(
                Signal(
                    side="EXIT",
                    timestamp=bar["timestamp"].replace(tzinfo=None),
                    symbol=bar["Symbol"],
                    qty=self.qty,
                    reason="RSI2_Long_Exit",
                    strategy_name="RSI2"
                )
            )

            self.position = 0

        return signals
