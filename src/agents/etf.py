from typing import Optional

from src.core.agent import Agent, Order


class ETFTrader(Agent):
    def __init__(self, cash: float, stocks: int, pct: float = 0.01) -> None:
        super().__init__(cash, stocks)
        self.pct = pct

    def make_decision(self, last_price: float) -> Optional[Order]:
        return self.create_buy_order(
            price=last_price,
            quantity=(self.cash / last_price) * self.pct,
        )
