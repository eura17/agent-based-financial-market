import random
from typing import Optional

from src.core.agent import Agent, Order


class FundamentalTrader(Agent):
    def __init__(
            self, 
            cash: float, 
            stocks: int, 
            mu: float, 
            sigma: float, 
            min: float = -0.001,
            max: float = 0.001,
            pct: float = 0.05,
        ) -> None:
        super().__init__(cash, stocks)
        self.mu = mu
        self.sigma = sigma
        self.min = min
        self.max = max
        self.pct = pct

        self.price_hat = None

    def make_decision(self, last_price: float) -> Optional[Order]:
        if self.price_hat is None:
            self.price_hat = last_price

        g = random.gauss(mu=self.mu, sigma=self.sigma)
        g = min(self.max, g)
        g = max(self.min, g)

        self.price_hat *= (1 + g)
        price_diff = abs(self.price_hat - last_price) / 2

        if self.price_hat > last_price:
            self.price_hat = last_price + price_diff
            return self.create_buy_order(self.price_hat, (self.cash / self.price_hat) * self.pct)
        elif self.stocks > 0:
            self.price_hat = max(last_price - price_diff, 1e-10)
            return self.create_sell_order(self.price_hat, self.stocks * self.pct)
