from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(slots=True)
class Order:
    type: OrderType
    price: float
    quantity: int
    agent: "Agent"

    def __post_init__(self) -> None:
        self.quantity = max(self.quantity, 1e-10)


class Agent(ABC):
    def __init__(self, cash: float, stocks: int) -> None:
        self.cash = cash
        self.stocks = stocks

        self.is_bankrupt = False

    @abstractmethod
    def make_decision(self, last_price: float) -> Optional[Order]: ...

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
            agent=self,
        )

    def create_sell_order(self, price: float, quantity: int) -> Order:
        return Order(
            type=OrderType.SELL,
            price=price,
            quantity=quantity,
            agent=self,
        )
