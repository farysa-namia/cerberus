class Action:
    INIT = 'initialise'
    SELL = 'sell'
    BUY  = 'buy'
    WDRAW = 'withdraw'
    FETCH = 'fetch'
    MSELL = 'marketsell'
    LSELL = 'limitsell'
    QBALC = 'balance'

class Status:
    FAIL = 'fail'
    SUCC = 'success'

class Cex:
    BNAC = 'binance'
    HUBI = 'huobi'
    NONE = 'none'