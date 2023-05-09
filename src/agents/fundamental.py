from random import gauss
from typing import Optional

from src.core.agent import Agent, Order


class FundamentalTrader(Agent):
    def __init__(
            self, 
            cash: float,
            *,
            mu: float, 
            sigma: float, 
            min: float = -0.001,
            max: float = 0.001,
            pct: float = 0.05,
        ) -> None:
        super().__init__(cash)
        self.mu = mu
        self.sigma = sigma
        self.min = min
        self.max = max
        self.pct = pct

        self.price_hat = None

    def make_decision(self, last_price: float) -> Optional[Order]:
        if self.price_hat is None:
            self.price_hat = last_price

        g = gauss(mu=self.mu, sigma=self.sigma)
        g = min(self.max, g)
        g = max(self.min, g)
        self.price_hat *= (1 + g)

        if (max_risk := self.total_equity(last_price) * self.pct) < 0:
            max_risk = max(self.cash, self.stocks * last_price) * self.pct
        
        price_diff = abs(self.price_hat - last_price) / 2
        if self.price_hat > last_price:
            price = self.price_hat + price_diff
            return self.create_buy_order(price, max_risk / price)
        else:
            price = max(self.price_hat - price_diff, 1e-10)
            return self.create_sell_order(price, max_risk / price)
