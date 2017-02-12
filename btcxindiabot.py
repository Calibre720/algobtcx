import urllib,urllib2
import requests
import json
import time
import hashlib
import hmac
import logging
import config
import base64

class Btcxindia:

    def __init__(self):
        #config variables
        self.apikey = config.apikey
        self.apisecret = config.apisecret
        self.clientid = config.clientid
        #ticker variables
        self.high = 0
        self.low = 0
        self.avg = 0
        self.totalvolume24 = 0
        self.currentvolume = 0
        self.lasttradedprice = 0
        self.lasttradedtime = 0
        self.bid = 0
        self.ask = 0
        #hourly ticker variables
        self.high_hour = 0
        self.low_hour = 0
        self.avg_hour = 0
        self.totalvolumehour = 0
        #orderbook variables
        self.orderbooktime = 0
        self.orderbookbids = []
        self.orderbookasks = []
        self.trades = []
        #balance variables
        self.balanceinr = -1
        self.balancebtc = -1
        self.balancetradefee = -1
        self.balance_error = -1
        #pending orders variables
        self.pending_orders = []

    def trade(self,buyorsell,volume,price):

        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "type":buyorsell,
                      "volume":volume,
                      "price":price}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/trade/',parameters)
            resp=json.load(response)
            print resp
            if resp[u'status']=='success':
                trade_orderid = resp[u'order_id']
                print resp
                logging.info('btcxindia TRADE CONNECTION SUCCESSFUL')
                response.close()
                return trade_orderid
            else:
                print 'RESPONSE STATUS = ERROR'
                return -1
        except:
            etype, foo, traceback = sys.exc_info()
            print 'foo %s' % foo


    def tradehistory(self,buyorsell,volume,price):

        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "type":buyorsell,
                      "volume":volume,
                      "price":price}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/trade/',parameters)
            resp=json.load(response)
            print resp
            if resp[u'status']=='success':
                trade_orderid = resp[u'order_id']
                print resp
                logging.info('btcxindia TRADE CONNECTION SUCCESSFUL')
                response.close()
                return trade_orderid
            else:
                print 'RESPONSE STATUS = ERROR'
                return -1
        except:
            etype, foo, traceback = sys.exc_info()
            print 'foo %s' % foo


    def balance(self):

        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce}
        parameters = urllib.urlencode(parameters)

        try:
            response = urllib2.urlopen('https://api.btcxindia.com/ac_balance/',parameters)
            resp = json.load(response)


            if response.getcode()==200:
                if resp[u'status'] == 'success':
                    logging.info('btcxindia BALANCE CHECK SUCCESSFUL')
                    response.close()
                    return resp[u'inr'],resp[u'btc'],resp[u'pending_inr'],resp[u'pending_btc']
            else:
                return -1,-1,-1,-1
        except urllib2.URLError, e:
            logging.warning('btcxindia BALANCE CHECK CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia BALANCE CHECK CONNECTION ERROR. Error Code:%r' % e
            return -2,e,e,e

    def pendingorders(self):

        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce}
        parameters = urllib.urlencode(parameters)

        try:
            response = urllib2.urlopen('https://api.btcxindia.com/my_pending_orders/',parameters)
            resp=json.load(response)
            if response.getcode()==200:
                self.pending_orders = resp
                logging.info('btcxindia fetch pending orders SUCCESSFUL')
                response.close()
                return [[x[u'order_id'],x[u'volume'],x[u'order_type'],x[u'inr_btc'],x[u'time']] for x in resp]

            else:
                return -1
        except urllib2.URLError, e:
            logging.warning('btcxindia fetch pending orders CONNECTION ERROR. Error Code: %r' % e)
            print
            print 'btcxindia fetch pending orders CONNECTION ERROR. Error Code:%r' % e
            return -2

    def cancelorder(self,orderid):
        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "order_id":orderid}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/cancel_order/',parameters)
            resp=json.load(response)
            if response.getcode()==200:
                print resp
                logging.info('btcxindia CANCEL ORDER SUCCESSFUL')
                response.close()
                print
                print resp
                return resp[u'status']
            else:
                return -1
        except urllib2.URLError, e:
            logging.warning('btcxindia CANCEL ORDER CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia CANCEL ORDER CONNECTION ERROR. Error Code: + %r' % e
            return -2

    def transactions(self,typeoftransaction):
        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "type":typeoftransaction}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/transactions/',parameters)
            resp=json.load(response)
            if response.getcode()==200:
                #if self.typeoftransaction == 'trade':
                #if self.typeoftransaction == 'deposit':
                #if self.typeoftransaction == 'withdrawal':
                logging.info('btcxindia transactions SUCCESSFUL')
                print
                print 'btcxindia transactions SUCCESSFUL'
            response.close()
        except urllib2.URLError, e:
            logging.warning('btcxindia transactions CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia transactions CONNECTION ERROR. Error Code:%r' % e

    def initiatewithdrawal(self,btcorinr,amount,address):
        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "type":btcorinr,
                      "amount":amount,
                      "address":address}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/withdrawalinitiate/',parameters)
            resp=json.load(response)
            if response.getcode()==200:
                logging.info('btcxindia withdrawal initiation successful SUCCESSFUL')
                print
                print 'btcxindia withdrawal initiation successful SUCCESSFUL'
            response.close()
        except urllib2.URLError, e:
            logging.warning('btcxindia withdrawal initiation  CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia withdrawal initiation  CONNECTION ERROR. Error Code:%r' % e


    def confirmwithdrawal(self,withdrawal):
        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "withdrawal_code":withdrawalcode}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/withdrawal_confirm/',parameters)
            resp=json.load(response)
            if response.getcode()==200:
                logging.info('btcxindia withdrawal confirmation SUCCESSFUL')
                print
                print 'btcxindia withdrawal confirmation SUCCESSFUL'
            response.close()
        except urllib2.URLError, e:
            logging.warning('btcxindia withdrawal confirmation CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia withdrawal confirmation CONNECTION ERROR. Error Code:%r' % e


    def wallet(self,btcorinr):
        nonce = int(time.time())
        Data = str(nonce) + self.apikey + self.clientid
        signature = base64.b64encode(hmac.new(self.apisecret,Data,digestmod=hashlib.sha256).digest())

        parameters = {"key":self.apikey,
                      "signature":signature,
                      "nonce":nonce,
                      "type":btcorinr}
        parameters = urllib.urlencode(parameters)
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/wallet/',parameters)
            resp=json.load(response)
            print
            print resp
            logging.info('btcxindia wallet check SUCCESSFUL')
            print
            print 'btcxindia wallet check SUCCESSFUL'
            response.close()
        except urllib2.URLError, e:
            logging.warning('btcxindia wallet check CONNECTION ERROR. Error Code:%r' % e)
            print
            print 'btcxindia wallet check CONNECTION ERROR. Error Code:%r' % e


    def ticker(self):
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/ticker/')
            resp=json.load(response)
            self.high = resp[u'high']
            self.low = resp[u'low']
            self.avg = resp[u'avg']
            self.totalvolume24 = resp[u'total_volume_24h']
            self.currentvolume = resp[u'current_volume']
            self.lasttradedprice = resp[u'last_traded_price']
            self.lasttradedtime = resp[u'last_traded_time']
            self.bid = resp[u'bid']
            self.ask = resp[u'ask']
            logging.info('btcxindia Ticker Update SUCCESSFUL')
            response.close()
            return 1
        except urllib2.URLError, e:
            print ("There was an error: %r" % e)
            logging.warning('btcxindia Ticker CONNECTION ERROR. Error Code:')
            return e
    def hourlyticker(self):
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/ticker_hour/')
            resp=json.load(response)
            self.high_hour = resp[u'high']
            self.low_hour = resp[u'low']
            self.avg_hour = resp[u'avg']
            self.totalvolumehour = resp[u'total_volume_hour']
            logging.info('btcxindia HourlyTicker Update SUCCESSFUL')
            response.close()
            return 1
        except urllib2.URLError, e:
            print ("There was an error: %r" % e)
            logging.warning('btcxindia Hourly Ticker CONNECTION ERROR. Error Code:')
            return e
    def orderbook(self):
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/order_book/')
            resp=json.load(response)
            self.orderbooktime = resp[u'timestamp']
            self.orderbookbids = resp[u'bids']
            self.orderbookasks = resp[u'asks']
            logging.info('btcxindia Orderbook Update SUCCESSFUL')
            response.close()
            return 1
        except urllib2.URLError, e:
            logging.warning('btcxindia orderbook CONNECTION ERROR. Error Code:%r' % e)
            return e

    def tradesnow(self):
        try:
            response = urllib2.urlopen('https://api.btcxindia.com/trades')
            resp=json.load(response)
            self.trades = [[x[u'time'],x[u'volume'],x[u'price']] for x in resp]
            logging.info('btcxindia Tradesnow Update SUCCESSFUL')
            response.close()
            return 1
        except urllib2.URLError, e:
            logging.warning('btcxindia Tradesnow CONNECTION ERROR. Error Code:%r' % e)
            return e

    def updatedata(self):
        self.ticker()
        self.hourlyticker()
        self.orderbook()
        self.tradesnow()
        while True:
            time.sleep(10)
            self.ticker()
            time.sleep(10)
            self.hourlyticker()
            time.sleep(10)
            self.orderbook()
            time.sleep(10)
            self.tradesnow()
