import heapq
from Order import Order, OrderDirection
from Sides import AskSide, BidSide


# Represents a LimitOrderBook
class LimitOrderBook:

    def __init__(self):

        self.askSideList: list(AskSide) = []
        self.bidSideList: list(BidSide) = []

    # calculates the spread  ( BestBid - BestAsk) == BBO
    def spread(self):
        if len(self.bidSideList) > 0 and len(self.askSideList) > 0:
            return round(self.bestAsk().order.orderPrice - self.bestBid().order.orderPrice, 4)
        elif len(self.bidSideList) > 0:
            return round(0 - self.bestBid().order.orderPrice, 4)
        elif len(self.bidSideList) > 0:
            return round(self.bestAsk().order.orderPrice - 0, 4)

    # calculates the best Bid based on comparison defined in BidSide Class
    def bestBid(self):
        if len(self.bidSideList) > 0:
            return self.bidSideList[0]
        return 0
    # calculates the best Ask based on comparison defined in AskSide Class

    def bestAsk(self):
        if len(self.askSideList) > 0:
            return self.askSideList[0]
        return 0
    # add market order

    def executeMarketOrder(self, givenOrder):

        if givenOrder.order.orderDirection == OrderDirection.BUY:
            # subtract from the top order on the Ask Side  until orderPrice is filled or Ask side is emptied.
            while(len(self.askSideList) != 0 and givenOrder.order.orderSize > 0):

                currentOrderSize = givenOrder.order.orderSize
                givenOrder.order.orderSize -= self.askSideList[0].order.orderSize
                self.askSideList[0].order.orderSize -= currentOrderSize
                if self.askSideList[0].order.orderSize <= 0:
                    heapq.heappop(self.askSideList)

            # if the givenOrder size is still not filled then reject it
            if givenOrder.order.orderSize > 0:
                print("Partially filled Market Order")

        elif givenOrder.order.orderDirection == OrderDirection.SELL:
            # subtract from the top order on the Bid Side until orderPrice is filled or Bid side is emptied.
            while(len(self.bidSideList) != 0 and givenOrder.order.orderSize > 0):

                currentOrderSize = givenOrder.order.orderSize
                givenOrder.order.orderSize -= self.bidSideList[0].order.orderSize
                self.bidSideList[0].order.orderSize -= currentOrderSize
                if self.bidSideList[0].order.orderSize <= 0:
                    heapq.heappop(self.bidSideList)

            # if the givenOrder size is still not filled then reject it
            if givenOrder.order.orderSize > 0:
                print("Partially filled Market Order")
        else:
            raise ValueError("Invalid Order Type ")

    def executeLimitOrder(self, givenOrder):

        if givenOrder.order.orderDirection == OrderDirection.BUY:
            # subtract from the top order on the Ask Side  if limitPrice is equal or  less until orderPrice is filled or Ask side is emptied.
            while(len(self.askSideList) != 0 and givenOrder.order.orderSize > 0):

                # if the limit Price is lesser
                if givenOrder.order.orderPrice < self.askSideList[0].order.orderPrice:

                    heapq.heappush(self.bidSideList, givenOrder)
                    return
                else:
                    currentOrderSize = givenOrder.order.orderSize
                    givenOrder.order.orderSize -= self.askSideList[0].order.orderSize

                    self.askSideList[0].order.orderSize -= currentOrderSize
                    if self.askSideList[0].order.orderSize <= 0:
                        heapq.heappop(self.askSideList)

            # if the givenOrder size is still not filled then put it in the bid side
            if givenOrder.order.orderSize > 0:
                heapq.heappush(self.bidSideList, givenOrder)
                print("Partially filled Limit Buy Order")

        elif givenOrder.order.orderDirection == OrderDirection.SELL:
            # subtract from the top order on the Bid Side until limitPrice is less or equal orderSide is filled or Bid side is emptied.

            while(len(self.bidSideList) != 0 and givenOrder.order.orderSize > 0):

                if givenOrder.order.orderPrice > self.bidSideList[0].order.orderPrice:
                    heapq.heappush(self.askSideList, givenOrder)
                    return
                else:
                    currentOrderSize = givenOrder.order.orderSize
                    givenOrder.order.orderSize -= self.bidSideList[0].order.orderSize
                    self.bidSideList[0].order.orderSize -= currentOrderSize
                    if self.bidSideList[0].order.orderSize <= 0:
                        heapq.heappop(self.bidSideList)

            # if the givenOrder size is still not filled then put it in the ask side
            if givenOrder.order.orderSize > 0:
                heapq.heappush(self.askSideList, givenOrder)
                print("Partially filled  Limit  Sell Order")

        else:
            raise ValueError("Invalid Order Type ")
