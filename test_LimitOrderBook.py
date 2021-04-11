from LimitOrderBook import LimitOrderBook
from Sides import AskSide, BidSide
import pytest


# setup the Limit Order Book instance to be used throughout the tests
@pytest.fixture(autouse=True)
def setup():
    return LimitOrderBook()


# test the type of ask order data
def test_AskOrderList(setup):

    assert isinstance(setup.askSideList, list)


# test the type of buy order data
def test_BuyOrderList(setup):

    assert isinstance(setup.bidSideList, list)


# test Limit Ask Order
def test_ExecuteLimitAskOrder(setup):
    setup.executeLimitOrder(AskSide('O1O1', 33.75, 2))
    assert len(setup.askSideList) == 1 and len(setup.bidSideList) == 0


# test Limit Buy Order
def test_ExecuteLimitBuyOrder(setup):
    setup.executeLimitOrder(BidSide('O1O2', 33.75, 2))
    assert len(setup.askSideList) == 0 and len(setup.bidSideList) == 1

# test Limit Marketable Buy Order


def test_limitMarketAbleBuyOrder(setup):
    setup.executeLimitOrder(AskSide('O1O3', 33.74, 8))
    setup.executeLimitOrder(BidSide('O1O4', 33.74, 2))
    assert len(setup.bidSideList) == 0 and len(
        setup.askSideList) == 1 and setup.askSideList[0].order.orderSize == 6


# test limit Marketable Sell Order
def test_limitMarketAbleSellOrder(setup):
    setup.executeLimitOrder(BidSide('O1O6', 33.74, 7))
    setup.executeLimitOrder(AskSide('O1O5', 33.74, 2))
    assert len(setup.askSideList) == 0 and len(
        setup.bidSideList) == 1 and setup.bidSideList[0].order.orderSize == 5


# test Market Sell Order
def test_MarketSellOrder(setup):
    setup.executeLimitOrder(BidSide('O1O7', 33.74, 7))
    setup.executeMarketOrder(AskSide('O1O8', 33.76, 1))
    assert len(setup.askSideList) == 0 and len(
        setup.bidSideList) == 1 and setup.bidSideList[0].order.orderSize == 6

# test Market Buy Order


def test_MarketSellOrder(setup):
    setup.executeLimitOrder(AskSide('O1O8', 33.77, 7))
    setup.executeMarketOrder(BidSide('O1O9', 33.76, 6))
    assert len(setup.askSideList) == 1 and len(
        setup.bidSideList) == 0 and setup.askSideList[0].order.orderSize == 1


# test spread
def test_spread(setup):
    setup.executeLimitOrder(AskSide('O1O8', 33.77, 7))
    setup.executeLimitOrder(BidSide('O1O8', 33.75, 1))
    setup.executeMarketOrder(BidSide('O1O9', 33.76, 6))

    assert setup.spread() == 0.02
