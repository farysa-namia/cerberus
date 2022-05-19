from abc import ABC, abstractmethod
from const import Cex, Status, Action

class Exchange(ABC):

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

    @abstractmethod
    def get_balance(self, sym: str) -> float: pass

    @abstractmethod
    def get_ask(self, counter: str, base: str) -> float: pass

    @abstractmethod
    def get_bid(self, counter: str, base: str) -> float: pass

    @abstractmethod
    def market_sell(self, counter: str, base: str, amount: float) -> dict: pass

    @abstractmethod
    def limit_sell(self, counter: str, base: str, amount: float, price: float) -> dict: pass

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
