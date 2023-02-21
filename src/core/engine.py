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

    def step(self, agents: list[Agent], last_price: float) -> float:
        self.order_book.drop_orders()

        shuffle(agents)
        for agent in agents:
            order = agent.make_order(last_price)
            if order is not None:
                self.order_book.register_order(order, agent)
        
        trades = self.order_book.match_orders()        
        for trade in trades:
            trade.buyer.update_cash(-trade.cost)
            trade.seller.update_cash(+trade.cost)
            trade.buyer.update_stocks(+trade.quantity)
            trade.seller.update_stocks(-trade.quantity)

        if trades:
            return trades[-1].price
        return last_price
