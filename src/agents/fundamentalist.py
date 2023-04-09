from typing import Optional

from src.core.agent import Agent, Order


class FundamentalTrader(Agent):
    def __init__(self, cash: float, stocks: int, pi: float, gdp: float, price0: float, pct: float = 0.05) -> None:
        super().__init__(cash, stocks)
        self.pi = pi
        self.gdp = gdp
        self.price0 = price0
        self.pct = pct
        self.t = 0

    def make_decision(self, last_price: float) -> Optional[Order]:
        self.t += 1
        estimated_price = self.price0 * (1 + self.pi + self.gdp) ** self.t

        if estimated_price > last_price:
            return self.create_buy_order(
                price=estimated_price,
                quantity=self.cash * self.pct / estimated_price,
            )
        elif (can_sell := min(self.cash * self.pct / estimated_price, self.stocks)) > 0:
            return self.create_sell_order(
                price=estimated_price,
                quantity=can_sell,
            )
