from typing import Optional

from src.core.agent import Agent, Order


class ETFTrader(Agent):
    def __init__(self, cash: float, *, pct: float = 0.01) -> None:
        super().__init__(cash)
        self.pct = pct

    def make_decision(self, last_price: float) -> Optional[Order]:
        if (max_risk := self.total_equity(last_price) * self.pct) < 0:
            return
        return self.create_buy_order(last_price, max_risk / last_price)
