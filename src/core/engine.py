from random import shuffle

from src.core.agent import Agent
from src.core.orderbook import OrderBook


class Engine:
    def __init__(self) -> None:
        self.order_book = OrderBook()

    def run(self, agents: list[Agent], initial_price: float, n_steps: int = 100) -> None:
        last_price = initial_price
        for _ in range(n_steps):
            last_price = self.step(agents, last_price=last_price)
            print(_, last_price)

    def step(self, agents: list[Agent], last_price: float) -> float:
        self.order_book.drop_orders()

        shuffle(agents)
        for agent in agents:
            order = agent.make_decision(last_price)
            if order is not None:
                self.order_book.register(order)
        
        transactions = self.order_book.match_orders()        
        for transaction in transactions:
            transaction.buyer.update_cash(-transaction.cost)
            transaction.seller.update_cash(+transaction.cost)
            transaction.buyer.update_stocks(+transaction.quantity)
            transaction.seller.update_stocks(-transaction.quantity)

        return transactions[-1].price if transactions else last_price
