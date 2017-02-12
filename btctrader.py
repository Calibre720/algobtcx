# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 02:21:10 2015

@author: calibre720
"""
import config
import logging
from pprint import pprint
import urllib2
import threading
import time,json
import btcxindiabot
import algorithm
import sys

logging.basicConfig(filename=config.address + 'btctrader.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
logging.info('Bot Alive')
print '\nBot Alive'

if config.proxyhost!='' or config.proxyport!='':
    proxy = urllib2.ProxyHandler({'https': config.proxyhost + ':' + config.proxyport})
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    logging.info('Proxy Set')
    print '\nProxy Set'

else:
    proxy = urllib2.ProxyHandler({'https': config.proxyhost + ':' + config.proxyport})
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)

btcx = btcxindiabot.Btcxindia()
logging.info('Btcxindiabot Object Created')

def callupdatebtcx():
    threadupdatebtcx = threading.Thread(target = btcx.updatedata)
    threadupdatebtcx.daemon = True
    threadupdatebtcx.start()
    logging.info('Started btcxindia data updation thread.')
    print
    print 'Started btcxindia data updation thread.'

def callautobot():
    threadautobot = threading.Thread(Target = algorithm.autobot)
    threadautobot.daemon = True
    threadautobot.start()
    logging.info('AUTOBOT BORN')
    print '\nAUTOBOT ALIVE'


x = raw_input('\nRun in MANUAL MODE ???  Enter Y/N/EXIT - ').lower()

while x!='exit':
    if x=='y' or x=='yes' or x==1:
        logging.info('ENTERED MANUAL MODE')
        print '\nENTERED MANUAL MODE\n'
        z = 'help'
        while z!='exit':
            if z=='update':
                print
                print 'UPDATING:  |                              | 0% DONE'
                btcx.ticker()
                sys.stdout.write('\033[F')
                print 'UPDATING:  |///////                       | 25% DONE'
                btcx.hourlyticker()
                sys.stdout.write('\033[F')
                print 'UPDATING:  |///////////////               | 50% DONE'
                btcx.orderbook()
                sys.stdout.write('\033[F')
                print 'UPDATING:  |///////////////////////       | 75% DONE'
                btcx.tradesnow()
                sys.stdout.write('\033[F')
                print 'UPDATING:  |//////////////////////////////| 100% DONE'
                print '\nBTCXINIDA UPDATE SUCCESSFUL'
                print '\nBID = ', btcx.bid
                print 'ASK = ', btcx.ask
                print 'HIGH = ', btcx.high
                print 'LOW = ',btcx.low
                print 'AVERAGE = ', btcx.avg
                print 'CURRENT VOLUME = ', btcx.currentvolume
                print 'LAST TRADED PRICE = ', btcx.lasttradedprice
                print 'LAST TRADED TIME = ', btcx.lasttradedtime
                print 'TOTAL VOLUME TRADED IN LAST 24 HOURS = ', btcx.totalvolume24

                print '\nTOTAL VOLUME TRADED IN THIS HOUR = ', btcx.totalvolumehour
                print 'HIGH REACHED LAST HOUR = ', btcx.high_hour
                print 'LOW REACHED LAST HOUR = ', btcx.low_hour
                print 'AVERAGE LAST HOUR = ', btcx.avg_hour

                print '\nORDER BOOK TIME STAMP = ', btcx.orderbooktime
                print '\nBID ORDERS FOR THIS TIME STAMP = '
                print '\n[NO.OFBTC  RATE  NO.OFORDERS]\n'
                print pprint(btcx.orderbookbids)
                print '\nASK ORDERS FOR THIS TIME STAMP = '
                print '\n[NO.OF BTC  RATE  NO.OF ORDERS]\n'
                print pprint(btcx.orderbookasks)
                print '\nRECENT TRADES = '
                print '\n[TIME    NO.OF BTC   RATE]\n'
                print pprint(btcx.trades)
                print '\nBTCXINIDA UPDATE COMPLETE'

            elif z=='balance':
                inr,btc,peninr,penbtc = btcx.balance()
                if inr==-1 or inr==-2:
                    print '\nERROR ',btc
                else:
                    print '\nBALANCE = ',inr, 'RUPPEES'
                    print 'BALANCE = ', btc, 'BTC'
                    print 'PENDING INR = ',peninr,'RUPPEES'
                    print 'PENDING BTC',penbtc,'BTC'

            elif z=='pending':
                pending = btcx.pendingorders()
                if pending==-1 or pending==-2:
                    print '\nERROR',pending
                else:
                    print '\n[OrderID  Volume  Type  Rate  Time]\n'
                    print pending

            elif z=='trade':

                typeoftransaction = raw_input('B or S? (C to cancel)- ').lower()
                while(typeoftransaction!='b' and typeoftransaction!='s' and typeoftransaction!='c'):
                    print 'Enter B or S or C for Buy - Sell - Cancel'
                    typeoftransaction = raw_input('B or S? (C to cancel)- ').lower()
                    print

                if(typeoftransaction=='c'):
                    break

                Volumeoftrade = float(raw_input('Volume? (multiples of 0.1) - '))
                while(Volumeoftrade*10!=int(Volumeoftrade*10)):
                    print 'Enter in multiples of 0.1'
                    Volumeoftrade = float(raw_input('Volume? (multiples of 0.1) - '))
                    print

                rate = int(raw_input('Rate? (multiples of 10) - '))
                while((rate/10)*10!=rate):
                    print 'Enter in multiples of 10'
                    rate = raw_input('Rate? (multiples of 10) - ')


                print '\nExecuting Order\n'
                tradeorder = btcx.trade(typeoftransaction,Volumeoftrade,rate)
                if tradeorder==-1 or tradeorder==-2:
                    print '\nError ',tradeorder
                else:
                    print '\nTrade Successful ', typeoftransaction,price,Volumeoftrade
                    print '\nTrade Order-ID = ', tradeorder
            elif z=='cancel':
                cancelid = raw_input('Enter TradeID to cancel?')
                print btcx.cancelorder(cancelid)

            elif z=='help' or z=='h':
                print '\nCOMMAND LIST:'
                print '\nUPDATE'
                print 'BALANCE'
                print 'PENDING'
                print 'TRADE'
                print 'CANCEL'
                print 'EXIT //To exit manual mode'
                print 'HELP\n'

            else:
                print
                print z + ' COMMAND NOT FOUND'
                print '\nCOMMAND LIST:'
                print '\nUPDATE'
                print 'BALANCE'
                print 'PENDING'
                print 'TRADE'
                print 'CANCEL'
                print 'EXIT //To exit manual mode'
                print 'HELP\n'

            z = raw_input('\nExecute COMMAND: - ').lower()
            print
        x = 'anything other than y or n'

    elif x=='no' or x=='n' or x==0:
        logging.info('ENTERED AUTOMATED MODE')
        print '\nENTERED AUTOMATED MODE'
        callupdatebtcx()
        callautobot()

    else :
        x = raw_input('\nRun in Manual Mode? Enter Y/N/EXIT - ').lower()

logging.info('Killing bot')
print '\nKilling bot'
