from const import Cex, Status, Action

class Exchange:

    def __init__(self, cex: Cex, api: str, sec: str) -> None:
        self._cex = cex
        self._api = api
        self._secret = sec
        return

    @property
    def cex(self) -> str: 
        return self._cex

    @property
    def api(self) -> str:
        return self._api

    @property
    def secret(self) -> str:
        return self._secret
    
    def get_withdrawal_fee(self, sym: str, net: str) -> float:
        try:
            chains = self._client.currencies[sym.upper()]['info']['chains']
            for chain in chains:
                if chain['chain'] == net: return(float(chain['transactFeeWithdraw']))
        except Exception as e:
            raise Exception(self.logify(self.cex,Status.FAIL,Action.WDRAW,{'currency':sym, 'network':net},e))

    def get_balance(self, sym: str) -> float:
        try:
            return float(self._client.fetch_balance()[sym.upper()]['free'])
        except Exception as e:
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.FETCH,
                {'currency':sym},
                e
            ))

    def get_ask(self, counter: str, base: str) -> float:
        try:
            return float(self._client.fetch_order_book(counter+'/'+base)['asks'][0])
        except Exception as e:
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.FETCH,
                {'counter':counter, 'base':base},
                e
            ))

    def get_bid(self, counter: str, base: str) -> float:
        try:
            return float(self._client.fetch_order_book(counter+'/'+base)['bids'][0])
        except Exception as e:
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.FETCH,
                {'counter':counter, 'base':base},
                e
            ))

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
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'},
                e
            ))

    def limit_sell(self, from_curr: str, to_curr: str, amount: float, price: float) -> str:

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
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.SELL,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':prc},
                e
            ))

    def withdraw(self, from_curr: str, amount: float, to_addy: str, network: str) -> str:

        #truncate the amount to 6 decimal places
        amnt = str(self.truncate(amount,6))

        try:
            self._client.withdraw(from_curr,amnt,to_addy, params={'chain':network})
            return (self.logify(
                self.cex,
                Status.SUCC,
                Action.WDRAW,
                {'currency':from_curr, 'amount':amnt, 'address':to_addy, 'network':network},
                ('Withdrawn ' + amnt + ' ' + from_curr + ' to ' + to_addy + ' on ' + network),
            ))
        
        except Exception as e:     
            raise Exception(self.logify(
                self.cex,
                Status.FAIL,
                Action.WDRAW,
                {'currency':from_curr, 'amount':amnt, 'address':to_addy, 'network':network},
                e
            ))

    @staticmethod
    def truncate(f: float, n: int) -> str:
        """Truncates a given float to the specified decimal places

        Args:
            f (float): The float to be truncated
            n (int): The number of decimal places

        Returns:
            str: The string representation of the truncated float
        """
        
        s = '{}'.format(f)
        if 'e' in s or 'E' in s: return '{0:.{1}f}'.format(f, n)
        i, _, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])

    @staticmethod
    def logify(cex : Cex, status: Status, action: Action, params: dict, log: dict) -> str:
        """Builds a standardised error/log text

        Args:
            log (str): The log's description
            status (str): Identifies whether this log is a failure/sucess log
            action (str): The action that was trying to be done
            params (list, optional): The list of parameters for log. Defaults to [].

        Returns:
            str: A standardised error text, ready for output
        """
        return (str(status) + ' | ' + str(cex) + ' | ' + str(action) + ' | ' + str(params) + ' | ' + str(log))
