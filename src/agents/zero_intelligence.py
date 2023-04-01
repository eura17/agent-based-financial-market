from random import uniform
from typing import Optional

from src.core.agent import Agent, Order


class ZeroIntelligenceTrader(Agent):
    def __init__(self, cash: float, stocks: int, noise: float = 0.5) -> None:
        super().__init__(cash, stocks)
        self.noise = noise

    def make_decision(self, last_price: float) -> Optional[Order]:
        estimated_price = uniform(self.noise * last_price, (1 + self.noise) * last_price)
        order_factory = self.create_buy_order if estimated_price > last_price else self.create_sell_order
        return order_factory(
            price=estimated_price,
            quantity=self.total_equity(last_price) / estimated_price,
        )
