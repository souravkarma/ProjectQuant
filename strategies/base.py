from abc import ABC, abstractmethod
from dataclasses import dataclass


from dataclasses import dataclass
from datetime import datetime



@dataclass
class Signal:
    side: str              # "BUY" | "SELL" | "EXIT"
    timestamp: object
    symbol: str
    qty: int
    strategy_name: str
    reason: str = ""



class Strategy(ABC):

    @abstractmethod
    def on_bar(self, bar):
        """
        Must return a list of Signal objects (possibly empty)
        """
        pass
