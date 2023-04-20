from typing import Optional

from src.core.agent import Agent, Order


class FundamentalTrader(Agent):
    def __init__(self, cash: float, stocks: int, pi: float, gdp: float, price_0: float, pct: float = 0.05) -> None:
        super().__init__(cash, stocks)
        self.pi = pi
        self.gdp = gdp
        self.price_0 = price_0
        self.pct = pct
        self.t = 0

    def make_decision(self, last_price: float) -> Optional[Order]:
        self.t += 1
        price_t = self.price_0 * (1 + self.pi + self.gdp) ** self.t
        price_diff = abs(price_t - last_price) / 2

        if price_t > last_price:
            price_hat = last_price + price_diff
            return self.create_buy_order(price_hat, (self.cash / price_hat) * self.pct)
        else:
            price_hat = max(last_price - price_diff, 1e-10)
            return self.create_sell_order(price_hat, self.stocks * self.pct)
