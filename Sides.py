from abc import abstractmethod, ABC
from Order import Order,OrderDirection

# Represent a Side of the LimitOrderBook


class Side(ABC):

    def __init__(self, orderId, orderPrice, orderDirection, orderSize):

        self.order: Order = Order(
            orderId, orderPrice, orderDirection, orderSize)

    @abstractmethod
    def __lt__(self, other):

        raise NotImplementedError

    def __repr__(self):
        return str(self.order)

# Represent an AskSide of the LimitOrderBook


class AskSide(Side):

    def __init__(self, orderId, orderPrice, askSize):
        super().__init__(orderId, orderPrice, OrderDirection.SELL, askSize)

    # compares based on price & time
    def __lt__(self, other):

        if self.order.orderPrice == other.order.orderPrice:
            return self.order.time.time() < other.order.time.time()
        else:
            return self.order.orderPrice < other.order.orderPrice

# Represent a BidSide of the LimitOrderBook


class BidSide(Side):

    def __init__(self, orderId, orderPrice, bidSize):
        super().__init__(orderId, orderPrice, OrderDirection.BUY, bidSize)

    # compares based on price & time
    def __lt__(self, other):

        if self.order.orderPrice == other.order.orderPrice:
            return self.order.time.time() < other.order.time.time()
        else:
            return self.order.orderPrice > other.order.orderPrice
