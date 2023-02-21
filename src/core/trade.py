from dataclasses import dataclass

from src.core.agent import Agent


@dataclass
class Trade:
    price: float
    quantity: int
    buyer: Agent
    seller: Agent

    @property
    def cost(self) -> float:
        return self.quantity * self.price
