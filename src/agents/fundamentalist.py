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
        price_hat = self.price0 * (1 + self.pi + self.gdp) ** self.t
        price_diff = abs(price_hat - last_price) / 2

        if price_hat > last_price:
            price = last_price + price_diff
            quantity = self.cash * self.pct / price
            return self.create_buy_order(price, quantity)
        else:
            price = max(last_price - price_diff, 1e-10)
            quantity = self.stocks * self.pct
            return self.create_sell_order(price, quantity)
