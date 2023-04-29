from random import uniform, random
from typing import Optional

from src.core.agent import Agent, Order


class ZeroIntelligenceTrader(Agent):
    def __init__(self, cash: float, *, noise: float = 0.1) -> None:
        super().__init__(cash)
        self.noise = noise

    def make_decision(self, last_price: float) -> Optional[Order]:
        if (max_risk := self.total_equity(last_price)) < 0:
            return
        
        price_hat = uniform((1 - self.noise) * last_price, (1 + self.noise) * last_price)
        if random() > 0.5:
            return self.create_buy_order(price_hat, max_risk / price_hat)
        else:
            return self.create_sell_order(price_hat, max_risk / price_hat)
