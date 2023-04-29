from random import shuffle

from tqdm import tqdm

from src.core.agent import Agent
from src.core.orderbook import OrderBook
from src.core.stats_monitor import StatsMonitor


class Engine:
    def __init__(self) -> None:
        self.order_book = OrderBook()
        self.stats_monitor = StatsMonitor()

    def run(self, agents: list[Agent], initial_price: float, n_steps: int = 100) -> None:
        last_price = initial_price
        for _ in tqdm(range(n_steps)):
            last_price = self.step(agents, last_price=last_price)

    def step(self, agents: list[Agent], last_price: float) -> float:
        self.stats_monitor.log_price(last_price)
        self.stats_monitor.log_balance_stats(agents, last_price)
        self.order_book.drop_orders()

        shuffle(agents)
        orders = []
        for agent in agents:
            order = agent.make_decision(last_price)
            if order is not None:
                orders.append(order)
                self.order_book.register(order)
        self.stats_monitor.log_supply_demand_stats(orders)
        
        transactions = self.order_book.match_orders()
        self.stats_monitor.log_trade_stats(transactions)
        cost, volume = 1e-10, 1e-10
        for transaction in transactions:
            transaction.buyer.update_cash(-transaction.cost)
            transaction.seller.update_cash(+transaction.cost)
            transaction.buyer.update_stocks(+transaction.quantity)
            transaction.seller.update_stocks(-transaction.quantity)

            cost += transaction.cost
            volume += transaction.quantity
 
        return cost / volume if transactions else last_price            
