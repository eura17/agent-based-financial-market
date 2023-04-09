from statistics import mean
from typing import Optional

from src.core.agent import Agent, Order


class TechnicalTrader(Agent):
    def __init__(self, cash: float, stocks: int, window_size: int = 3) -> None:
        super().__init__(cash, stocks)
        self.window_size = window_size - 1
        self.window = []

    @property
    def is_window_full(self) -> bool:
        return len(self.window) == self.window_size
    
    def moving_average(self, last_price: float) -> Optional[float]:
        self.window.append(last_price)
        if not self.is_window_full:
            return None
        self.window = self.window[1:]
        return mean(self.window)


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
