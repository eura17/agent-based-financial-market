from queue import Queue
from typing import Optional

from src.core.agent import Agent, Order


class TechnicalTrader(Agent):
    def __init__(self, cash: float, *, window_size: int = 3, pct: float = 0.1) -> None:
        super().__init__(cash)
        self.pct = pct

        self.window = Queue(maxsize=window_size - 1)
        self.window_sum = 0
    
    def moving_average(self, last_price: float) -> Optional[float]:
        if self.window.full():
            self.window_sum -= self.window.get()
            self.window.task_done()

        self.window.put(last_price)
        self.window_sum += last_price

        if self.window.full():
            return self.window_sum / self.window.maxsize


class TrendTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        if (ma := self.moving_average(last_price)) is None:
            return
        
        if (max_risk := self.total_equity(last_price) * self.pct) < 0:
            max_risk = max(self.cash, self.stocks * last_price) * self.pct
        
        price_diff = abs(ma - last_price) / 2
        if last_price > ma:
            price = last_price + price_diff
            return self.create_buy_order(price, max_risk / price)
        else:
            price = max(last_price - price_diff, 1e-10)
            return self.create_sell_order(price, max_risk / price)


class MeanReversionTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        if (ma := self.moving_average(last_price)) is None:
            return
        
        if (max_risk := self.total_equity(last_price) * self.pct) < 0:
            max_risk *= -1
            # return
        
        price_diff = abs(ma - last_price) / 2
        if last_price > ma:
            price = max(last_price - price_diff, 1e-10)
            return self.create_sell_order(price, max_risk / price)
        else:
            price = last_price + price_diff
            return self.create_buy_order(price, max_risk / price)
