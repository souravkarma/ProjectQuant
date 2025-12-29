import pandas as pd
import numpy as np

def compute_metrics(trades):

    df = pd.DataFrame(trades)
    if df.empty:
        return {}

    equity = df["pnl"].cumsum()

    dd = equity - equity.cummax()
    max_dd = dd.min()

    sharpe = np.sqrt(252) * df["pnl"].mean() / df["pnl"].std()

    winrate = (df["pnl"] > 0).mean()

    return dict(
        total_pnl=df["pnl"].sum(),
        sharpe=sharpe,
        max_drawdown=max_dd,
        winrate=winrate,
        num_trades=len(df)
    )
