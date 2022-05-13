import sys
import ccxt
import json
from datetime import datetime as dt

REQUIRED_ARGS = 3
CEX_MODE = 'Huobi'

class Action:
    INIT = 'initialise'
    TRADE = 'trade'
    WITHDRAW = 'withdraw'

class Status:
    FAIL = 'fail'
    SUCCESS = 'success'

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

def logify(log: str, status: Status, action: Action, params: dict = {}) -> str:
    """Builds a standardised error/log text

    Args:
        log (str): The log's description
        status (str): Identifies whether this log is a failure/sucess log
        action (str): The action that was trying to be done
        params (list, optional): The list of parameters for log. Defaults to [].

    Returns:
        str: A standardised error text, ready for output
    """
    return (str(dt.now()) + ' | ' + status + ' | ' + CEX_MODE + ' | ' + action + ' | ' + str(params) + ' | ' + str(log))


if __name__ == '__main__':

    try:

        # Ensure 3 arguments are given
        if len(sys.argv) - 1 != REQUIRED_ARGS:
            raise Exception(
                logify(
                ('There must be ' + str(REQUIRED_ARGS) + ' arguments but ' + str(len(sys.argv)-1) + ' is given!'),
                Status.FAIL,
                Action.INIT,
                {'n_arguments_give': str(len(sys.argv)-1)}
                )
            )

        #Get the authentication file, along with the currency-pair to trade
        authFile        = sys.argv[1]
        from_curr       = sys.argv[2]
        to_curr         = sys.argv[3]

        #Get the api key and secret from file, and the close it
        with open(authFile) as aFile: 
            dDump = json.load(aFile)
            apiKey = dDump['key']
            secret = dDump['secret']
            aFile.close()

        #Create an exchange instance (Huobi in this instance)
        xchng = ccxt.huobi()

        #Init xchange instance credentials
        xchng.apiKey = apiKey
        xchng.secret = secret

        #Ensure sufficient credentials given for exchange
        try: 
            xchng.check_required_credentials() 
        except Exception as e: 
            raise Exception(logify(
                str(e),
                Status.FAIL,
                Action.INIT,
                {'file':authFile, 'from':from_curr, 'to':to_curr}
            ))

        #fetch the amount of availble balance for from_currency
        amnt = str(truncate(float(xchng.fetch_balance()[from_curr]['free']),6))

        #sell the currency using market price
        try:
            xchng.create_market_sell_order(from_curr+'/'+to_curr,amnt)
            print(logify(
                ('Traded ' + amnt + ' ' + from_curr + ' to ' + to_curr + ' at market price.'),
                Status.SUCCESS,
                Action.TRADE,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'}
            ))
        except Exception as e:        
            raise Exception(logify(
                str(e),
                Status.FAIL,
                Action.TRADE,
                {'from':from_curr, 'to':to_curr, 'amount':amnt, 'rate':'market'}
            ))
    
    except Exception as e:

        #print out any errors/logs to console
        print(e)

    finally:

        #ensure program exits
        exit()