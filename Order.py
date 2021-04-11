from datetime import datetime
import enum

# Types of Order


class OrderDirection(enum.Enum):

    BUY = 1  # Bid
    SELL = 0  # Ask


# Represent An Order
class Order:

    def __init__(self, orderId, orderPrice, orderDirection, orderSize):
        self.orderId: str = orderId
        self.time: str = datetime.now()
        self.orderPrice: int = orderPrice
        self.orderSize: int = orderSize
        self.orderDirection: OrderDirection = orderDirection

    def __eq__(self, other):

        return type(self) == type(other) and self.orderId == other.orderId

    def __str__(self):
        return f'({self.time.strftime("%H:%M:%S %p")})[{self.orderId}] '

    def __repr__(self):
        return f'({self.time.strftime("%H:%M:%S %p")})[{self.orderId}] '
