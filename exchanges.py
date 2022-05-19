from base import Exchange
import ccxt as c
from const import Cex, Status, Action

class Binance(Exchange):

    def __init__(self, api: str, sec: str) -> None:
        super().__init__(Cex.BNAC, api, sec)
        self._client = c.binance(config={'apiKey':api,'secret':sec})

    def get_balance(self, sym: str) -> float:
        return float(self._client.fetch_balance()[sym.upper()]['free'])

    def get_ask(self, counter: str, base: str) -> float:
        return float(self._client.fetch_order_book(counter+'/'+base)['asks'][0])
    
    def get_bid(self, counter: str, base: str) -> float:
        return float(self._client.fetch_order_book(counter+'/'+base)['bids'][0])

    def market_sell(self, from_curr: str, to_curr: str, amount: float) -> str:

        #fetch the amount of availble balance for from_currency
        amnt = str(self.truncate(amount,6))

        #sell the currency using market price
        try:
            self._client.create_market_sell_order((from_curr+'/'+to_curr).upper(),amnt)
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'},
                ('Traded ' + amnt + ' ' + from_curr + ' to ' + to_curr + ' at market price.'),
            ))

        except Exception as e:     
            return (self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'},
                e
            ))
    
    def limit_sell(self, from_curr: str, to_curr: str, amount: float, price: float) -> dict:

        #fetch the amount of availble balance for from_currency and convert given price to string
        amnt = str(self.truncate(amount,6))
        prc = str(price)

        #sell the currency using given price
        try:
            self._client.create_limit_sell_order((from_curr+'/'+to_curr).upper(),amnt,prc)
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':prc},
                ('Traded ' + amnt + ' ' + from_curr + ' to ' + to_curr + ' at ' + prc + ' ' + from_curr + ' per ' + to_curr),
            ))

        except Exception as e:     
            return (self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':prc},
                e
            ))

class Huobi(Exchange):

    def __init__(self, api: str, sec: str) -> None:
        super().__init__(Cex.HUBI, api, sec)
        self._client = c.huobi(config={'apiKey':api,'secret':sec})

    def get_balance(self, sym: str) -> float:
        return float(self._client.fetch_balance()[sym.upper()]['free'])

    def get_ask(self, counter: str, base: str) -> float:
        return float(self._client.fetch_order_book(counter+'/'+base)['asks'][0])
    
    def get_bid(self, counter: str, base: str) -> float:
        return float(self._client.fetch_order_book(counter+'/'+base)['bids'][0])

    def market_sell(self, from_curr: str, to_curr: str, amount: float) -> str:

        #fetch the amount of availble balance for from_currency
        amnt = str(self.truncate(amount,6))

        #sell the currency using market price
        try:
            self._client.create_market_sell_order((from_curr+'/'+to_curr).upper(),amnt)
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'},
                ('Traded ' + amnt + ' ' + from_curr + ' to ' + to_curr + ' at market price.'),
            ))

        except Exception as e:     
            return (self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'},
                e
            ))
    
    def limit_sell(self, from_curr: str, to_curr: str, amount: float, price: float) -> dict:

        #fetch the amount of availble balance for from_currency and convert given price to string
        amnt = str(self.truncate(amount,6))
        prc = str(price)

        #sell the currency using given price
        try:
            self._client.create_limit_sell_order((from_curr+'/'+to_curr).upper(),amnt,prc)
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':prc},
                ('Traded ' + amnt + ' ' + from_curr + ' to ' + to_curr + ' at ' + prc + ' ' + from_curr + ' per ' + to_curr),
            ))

        except Exception as e:     
            return (self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':prc},
                e
            ))
