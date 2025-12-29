class ExecutionEngine:

    def __init__(self, slippage=0.0005):
        self.slippage = slippage
        self.positions = {}
        self.trades = []

    def execute(self, bar, signals):

        actual_close = bar["close"]
        ts = bar["timestamp"]

        for sig in signals:

            key = (sig.strategy_name, sig.symbol)

            # ===== Execution price with slippage =====
            if sig.side == "BUY":
                fill = actual_close * (1 + self.slippage)
            else:   # EXIT means SELL for longs
                fill = actual_close * (1 - self.slippage)

            # ===== OPEN LONG =====
            if sig.side == "BUY":

                self.positions[key] = dict(
                    entry=fill,                 # execution price with slippage
                    entry_close=actual_close,   # raw close price
                    time=ts.replace(tzinfo=None) if hasattr(ts, "tzinfo") else ts,
                    qty=sig.qty,
                    side="LONG"
                )

            # ===== EXIT LONG =====
            elif sig.side == "EXIT" and key in self.positions:

                pos = self.positions.pop(key)

                exit_close = actual_close     # raw close price

                # PnL based on execution prices
                pnl = (fill - pos["entry"]) * pos["qty"]

                self.trades.append(dict(
                    symbol=sig.symbol,
                    strategy=sig.strategy_name,

                    entry_time=pos["time"],
                    exit_time=ts.replace(tzinfo=None) if hasattr(ts, "tzinfo") else ts,

                    # --- store both prices ---
                    actual_entry_close=pos["entry_close"],
                    slippage_entry_price=pos["entry"],

                    actual_exit_close=exit_close,
                    slippage_exit_price=fill,

                    qty=pos["qty"],
                    side=pos["side"],

                    pnl=pnl
                ))

def execute(self, bar, signals):

    actual_close = bar["close"]
    ts = bar["timestamp"]

    for sig in signals:

        key = (sig.strategy_name, sig.symbol)

        # ===== Execution price with slippage =====
        if sig.side == "BUY":
            fill = actual_close * (1 + self.slippage)
        else:   # EXIT means SELL for longs
            fill = actual_close * (1 - self.slippage)

        # ===== OPEN LONG =====
        if sig.side == "BUY":

            self.positions[key] = dict(
                entry=fill,                 # execution price with slippage
                entry_close=actual_close,   # raw close price
                time=ts.replace(tzinfo=None) if hasattr(ts, "tzinfo") else ts,
                qty=sig.qty,
                side="LONG"
            )

        # ===== EXIT LONG =====
        elif sig.side == "EXIT" and key in self.positions:

            pos = self.positions.pop(key)

            exit_close = actual_close     # raw close price

            # PnL based on execution prices
            pnl = (fill - pos["entry"]) * pos["qty"]

            self.trades.append(dict(
                symbol=sig.symbol,
                strategy=sig.strategy_name,

                entry_time=pos["time"],
                exit_time=ts.replace(tzinfo=None) if hasattr(ts, "tzinfo") else ts,

                # --- store both prices ---
                actual_entry_close=pos["entry_close"],
                slippage_entry_price=pos["entry"],

                actual_exit_close=exit_close,
                slippage_exit_price=fill,

                qty=pos["qty"],
                side=pos["side"],

                pnl=pnl
            ))
