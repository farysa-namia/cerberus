import json
from datetime import datetime as dt
from exchanges import Binance, Huobi
from const import Cex, Action
import argparse

if __name__ == '__main__':

    try:

        #get all the necessary arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('cex', help='the exchange you want to use', choices=[Cex.BNAC, Cex.HUBI])
        parser.add_argument('auth', help='the path to the api key/secret', type=str)
        parser.add_argument('action', help='what you want to do', choices=[Action.MSELL, Action.LSELL, Action.QBALC, Action.WDRAW])
        parser.add_argument('-frm', help='currency to operate from', type=str)
        parser.add_argument('-to', help='currency to operate to', type=str)
        parser.add_argument('-percent', help='percentage of holdings to sell', choices=[x for x in range(1,101)], type=int)
        parser.add_argument('-price', help='price to sell holdings for', type=float)
        parser.add_argument('-address', help='address to withdraw to', type=str)
        parser.add_argument('-network', help='network to withdraw to', type=str)

        arg = parser.parse_args()
        cex, auth, action = arg.cex, arg.auth, arg.action

        #Get the api key and secret from file, and the close it
        with open(auth) as aFile: 
            dDump = json.load(aFile)
            apiKey = dDump['key']
            secret = dDump['secret']
            aFile.close()

        #Create an exchange instance
        if cex == Cex.BNAC: xchng = Binance(apiKey,secret)
        elif cex == Cex.HUBI: xchng = Huobi(apiKey,secret)
        else: raise Exception('Exchange ' + cex + ' is not supported!')

        #if the action selected is a market sell
        if action == Action.MSELL:
            
            #ensure the frm, to, precent amount is geiven
            if arg.frm is None: raise Exception('From Currency symbol is not given!')
            if arg.to is None: raise Exception('To Currency symbol is not given!')
            if arg.percent is None: raise Exception('Percentage to sell is not given!')

            #grab the from, to and percent
            from_curr, to_curr, percent = arg.frm, arg.to, arg.percent

            #ensure the currency symbols are upper to avoid any error with exchanges
            from_curr, to_curr = from_curr.lower(), to_curr.lower()

            #get the amount to sell
            amount = xchng.get_balance(from_curr) * (percent/100)

            #sell from currency
            print(str(dt.now()) + ' | ' + xchng.market_sell(from_curr,to_curr,amount))
        
        #if the action selected is a limit sell
        elif action == Action.LSELL:

            #ensure the frm, to, precent amount is geiven
            if arg.frm is None: raise Exception('From Currency symbol is not given!')
            if arg.to is None: raise Exception('To Currency symbol is not given!')
            if arg.percent is None: raise Exception('Percentage to sell is not given!')
            if arg.price is None: raise Exception('Price to sell is not given!')

            #grab the from, to, percent and price
            from_curr, to_curr, percent, price = arg.frm, arg.to, arg.percent, arg.price

            #ensure the currency symbols are upper to avoid any error with exchanges
            from_curr, to_curr = from_curr.lower(), to_curr.lower()

            #get the amount to sell
            amount = xchng.get_balance(from_curr) * (percent/100)

            #sell from currency
            print(str(dt.now()) + ' | ' + xchng.limit_sell(from_curr,to_curr,amount,price))
        
        elif action == Action.QBALC:

            #ensure the frm, to, precent amount is geiven
            if arg.frm is None: raise Exception('From Currency symbol is not given to check balance!')

            #grab the from currecnyc
            from_curr = arg.frm

            #ensure the currency symbols are lowered to avoid any error with exchanges
            from_curr = from_curr.lower()

            #get the balance for the currency
            print(str(dt.now()) + ' | ' + cex + ' | ' + from_curr + ' | ' + 'balance : ' + str(xchng.get_balance(from_curr)))

        #if the action selected is withdraw
        elif action == Action.WDRAW:

            #ensure the frm, to_address, percentage is given
            if arg.frm is None: raise Exception('From Currency symbol is not given!')
            if arg.percent is None: raise Exception('Percentage to withdraw is not given!')
            if arg.address is None: raise Exception('Address to withdraw to is not given!')
            if arg.network is None: raise Exception('Network is not given!')

            #grab the from, to, percent and price
            from_curr, percent, addy, net = arg.frm, arg.percent, arg.address, arg.network

            #get the amount to withdraw (less fees)
            amount = (xchng.get_balance(from_curr) * (percent/100)) - xchng.get_withdrawal_fee(from_curr, net)

            #withdraw the currency to address
            print(str(dt.now()) + ' | ' + xchng.withdraw(from_curr,amount,addy, net))
            

    #all errors will be printed out to console
    except Exception as e:
        print(str(dt.now()) + ' | ' + str(e))

    #exit the program
    finally:
        exit()
