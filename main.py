import yaml
import pandas as pd
from data.feed import MarketDataFeed
from strategies.moving_average import MovingAverageStrategy
from strategies.supertrend import SupertrendStrategy
from strategies.rsi2 import RSI2LongStrategy

from execution.engine import ExecutionEngine
from risk.manager import RiskManager
from analytics.metrics import compute_metrics


cfg = yaml.safe_load(open("config/settings.yaml"))

# ---- Common feed ----
feed = MarketDataFeed(cfg["data_path"], cfg["symbols"])

# ---- Strategy registry ----
strategy_map = {
    "MA": MovingAverageStrategy,
    "Supertrend": SupertrendStrategy,
    "RSI2": RSI2LongStrategy,   # your renamed fast strategy
}

# ---- Loop each strategy separately ----
for strat_name, strat_cls in strategy_map.items():

    print(f"\n==============================")
    print(f" RUNNING STRATEGY : {strat_name}")
    print(f"==============================\n")

    strat = strat_cls()
    engine = ExecutionEngine(cfg["slippage"])
    risk = RiskManager(cfg["max_qty"], cfg["daily_loss_limit_pct"])

    # reset feed iteration
    for bar in feed.stream():

        sigs = strat.on_bar(bar)

        if not sigs:
            continue

        # risk filter
        allowed = []
        for s in sigs:
            x = risk.allow(s, 0)
            if x:
                allowed.append(x)

        engine.execute(bar, allowed)

    trades = engine.trades
    trades_df = pd.DataFrame(trades)

    out_trades = f"trades_{strat_name}.csv"
    trades_df.to_csv(out_trades, index=False)
    print(f"Saved {out_trades}  ({len(trades_df)} trades)")

    # metrics
    metrics = compute_metrics(trades)
    pd.DataFrame([metrics]).to_csv(f"metrics_{strat_name}.csv", index=False)

    # equity curve
    if len(trades_df):
        trades_df["equity"] = trades_df["pnl"].cumsum()
        trades_df.to_csv(f"equity_{strat_name}.csv", index=False)

    print(f"Completed strategy {strat_name}")
