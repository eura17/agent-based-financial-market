from queue import Queue
from typing import Optional

from src.core.agent import Agent, Order


class TechnicalTrader(Agent):
    def __init__(self, cash: float, stocks: int, window_size: int = 3, pct: float = 0.1) -> None:
        super().__init__(cash, stocks)
        self.window_size = window_size - 1
        self.window_sum = 0
        self.window = Queue(maxsize=window_size)

        self.pct = pct
    
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
            return None
        
        price_diff = abs(ma - last_price) / 2
        if last_price > ma:
            price_hat = last_price#last_price + price_diff
            if self.cash == 0:
                return
            elif self.cash < 0:
                return self.create_sell_order(price_hat, (-self.cash / price_hat) * self.pct)
            else:
                return self.create_buy_order(price_hat, (self.cash / price_hat) * self.pct)
        else:
            price_hat = last_price#max(last_price - price_diff, 1e-10)
            if (can_borrow := self.can_borrow(last_price)) == 0:
                return
            elif can_borrow < 0:
                return self.create_buy_order(price_hat, (-can_borrow / price_hat) * self.pct)
            else:
                return self.create_sell_order(price_hat, (can_borrow / price_hat) * self.pct)


class MeanReversionTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        if (ma := self.moving_average(last_price)) is None:
            return None
        
        price_diff = abs(ma - last_price) / 2
        if last_price > ma:
            price_hat = max(last_price - price_diff, 1e-10)
            if (can_borrow := self.can_borrow(last_price)) == 0:
                return
            elif can_borrow < 0:
                return self.create_buy_order(price_hat, (-can_borrow / price_hat) * self.pct)
            else:
                return self.create_sell_order(price_hat, (can_borrow / price_hat) * self.pct)
        else:
            price_hat = last_price + price_diff
            if self.cash == 0:
                return
            elif self.cash < 0:
                return self.create_sell_order(price_hat, (-self.cash / price_hat) * self.pct)
            else:
                return self.create_buy_order(price_hat, (self.cash / price_hat) * self.pct)
