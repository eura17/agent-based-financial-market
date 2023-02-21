from collections import defaultdict, deque

from src.core.agent import Agent
from src.core.order import Order, OrderType
from src.core.trade import Trade


class OrderBook:
    def __init__(self) -> None:
        self.bids: defaultdict[float, deque[tuple[Order, Agent]]] = defaultdict(deque)
        self.asks: defaultdict[float, deque[tuple[Order, Agent]]] = defaultdict(deque)

    def register_order(self, order: Order, agent: Agent) -> None:
        if order.type == OrderType.BUY:
            self.bids[order.price].append((order, agent))
        else:
            self.asks[order.price].append((order, agent))

    def match_orders(self) -> list[Trade]: ...
    
    def drop_orders(self) -> None:
        self.bids.clear()
        self.asks.clear()
