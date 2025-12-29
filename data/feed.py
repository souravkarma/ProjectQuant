import pandas as pd
import glob
import os

class MarketDataFeed:

    def __init__(self, folder_path, symbols):
        self.data = []
        for sym in symbols:
            path = os.path.join(folder_path, f"{sym}.csv")
            df = pd.read_csv(path)
            df["timestamp"] = pd.to_datetime(df["date"])
            df["Symbol"] = sym
            df = df[["timestamp","open","high","low","close","volume","Symbol"]]
            self.data.append(df)

        self.df = pd.concat(self.data).sort_values("timestamp")
        print(f"Loaded {len(self.df)} total bars across {len(symbols)} symbols")


    def stream(self):
        for row in self.df.itertuples(index=False):
            yield {
                "timestamp": row.timestamp,
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "volume": row.volume,
                "Symbol": row.Symbol
            }

