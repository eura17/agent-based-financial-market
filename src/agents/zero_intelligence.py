from random import uniform, random
from typing import Optional

from src.core.agent import Agent, Order


class ZeroIntelligenceTrader(Agent):
    def __init__(self, cash: float, stocks: int, noise: float = 0.5) -> None:
        super().__init__(cash, stocks)
        self.noise = noise

    def make_decision(self, last_price: float) -> Optional[Order]:
        # price_hat = uniform(max(last_price - self.noise, 0), last_price + self.noise)
        price_hat = uniform((1 - self.noise) * last_price, (1 + self.noise) * last_price)
        if random() > 0.5:
            if self.cash > 0:
                return self.create_buy_order(price_hat, self.cash / price_hat)
        else:
            ostatok = 2 * self.total_equity(last_price) - self.cash
            if ostatok > 0:
                return self.create_sell_order(price_hat, ostatok / price_hat)
