from base import Exchange
import ccxt
from const import Cex

class Binance(Exchange):

    def __init__(self, api: str, sec: str) -> None:
        super().__init__(Cex.BNAC, api, sec)
        self._client = ccxt.binance(config={'apiKey':api,'secret':sec})

    def get_balance(self, sym: str) -> float:
        return super().get_balance(sym)

    def get_ask(self, counter: str, base: str) -> float:
        return super().get_ask(counter,base)
    
    def get_bid(self, counter: str, base: str) -> float:
        return super().get_bid(counter,base)

    def market_sell(self, from_curr: str, to_curr: str, amount: float) -> str:
        return super().market_sell(from_curr,to_curr,amount)
    
    def limit_sell(self, from_curr: str, to_curr: str, amount: float, price: float) -> dict:
        return super().limit_sell(from_curr,to_curr,amount,price)

class Huobi(Exchange):

    def __init__(self, api: str, sec: str) -> None:
        super().__init__(Cex.HUBI, api, sec)
        self._client = ccxt.huobi(config={'apiKey':api,'secret':sec})
        return

    def get_balance(self, sym: str) -> float:
        return super().get_balance(sym)

    def get_ask(self, counter: str, base: str) -> float:
        return super().get_ask(counter,base)
    
    def get_bid(self, counter: str, base: str) -> float:
        return super().get_bid(counter,base)

    def market_sell(self, from_curr: str, to_curr: str, amount: float) -> str:
        return super().market_sell(from_curr,to_curr,amount)
    
    def limit_sell(self, from_curr: str, to_curr: str, amount: float, price: float) -> dict:
        return super().limit_sell(from_curr,to_curr,amount,price)


