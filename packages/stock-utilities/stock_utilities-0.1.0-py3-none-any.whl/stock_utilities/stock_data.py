import abc
import datetime
import typing

from . import model, proxy


class StockData(abc.ABC):
    symbol: str
    data_proxy: proxy.DataProxy

    def __init__(self, symbol: str, data_proxy: typing.Type[proxy.DataProxy]):
        self.symbol = symbol
        self.data_proxy = data_proxy(symbol)

    def get_last_price(self) -> float:
        return self.data_proxy.get_last_price()

    def get_stock_price_history(
        self, interval: datetime.timedelta, period: datetime.timedelta
    ) -> typing.List[model.StockHistoryDatum]:
        return self.data_proxy.get_stock_price_history(interval, period)

    def get_option_chain(self, date: datetime.datetime) -> model.OptionChain:
        return self.data_proxy.get_option_chain(date)

    def get_next_friday_option_chain(self) -> model.OptionChain:

        today = datetime.datetime.today()
        next_friday_days = datetime.timedelta(days=(4 - today.weekday()) % 7)

        next_friday = today + next_friday_days
        return self.data_proxy.get_option_chain(next_friday)
