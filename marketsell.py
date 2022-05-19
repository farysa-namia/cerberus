import sys
import json
from datetime import datetime as dt
from exchanges import Binance
from const import Cex


REQUIRED_ARGS = 4

if __name__ == '__main__':

    try:

        # Ensure 3 arguments are given
        if len(sys.argv) - 1 != REQUIRED_ARGS:
            raise Exception('There must be ' + str(REQUIRED_ARGS) + ' arguments but ' + str(len(sys.argv)-1) + ' is given!')

        #Get the authentication file and exchange to use
        cex                  = sys.argv[1].lower()
        authFile             = sys.argv[2]
        ccounter             = sys.argv[3].lower()
        cbase                = sys.argv[4].lower()

        #Get the api key and secret from file, and the close it
        with open(authFile) as aFile: 
            dDump = json.load(aFile)
            apiKey = dDump['key']
            secret = dDump['secret']
            aFile.close()

        #Create an exchange instance
        if cex == Cex.BNAC: xchng = Binance(apiKey,secret)
        else: raise Exception('Exchange ' + cex + ' is not supported!')

        #sell all available base currencys
        print(str(dt.now()) + ' | ' + xchng.market_sell(ccounter,cbase,xchng.get_balance(cbase)))

    except Exception  as e:
        print(str(dt.now()) + ' | ' + e)

    finally:
        exit()