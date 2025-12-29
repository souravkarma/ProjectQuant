import collections
import math
from .base import Strategy, Signal


class SupertrendStrategy(Strategy):
    """
    TradingView-style Supertrend strategy.
    Optimised version — O(1) update per bar.
    """

    def __init__(self, period=10, multiplier=3.0, qty=50):
        self.period = period
        self.mult = multiplier
        self.qty = qty

        self.bars = collections.deque(maxlen=period + 2)

        self.atr = None
        self.trend = 1
        self.up = None
        self.dn = None

        self.position = 0

    def true_range(self, h, l, c_prev):
        return max(
            h - l,
            abs(h - c_prev),
            abs(l - c_prev)
        )

    def on_bar(self, bar):

        ts = bar["timestamp"].replace(tzinfo=None)
        h = float(bar["high"])
        l = float(bar["low"])
        c = float(bar["close"])
        sym = bar["Symbol"]

        self.bars.append((ts, h, l, c))

        if len(self.bars) < self.period + 1:
            return []

        _, h_prev, l_prev, c_prev = self.bars[-2]

        tr = self.true_range(h, l, c_prev)

        if self.atr is None:
            self.atr = tr
        else:
            self.atr = (self.atr * (self.period - 1) + tr) / self.period

        hl2 = (h + l) / 2

        basic_up = hl2 - self.mult * self.atr
        basic_dn = hl2 + self.mult * self.atr

        if self.up is None:
            self.up = basic_up
            self.dn = basic_dn
        else:
            self.up = basic_up if c_prev <= self.up else max(basic_up, self.up)
            self.dn = basic_dn if c_prev >= self.dn else min(basic_dn, self.dn)

        prev_trend = self.trend

        if self.trend == 1 and c < self.up:
            self.trend = -1
        elif self.trend == -1 and c > self.dn:
            self.trend = 1

        signals = []

        # ENTRY
        if self.position == 0 and prev_trend == -1 and self.trend == 1:
            signals.append(Signal(
                side="BUY",
                timestamp=ts,
                symbol=sym,
                qty=self.qty,
                reason="SupertrendUp",
                strategy_name="Supertrend"
            ))
            self.position = 1

        # EXIT
        elif self.position == 1 and prev_trend == 1 and self.trend == -1:
            signals.append(Signal(
                side="EXIT",
                timestamp=ts,
                symbol=sym,
                qty=self.qty,
                reason="SupertrendDown",
                strategy_name="Supertrend"
            ))
            self.position = 0

        return signals
