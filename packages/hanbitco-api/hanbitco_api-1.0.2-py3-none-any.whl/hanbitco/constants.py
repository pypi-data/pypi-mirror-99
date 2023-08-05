from enum import Enum

ORIGIN = "api.hanbitcotest.com"


class OrderType(Enum):
    LIMIT = "LIMIT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    WAIT = "WAIT"
    DONE = "DONE"
    CANCEL = "CANCEL"
