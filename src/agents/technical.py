from statistics import mean
from typing import Optional
from queue import Queue

from src.core.agent import Agent, Order


class TechnicalTrader(Agent):
    def __init__(self, cash: float, stocks: int, window_size: int = 3) -> None:
        super().__init__(cash, stocks)
        self.window = Queue(maxsize=window_size - 1)
    
    def moving_average(self, last_price: float) -> Optional[float]:
        self.window.put(last_price)
        if not self.window.full():
            return None
        return mean(self.window.queue)


class TrendTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        if ma := self.moving_average(last_price):
            order_factory = self.create_buy_order if ma > last_price else self.create_sell_order
            return order_factory(
                price=ma,
                quantity=self.total_equity(last_price) / ma,
            )


class MeanReversionTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        if ma := self.moving_average(last_price):
            order_factory = self.create_buy_order if ma < last_price else self.create_sell_order
            return order_factory(
                price=ma,
                quantity=self.total_equity(last_price) / ma,
            )
