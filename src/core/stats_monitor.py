from collections import defaultdict, Counter
from statistics import mean, median

from src.core.agent import Order, OrderType, Agent
from src.core.orderbook import Transaction

class StatsMonitor:
    def __init__(self) -> None:
        self.balance_stats = []
        self.supply_demand_stats = []
        self.trade_stats = []

    def log_balance_stats(self, agents: list[Agent], last_price: float) -> None:
        stats = defaultdict(Counter)
        for agent in agents:
            if agent.total_equity(last_price) < 0:
                agent.update_cash(-agent.cash)
                agent.update_stocks(-agent.stocks)
                agent.is_bankrupt = True

            agent_type = type(agent)
            stats[agent_type]["total_cash"] += agent.cash
            stats[agent_type]["total_stocks"] += agent.stocks
            stats[agent_type]["total_equity"] += agent.total_equity(last_price)
            stats[agent_type]["total_bankrupts"] += agent.is_bankrupt
        self.balance_stats.append(stats)

    def log_supply_demand_stats(self, orders: list[Order]) -> None:
        stats = defaultdict(Counter)

        raw_stats = defaultdict(lambda: defaultdict(list))
        for order in orders:
            agent_type = type(order.agent)
            if order.type == OrderType.BUY:
                stats[agent_type]["total_buy_orders"] += 1
                stats[agent_type]["total_buy_orders_quantity"] += order.quantity
                stats[agent_type]["total_buy_orders_cash"] += order.price * order.quantity

                raw_stats[agent_type]["buy_prices"].append(order.price)
                raw_stats[agent_type]["buy_quantities"].append(order.quantity)
            else:
                stats[agent_type]["total_sell_orders"] += 1
                stats[agent_type]["total_sell_orders_quantity"] += order.quantity
                stats[agent_type]["total_sell_orders_cash"] += order.price * order.quantity

                raw_stats[agent_type]["sell_prices"].append(order.price)
                raw_stats[agent_type]["sell_quantities"].append(order.quantity)

        for agent_type, agent_type_stats in raw_stats.items():
            if "buy_prices" in agent_type_stats:
                stats[agent_type]["mean_buy_order_price"] = mean(agent_type_stats["buy_prices"])
                stats[agent_type]["median_buy_order_price"] = median(agent_type_stats["buy_prices"])
                stats[agent_type]["mean_weighted_buy_order_price"] = (
                    sum([p * q for p, q in zip(agent_type_stats["buy_prices"], agent_type_stats["buy_quantities"])])
                    / sum(agent_type_stats["buy_quantities"], start=1e-8)
                )

            if "sell_prices" in agent_type_stats:
                stats[agent_type]["mean_sell_order_price"] = mean(agent_type_stats["sell_prices"])
                stats[agent_type]["median_sell_order_price"] = median(agent_type_stats["sell_prices"])
                stats[agent_type]["mean_weighted_sell_order_price"] = (
                    sum([p * q for p, q in zip(agent_type_stats["sell_prices"], agent_type_stats["sell_quantities"])])
                    / sum(agent_type_stats["sell_quantities"], start=1e-8)
                )

        self.supply_demand_stats.append(stats)

    def log_trade_stats(self, transactions: list[Transaction]) -> None:
        stats = defaultdict(Counter)

        raw_stats = defaultdict(lambda: defaultdict(list))
        for transaction in transactions:
            buyer_type = type(transaction.buyer)
            stats[buyer_type]["total_buy_transactions"] += 1
            stats[buyer_type]["total_buy_transactions_quantity"] += transaction.quantity
            stats[buyer_type]["total_buy_transactions_cash"] += transaction.price * transaction.quantity
            raw_stats[buyer_type]["buy_prices"].append(transaction.price)
            raw_stats[buyer_type]["buy_quantities"].append(transaction.quantity)

            seller_type = type(transaction.seller)
            stats[seller_type]["total_sell_transactions"] += 1
            stats[seller_type]["total_sell_transactions_quantity"] += transaction.quantity
            stats[seller_type]["total_sell_transactions_cash"] += transaction.price * transaction.quantity
            raw_stats[seller_type]["sell_prices"].append(transaction.price)
            raw_stats[seller_type]["sell_quantities"].append(transaction.quantity)
        
        for agent_type, agent_type_stats in raw_stats.items():
            if "buy_prices" in agent_type_stats:
                stats[agent_type]["mean_buy_transaction_price"] = mean(agent_type_stats["buy_prices"])
                stats[agent_type]["median_buy_transaction_price"] = median(agent_type_stats["buy_prices"])
                stats[agent_type]["mean_weighted_buy_transaction_price"] = (
                    sum([p * q for p, q in zip(agent_type_stats["buy_prices"], agent_type_stats["buy_quantities"])])
                    / sum(agent_type_stats["buy_quantities"], start=1e-8)
                )

            if "sell_prices" in agent_type_stats:
                stats[agent_type]["mean_sell_transaction_price"] = mean(agent_type_stats["sell_prices"])
                stats[agent_type]["median_sell_transaction_price"] = median(agent_type_stats["sell_prices"])
                stats[agent_type]["mean_weighted_sell_transaction_price"] = (
                    sum([p * q for p, q in zip(agent_type_stats["sell_prices"], agent_type_stats["sell_quantities"])])
                    / sum(agent_type_stats["sell_quantities"], start=1e-8)
                )

        self.trade_stats.append(stats)
