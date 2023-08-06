import typing


class StockHistoryDatum(typing.NamedTuple):
    time: int
    close_value: float
    open_value: float


class OptionChainDatum(typing.NamedTuple):
    strike: float
    bid: int


class OptionChain(typing.NamedTuple):
    calls: typing.List[OptionChainDatum]
    puts: typing.List[OptionChainDatum]
