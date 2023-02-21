from dataclasses import dataclass
from enum import Enum


class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(slots=True)
class Order:
    type: OrderType
    price: float
    quantity: int
