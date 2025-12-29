📈 ProjectQuant — Multi-Strategy Equity Backtesting Engine

ProjectQuant is a modular, event-driven backtesting framework designed to simulate real-time equity trading using historical OHLC market data.
It supports multiple independent trading strategies running concurrently on the same market data stream while enforcing risk controls, execution logic, and portfolio-level analytics.

The system architecture closely mirrors real-world quantitative trading platforms by separating:

✔ Market Data Feed — streams historical data bar-by-bar
✔ Strategy Engine — generates trading signals
✔ Risk Manager — validates and filters orders
✔ Execution Engine — simulates fills and maintains positions
✔ Analytics Engine — produces performance metrics and reports

This design ensures clarity, extensibility, and testability, while complying fully with the project specification requirements.

🎯 Key Capabilities

🔄 Historical Replay Mode — data is processed bar-by-bar as if live

🤝 Multiple strategies evaluated concurrently

🧠 Strategy-agnostic architecture — each strategy is isolated and pluggable

💹 Market-order execution simulation with slippage

⚠️ Risk constraints enforced pre-trade

📊 Trade logs, equity curves, and per-strategy performance metrics

🧾 CSV export for all major outputs

⚙️ Built only with Python + pandas — no trading frameworks

📦 Included Trading Strategies
Strategy	Description	Bias
Moving Average Crossover	Trend-following	Long / Exit
Supertrend	Directional trailing stop strategy	Long / Exit
RSI-2 Mean Reversion	Short-term momentum reversion	Long / Exit

Each strategy:

✔ Implements a common interface
✔ Consumes the same live data feed
✔ Emits structured Signal objects
✔ Operates independently

📁 Outputs Generated

The backtest produces:

📄 trades_<strategy>.csv — all executed trades
📈 equity_<strategy>.csv — cumulative PnL curve
📊 metrics_<strategy>.csv — Sharpe, drawdown, win-rate, etc.
📑 strategy_metrics.csv — consolidated results

These files make the system suitable for research workflows, presentation, and audit review.

🏗️ Design Philosophy

ProjectQuant follows separation of concerns:

✔ Data layer
✔ Strategy layer
✔ Execution layer
✔ Risk layer
✔ Analytics layer

This simplifies debugging, enables future strategy extensions, and demonstrates sound software engineering practices expected in quantitative finance systems.



