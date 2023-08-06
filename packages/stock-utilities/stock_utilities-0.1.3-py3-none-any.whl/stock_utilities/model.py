import typing
import enum

class OptionType(enum.Enum):
    UNDEFINED = 0
    CALL = 1
    PUT = 2

class StockHistoryDatum(typing.NamedTuple):
    time: int
    close_value: float
    open_value: float


class OptionChainDatum(typing.NamedTuple):
    type: OptionType
    strike: float
    bid: float
    open_interest: float
    currency: str,
    last_price: float
    last_trade_date: datetime.datetime


class OptionChain(typing.NamedTuple):
    calls: typing.List[OptionChainDatum]
    puts: typing.List[OptionChainDatum]
