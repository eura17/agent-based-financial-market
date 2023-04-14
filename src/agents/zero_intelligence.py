from random import uniform, random
from typing import Optional

from src.core.agent import Agent, Order


class ZeroIntelligenceTrader(Agent):
    def __init__(self, cash: float, stocks: int, noise: float = 0.5) -> None:
        super().__init__(cash, stocks)
        self.noise = noise

    def make_decision(self, last_price: float) -> Optional[Order]:
        price_hat = uniform(self.noise * last_price, (1 + self.noise) * last_price)

        if random() > 0.5:
            order_factory = self.create_buy_order
            if self.stocks >= 0:
                quantity = self.cash / price_hat
            else:
                quantity = -self.stocks + (self.cash + self.stocks * price_hat) / price_hat
        else:
            order_factory = self.create_sell_order
            if self.stocks <= 0:
                quantity = self.cash / price_hat
            else:
                quantity = self.stocks + (self.cash + self.stocks * price_hat) / price_hat

        return order_factory(price=price_hat, quantity=quantity)
