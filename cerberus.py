import sys
import json
from binance import Binance
from const import Cex, Symbol


REQUIRED_ARGS = 2

if __name__ == '__main__':

    # Ensure 3 arguments are given
    if len(sys.argv) - 1 != REQUIRED_ARGS:
        raise Exception('There must be ' + str(REQUIRED_ARGS) + ' arguments but ' + str(len(sys.argv)-1) + ' is given!')

    #Get the authentication file and exchange to use
    cex                  = sys.argv[1]
    authFile             = sys.argv[2]

    #Get the api key and secret from file, and the close it
    with open(authFile) as aFile: 
        dDump = json.load(aFile)
        apiKey = dDump['key']
        secret = dDump['secret']
        aFile.close()

    #Create an exchange instance
    if cex.lower() == Cex.BNAC: xchng = Binance(apiKey,secret)
    else: raise Exception('Exchange ' + cex + ' is not supported!')

    #sell all available BTC
    print(xchng.market_sell(Symbol.BTC,Symbol.USDC,xchng.get_balance(Symbol.BTC)))

    #exit the program
    exit()