# ProjectQuant
classDiagram

    class MarketDataFeed{
        +stream() Bar
    }

    class Strategy{
        <<abstract>>
        +on_bar(Bar) Signal[]
    }

    class MovingAverageStrategy{
        +on_bar(Bar) Signal[]
    }

    class SupertrendStrategy{
        +on_bar(Bar) Signal[]
    }

    class RSI2Strategy{
        +on_bar(Bar) Signal[]
    }

    class Signal{
        +side: str
        +timestamp: datetime
        +symbol: str
        +qty: int
        +reason: str
        +strategy_name: str
    }

    class RiskManager{
        +allow(Signal, pnl) Signal | None
    }

    class ExecutionEngine{
        -positions
        -trades
        +execute(Bar, Signal[])
        +trades: list
    }

    class MetricsEngine{
        +compute_metrics(trades)
    }

    class main_py{
        -feed: MarketDataFeed
        -strategies: list
        -engine: ExecutionEngine
        -risk: RiskManager
        +run()
    }

    MarketDataFeed --> Strategy : streams Bar
    Strategy --> Signal : emits
    Signal --> RiskManager : checked by
    RiskManager --> ExecutionEngine : passes signals
    ExecutionEngine --> MetricsEngine : outputs trades
    Strategy <|-- MovingAverageStrategy
    Strategy <|-- SupertrendStrategy
    Strategy <|-- RSI2Strategy
    main_py --> MarketDataFeed
    main_py --> Strategy
    main_py --> ExecutionEngine
    sequenceDiagram
    autonumber
    participant Main as main.py
    participant Feed as MarketDataFeed
    participant Strat1 as Strategy A<br/>(MA)
    participant Strat2 as Strategy B<br/>(Supertrend)
    participant Strat3 as Strategy C<br/>(RSI2)
    participant Risk as RiskManager
    participant Exec as ExecutionEngine
    participant Metrics as Analytics/Metrics

    Main->>Feed: request next Bar
    Feed-->>Main: return Bar

    loop per Strategy
        Main->>Strat1: on_bar(Bar)
        Strat1-->>Main: Signal[] (0..N)

        Main->>Strat2: on_bar(Bar)
        Strat2-->>Main: Signal[] (0..N)

        Main->>Strat3: on_bar(Bar)
        Strat3-->>Main: Signal[] (0..N)
    end

    Main->>Risk: check Signals
    Risk-->>Main: allowed Signals

    Main->>Exec: execute(Bar, Signals)
    Exec-->>Exec: update positions & trades

    Note right of Exec: Realised & Unrealised PnL updated

    Main->>Feed: request next Bar
    Feed-->>Main: return Bar

    opt End of Backtest
        Main->>Metrics: compute(trades)
        Metrics-->>Main: per-strategy analytics
        Main-->>Main: save CSV outputs
    end
graph TD

    subgraph Data Layer
        Feed[MarketDataFeed\n(OHLC Loader + Replay)]
    end

    subgraph Strategy Engine
        MA[MovingAverageStrategy]
        ST[SupertrendStrategy]
        RSI[RSI2Strategy]
        Base[Strategy Base Class]
    end

    subgraph Execution Layer
        Risk[RiskManager]
        Exec[ExecutionEngine\n(Market Order Simulator)]
    end

    subgraph Analytics Layer
        Metrics[Metrics Engine\n(Sharpe • DD • Win-rate)]
        Reports[CSV Outputs\nTrades • Metrics • Equity]
    end

    Main[main.py\n(Orchestrator)]

    Feed --> Main

    Base --- MA
    Base --- ST
    Base --- RSI

    Main --> MA
    Main --> ST
    Main --> RSI

    MA --> Main
    ST --> Main
    RSI --> Main

    Main --> Risk
    Risk --> Exec

    Exec --> Metrics
    Metrics --> Reports

    main_py --> RiskManager

