from base import Exchange
from ccxt import binance
from const import Cex, Status, Action

class Binance(Exchange):

    def __init__(self, api: str, sec: str) -> None:
        super().__init__(Cex.BNAC, api, sec)
        self._client = binance(config={'apiKey':api,'secret':sec})

    def get_balance(self, sym: str) -> float:
        return float(self._client.fetch_balance()[sym]['free'])

    def get_price(self, counter: str, base: str) -> float:
        return super().get_price(counter, base)

    def market_sell(self, counter: str, base: str, amount: float) -> str:

        #fetch the amount of availble balance for from_currency
        amnt = str(self.truncate(amount,6))

        #sell the currency using market price
        try:
            self._client.create_market_sell_order(counter+'/'+base,amnt)
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.SELL,
                {'from':base, 'to':counter, 'amount':amnt, 'rate':'market'},
                ('Traded ' + amnt + ' ' + base + ' to ' + counter + ' at market price.'),
            ))

        except Exception as e:     
            return (self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':base, 'to':counter, 'amount':amnt, 'rate':'market'},
                e
            ))