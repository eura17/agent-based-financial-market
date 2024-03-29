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
        if self.price <= 0 or self.quantity <= 0:
            raise ValueError(self)
    
    @property
    def cost(self) -> float:
        return self.price * self.quantity


class Agent(ABC):
    def __init__(self, cash: float, stocks: int = 0) -> None:
        self.cash = cash
        self.stocks = stocks

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
