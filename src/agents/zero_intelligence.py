from random import uniform
from typing import Optional

from src.core.agent import Agent, Order


class ZeroIntelligenceTrader(Agent):
    def __init__(self, cash: float, stocks: int, noise: float = 0.5) -> None:
        super().__init__(cash, stocks)
        self.noise = noise

    def make_decision(self, last_price: float) -> Optional[Order]:
        price_lower_bound = self.noise * last_price
        price_upper_bound = (1 + self.noise) * last_price
        return uniform(price_lower_bound, price_upper_bound)
