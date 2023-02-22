from collections import defaultdict, deque
from dataclasses import dataclass

from src.core.agent import Agent, Order, OrderType


@dataclass
class Transaction:
    price: float
    quantity: int
    buyer: Agent
    seller: Agent

    @property
    def cost(self) -> float:
        return self.quantity * self.price


class OrderBook:
    def __init__(self) -> None:
        self.bids = OrdersList()
        self.asks = OrdersList()

    def register(self, order: Order) -> None:
        if order.type == OrderType.BUY:
            self.bids.place(order)
        else:
            self.asks.place(order)

    def match_orders(self) -> list[Transaction]:
        transactions = []
        while (best_bid := self.bids.max_price()) >= (best_ask := self.asks.min_price()):
            transaction = self.make_deal(best_bid, best_ask)
            transactions.append(transaction)
        return transactions

    def make_deal(self, bid_price: float, ask_price: float) -> Transaction:
        bid_order = self.bids.fetch_first(bid_price)
        ask_order = self.asks.fetch_first(ask_price)

        transaction = Transaction(
            price=(bid_order.price + ask_order.price) / 2,
            quantity=min(bid_order.quantity, ask_order.quantity),
            buyer=bid_order.agent,
            seller=ask_order.agent,
        )

        bid_order.quantity -= transaction.quantity
        if bid_order.quantity == 0:
            self.bids.drop_first(bid_price)
        ask_order.quantity -= transaction.quantity
        if ask_order.quantity == 0:
            self.asks.drop_first(ask_price)

        return transaction
    
    def drop_orders(self) -> None:
        self.bids.truncate()
        self.asks.truncate()


class OrdersList:
    def __init__(self) -> None:
        self.levels: defaultdict[float, deque[Order]] = defaultdict(deque)

    def place(self, order: Order) -> None:
        self.levels[order.price].append(order)

    def fetch_first(self, price: float) -> Order:
        if (orders := self.levels.get(price)) is None:
            raise ValueError(f"no orders with {price = }")
        return orders[0]

    def drop_first(self, price: float) -> None:
        if (orders := self.levels.get(price)) is None:
            raise ValueError(f"already no orders with {price = }")
        orders.popleft()
        if not orders:
            self.levels.pop(price)

    def max_price(self) -> float:
        return max(self.levels, default=float("inf"))

    def min_price(self) -> float:
        return min(self.levels, default=float("-inf"))

    def truncate(self) -> None:
        self.levels.clear()
