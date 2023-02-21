from abc import ABC, abstractmethod
from typing import Optional

from src.core.order import Order, OrderType


class Agent(ABC):
    def __init__(self, cash: float, stocks: int) -> None:
        self.cash = cash
        self.stocks = stocks

    @abstractmethod
    def make_order(self, last_price: float) -> Optional[Order]: ...

    def total_equity(self, stock_price: float) -> float:
        return self.cash + self.stocks * stock_price

    def update_cash(self, diff: float) -> None:
        self.cash += diff

    def update_stocks(self, diff: int) -> None:
        self.stocks += diff

    def create_buy_order(self, price: float, quantity: int) -> Order:
        return Order(
            type=OrderType.BUY,
            price=price,
            quantity=quantity,
        )

    def create_sell_order(self, price: float, quantity: int) -> Order:
        return Order(
            type=OrderType.SELL,
            price=price,
            quantity=quantity,
        )
