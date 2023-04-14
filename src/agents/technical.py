from statistics import mean
from typing import Optional

from src.core.agent import Agent, Order


class TechnicalTrader(Agent):
    def __init__(self, cash: float, stocks: int, window_size: int = 3, pct: float = 0.1) -> None:
        super().__init__(cash, stocks)
        self.window_size = window_size - 1
        self.window = []

        self.pct = pct

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
        price_hat = self.moving_average(last_price)
        if price_hat is None:
            return
        
        price_diff = abs(price_hat - last_price) / 2

        if last_price > price_hat:
            price = last_price + price_diff
            if self.stocks >= 0:
                quantity = self.cash * self.pct / price
            else:
                quantity = -self.stocks + (self.cash + self.stocks * price) * self.pct / price
            return self.create_buy_order(price_hat + price_diff, quantity)
        else:
            price = max(last_price - price_diff, 1e-10)
            if self.stocks <= 0:
                quantity = (self.cash + 2 * self.stocks * price) * self.pct / price
            else:
                quantity = self.stocks + (self.cash + self.stocks * price) * self.pct / price
            return self.create_sell_order(price, quantity)


class MeanReversionTrader(TechnicalTrader):
    def make_decision(self, last_price: float) -> Optional[Order]:
        price_hat = self.moving_average(last_price)
        if price_hat is None:
            return
        
        price_diff = abs(price_hat - last_price) / 2

        if last_price > price_hat:
            price = max(last_price - price_diff, 1e-10)
            if self.stocks <= 0:
                quantity = (self.cash + 2 * self.stocks * price) * self.pct / price
            else:
                quantity = self.stocks + (self.cash + self.stocks * price) * self.pct / price
            return self.create_sell_order(price_hat + price_diff, quantity)
        else:
            price = last_price + price_diff
            if self.stocks >= 0:
                quantity = self.cash * self.pct / price
            else:
                quantity = -self.stocks + (self.cash + self.stocks * price) * self.pct / price
            return self.create_buy_order(price, quantity)
