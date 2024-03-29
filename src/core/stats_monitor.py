from collections import defaultdict, Counter
from statistics import mean, median, stdev

from src.core.agent import Order, OrderType, Agent
from src.core.orderbook import Transaction, OrderBook

class StatsMonitor:
    def __init__(self) -> None:
        self.prices = []
        self.balance_stats = []
        self.supply_demand_stats = []
        self.trade_stats = []
        self.period_stats = []
        self.spreads = []
       
    def log_price(self, price: float) -> None:
        self.prices.append(price)

    def log_balance_stats(self, agents: list[Agent], last_price: float) -> None:
        stats = defaultdict(Counter)
        for agent in agents:
            agent_type = type(agent)
            stats[agent_type]["total_cash"] += agent.cash
            stats[agent_type]["total_stocks"] += agent.stocks
            stats[agent_type]["total_equity"] += agent.total_equity(last_price)
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

    def log_period_stats(self, transactions: list[Transaction]) -> None:
        if not transactions:
            stats = {
                "total_trades": 0,
                "total_quantity": 0,
                "mean_price": None,
                "std_price": None,
                "median_price": None,
                "mean_weighted_price": None,
            }
            self.period_stats.append(stats)
            return
        
        stats = Counter()
        prices, quantities = [], []
        for transaction in transactions:
            stats["total_trades"] += 1
            stats["total_quantity"] += transaction.quantity
            prices.append(transaction.price)
            quantities.append(transaction.quantity)
        stats["mean_price"] = mean(prices)
        stats["std_price"] = stdev(prices)
        stats["median_price"] = median(prices)
        stats["mean_weighted_price"] = (
            sum([p * q for p, q in zip(prices, quantities)])
            / sum(quantities, start=1e-8)
        )
        self.period_stats.append(stats)

    def log_spread(self, order_book: OrderBook) -> None:
        self.spreads.append(
            {
                "min_ask": order_book.asks.min_price(),
                "max_bid": order_book.bids.max_price(),
                "spread": order_book.asks.min_price() - order_book.bids.max_price(),
            }
        )
