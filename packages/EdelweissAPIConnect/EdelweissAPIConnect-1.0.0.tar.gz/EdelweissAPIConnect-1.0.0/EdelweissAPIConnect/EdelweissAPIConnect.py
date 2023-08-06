"""
    Edelweiss API Connect for Python


    The library
    -----------
    Edelweiss API Connect is a set of REST-like APIs that expose
    many capabilities required to build a complete
    investment and trading platform. Execute orders in
    real time, manage user portfolio, stream live market
    data (WebSockets), and more, with the simple HTTP API collection
    This module provides an easy to use abstraction over the HTTP APIs.
    The HTTP calls have been converted to methods and their JSON responses
    are returned as native Python structures, for example, dicts, lists, bools etc.

    Getting started
    ---------------
        #!python
        import EdelweissAPIConnect


        # Redirect the user to the login url - https://ewuat.edelbusiness.in/ewhtml/app/login?v=3&api_key=APIKEY
        # after the login flow, You will get request_id.
        # Generate a session with this request id
        # as follows.
        edel = EdelweissAPIConnect.EdelweissAPIConnect("api_key_here", "api_secret", "request_id")

        # Place an order
        response = edel.PlaceTrade('Symbol',
                                  'Exchange',
                                  'Buy-Sell',
                                  'Validity',
                                  'OrderType',
                                  'Quantity',
                                  'ExchangeCode',
                                  'LimitPrice',
                                  'ProductCode')

        # Fetch all orders
        edel.OrderBook()
        #Fetch all trades
        edel.TradeBook()

    A typical web application
    -------------------------
    In a typical web application where a new instance of
    views, controllers etc. are created per incoming HTTP
    request, you will need to initialise a new instance of
    Edelweiss API Connect client per request as well. This is because each
    individual instance represents a single user that's
    authenticated, unlike an **admin** API where you may
    use one instance to manage many users.
    Hence, in your web application, typically:
    - You will initialise an instance of the Edelweiss client
    - Redirect the user to the `login_url()`
    - At the redirect url endpoint, obtain the
    `request_id` from the query parameters
    - Pass this 'request_id' along with 'api_key' and 'api_secret'
    at the time of initialization

    """

import csv
import json
import os
import socket
import sys
import urllib
import zipfile
from os import path

import requests


class EdelweissAPIConnect:
    '''

    This is **EdelweissAPIConnect** class. Please initialise single instance of this per `api_key`.

    `api_key` : API key provided by Edelweiss

    `api_secret` : Password provided by Edelweiss

    `request_id` : Token to be collected post redirection from Login URL https://ewuat.edelbusiness.in/ewhtml/app/login?v=3&api_key=APIKEY

    `downloadContract': If this is set to `True` then It will download all the contracts and return the records in dictionary `instruments`.

    '''
    # Initilization of EdelweissAPIConnect Class
    ##Inputs Required : APIKey, Password and Request ID generated post Login
    def __init__(self, ApiKey, Password, reqID, downloadContract: bool):
        """


        Construct a new 'EdelweissAPIConnect' object.

        ApiKey: API key provided by Edelweiss

        Password: Password provided by Edelweiss

        reqID: Token to be collected post redirection from URL


        """
        self.version = '1.0.0'
        self.dc = downloadContract
        self.instruments = []

        self.__config = self.__Config()
        self. \
            __constants = self.__Constants()
        self.__http = self.__Http(self.__constants)

        self.__constants.set_ApiKey(ApiKey)
        self.__constants.set_AppIdKey(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjE2Mzk3MzMyLCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjAiLCJhcHBpZCI6ImQ5MDM1NjFiZTFhYWUyYWY3M2RjZTJjOWJhODFiODViIiwiaXNzIjoiZW10IiwiZXhwIjoxNjE2NDM3ODAwLCJpYXQiOjE2MTYzOTc2MzJ9.iy2c_iialRdLSTLcHMHD0JM81DDUMHwGx9SrreVass8")

        # LIVE-> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjE2Mzk3MzMyLCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjAiLCJhcHBpZCI6ImQ5MDM1NjFiZTFhYWUyYWY3M2RjZTJjOWJhODFiODViIiwiaXNzIjoiZW10IiwiZXhwIjoxNjE2NDM3ODAwLCJpYXQiOjE2MTYzOTc2MzJ9.iy2c_iialRdLSTLcHMHD0JM81DDUMHwGx9SrreVass8

        # UAT-> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjE2Mzk3NDQxLCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjAiLCJhcHBpZCI6IjE2OTExYTA1ZDU4ZTI5YjVmNTMyZTE3MzRkYzQyMjI2IiwiaXNzIjoiZW10IiwiZXhwIjoxNjE2NDM3ODAwLCJpYXQiOjE2MTYzOTc3NDF9.X2L9kMZjK2yzK5wLiOk2gnF73j5q4WnQtAq26W9XFM4
        if path.exists("readme.txt"):
            read = open("readme.txt", 'r').read()
            j = json.loads(read)
            self.__constants.set_VendorSession(j['vt'])
            self.__constants.set_JSession(j['auth'])
            self.__constants.set_AccId(j['accid'])
            self.__constants.set_Data(j['data'])
            self.__constants.set_AppIdKey(j['appidkey'])
        else:
            self.__VendorSession = self.GenerateVendorSession(ApiKey, Password)
            self.__Authorization = self.GetAuthorization(reqID)

        # self.__feed = self.__Feed(self.__constants, self.__config)
        # self.cb = feedMessage_callback
        self.__CheckUpdate()

        self.Instruments()

        self.orderType = ['LIMIT', 'MARKET', 'STOP_LIMIT', 'STOP_MARKET']
        '''
        Several instruments exist between multiple exchanges and segments that trade. Any trading application has to have a master list of these instruments. The instruments API provides a consolidated, import-ready CSV list of instruments available for trading.
                
        Order Types:

        - `LIMIT` - Limit orders are orders where you strictly define the purchase or sell price. Whenever there is available quantity for the given limit price the order will get executed at that price. There is a chance that your limit price order may not get executed at all or may get executed partially in case adequate quantity is not available at the specified Limit price.

        - `MARKET` - Market orders will place an order which is nearly guaranteed to get executed at the best available price in market. What this means is that if you are trying to buy then you will get whatever quantity is available in the market at the lowest available sell price. If you are trying to sell you will get the quantity at the highest available buy price.

        - `STOP_LIMIT` - This is a stop loss limit order. It mainly contains of 2 parts to consider there is a limit price and there is a trigger price. The trigger price is the price which needs to be breached (either on high side in case of Stop Loss Sell orders, or on lower side in case of Stop Loss Buy orders). Once the trigger price is breached then an order is placed for your required action (i.e. buy or sell) at the Limit price similar to a Limit order.

        - `STOP_MARKET` - This is a stop loss market order. Think of it as a stop loss limit order without requiring to set a limit price. Whenever the trigger price is breached then the system will place a market order which is almost guaranteed to get executed.
        
        '''
        self.productType = ['BO', 'CO', 'CNC', 'MIS', 'NRML', 'MTF']
        '''
        Product Types:
        
        BO -This is a 3 leg order where you can specify your original order, a profit booking order and a stop loss order all at one go. Here the main functionality will involve placing a limit order (either buy or sell) and then specifying the trigger prices at which you will look to book profit and limit your loss, these will be specified in the form of trigger prices and will end up placing market orders squaring off whenever a particular trigger is breached. In case of one of the trigger orders getting placed the pending trigger order will get auto cancelled. So in case you placed a bracket order for reliance industries with 1000 as limit and 100 as trigger for profit and 50 as trigger for stop loss, it means that in case the LTP goes above 1100 or goes below 950 the respective profit or stop loss trigger will get invoked and close out the entire position. Please note that bracket orders are intraday orders.w
        
        CO - Pay a fraction of total order amount (10% or Rs. 20) to own the shares. In case it falls below the following price, sell it off to prevent me losing money from sharp price drops.
        
        CNC - Pay total order amount to own the shares.
        
        MIS - Pay a fraction of total order amount (10% or Rs. 20) to own the shares. You can hold the stocks till market closes today (3:15pm) or sell it off anytime before.

The positions taken in MIS, will be sqaured off on the same day by the client or till the exchange squared off.
        
        NRML - Pay a fraction of total order amount now and pay the remaining amount in 5 days to own the shares.
        
        MTF - Pay a fraction of total order amount now and pay the remaining at a later date at a fixed interest rate.
        '''
        self.validity = ['DAY', 'IOC', 'EOS', 'GTC', 'GTD']

        '''
        Validity:
       
        DAY - Order will be placed and valid throughout the market hours including the post closing session (9AM to 4PM).
       
        IOC - Order will be placed to exchange and executed if matching price and quantity is found at the time of order placement, if not executed, the order will be immediately cancelled.
       
        EOS - Order will be placed and valid throughout the market hours (9.15AM to 3.30PM). Order will not be valid for the post closing session.
       
        GTC - GTC order is active until the trade is executed or trader cancels the order.
       
        GTD - GTD orders remains active until a user specified date/7 days whichever is earlier or it has been filled or cancelled.
           
        '''

    def Instruments(self):
        '''

        :return: Download the Contract File and places the scrips in an Iterable format
        '''
        if self.dc:
            url = self.__config.ContractURL
            urllib.request.urlretrieve(url, 'instruments.zip')

        with zipfile.ZipFile('instruments.zip', 'r') as zip_ref:
            zip_ref.extractall('instruments')
        with open('instruments/instruments.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                self.instruments.append(row)

    def __CheckUpdate(self):

        url = self.__config.CheckUpdateURl()
        rep = self.__http.PostMethod(url, json.dumps({"lib": "EAC_PYTHON", "vsn": self.version}))
        if rep['data']['sts'] is True:
            if rep['data']['msg'] == 'MANDATORY':
                print("Mandatory Update. New version " + rep['data']['vsn'] + '. Update to new version to continue.')
                sys.exit(0)
            if rep['data']['msg'] == 'OPTIONAL':
                print("New version " + rep['data']['vsn'] + " is available. Stay up to date for better experience")

    def GetLoginData(self):
        """

        Get Login Info.

        """
        return self.__constants.get_Data()

    def GenerateVendorSession(self, ApiKey, Password) -> str:
        """

        Get Login Info.

        ApiKey : Key provided by Edelweiss

        Password : Password provided by Edelweiss

        """
        self.Login(ApiKey, Password)

    def GetAuthorization(self, reqId) -> str:
        """

        Get Login Info.

        reqId : Request ID generated during re-direction to a url

        """
        self.Token(reqId);

    def OrderBook(self):
        """

        This method will retrieve the equity Order Book. Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        """
        url = self.__config.OrderBookURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def TradeBook(self):

        """

          This method will retrieve the Trade Book. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

        """
        url = self.__config.TradeBookURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def NetPosition(self):
        """
        Net position usually is referred to in context of trades placed during the day in case of Equity, or can refer to carry forward positions in case of Derivatives, Currency and Commodity. It indicates the net obligation (either buy or sell) for the given day in a given symbol. Usually you monitor the net positions screen to track the profit or loss made from the given trades and will have options to square off your entire position and book the entire profit and loss.


       This method will retrieve the Net position. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

          """
        url = self.__config.NetPositionURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def OrderDetails(self, OrderId):
        """

          Please use this method to retrive the details of single order.
          Response Fields :
           - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

          """
        url = self.__config.OrderDetailsURL().format(userid=self.__constants.get_AccId(), orderid=OrderId)
        return self.__http.GetMethod(url)

    def OrderHistory(self, StartDate, EndDate):
        """

          This method will retrive all the historical orders placed from `StartDate` to `EndDate`

          StartDate : Start Date of Search

          EndDate : End Date of search

          """
        url = self.__config.OrderHistoryURL().format(userid=self.__constants.get_AccId(), StartDate=StartDate,
                                                     EndDate=EndDate)
        return self.__http.GetMethod(url)

    def Holdings(self):
        """
        Holdings comprises of the user's portfolio of long-term equity delivery stocks. An instrument in a holding's portfolio remains there indefinitely until its sold or is delisted or changed by the exchanges. Underneath it all, instruments in the holdings reside in the user's DEMAT account, as settled by exchanges and clearing institutions.


          """
        url = self.__config.HoldingURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def PlaceTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                   Streaming_Symbol,
                   Limit_Price,
                   Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):

        """
        Order placement refers to the function by which you as a user can place an order to respective exchanges. Order placement allows you to set various parameters like the symbol, action (buy, sell, stop loss buy, stop loss sell), product type, validity period and few other custom parameters and then finally place the order. Any order placed will first go through a risk validation in our internal systems and will then be sent to exchange. Usually any order successfully placed will have OrderID and ExchangeOrderID fields populated. If ExchangeOrderID is blank it usually means that the order has not been sent and accepted at respective exchange.

        Order placement method

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration,
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "N",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0"}

        url = self.__config.PlaceTradeURL().format(userid=self.__constants.get_AccId())
        reply = self.__http.PostMethod(url, json.dumps(data))
        return reply

    def PlaceCoverTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                        Streaming_Symbol,
                        Limit_Price,
                        Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):
        """

        A Cover Order is an order type for intraday trades. A Cover Order lets you to place trades with very high leverage of up to 20 times the available limits (Cash/Stocks collateral limits)

        Pay a fraction of total order amount (10% or Rs. 20) to own the shares. In case it falls below the following price, sell it off to prevent me losing money from sharp price drops.

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """
        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration,
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0", }

        url = self.__config.PlaceCoverTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(data))

    def PlaceGtcGtdTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity, Limit_Price,
                         Product_Code, DTDays):

        """
        Good Till Cancel (GTC) orders refers to orders where the validity period of the order is upto execution, cancellation by user or 90 days whichever comes first. This is a validity period used when you want to fire and forget an order and is usually an order placed with a limit price.
		Good Till Date (GTD) orders are similar to GTC orders, however here the validity period is set by the user (max validity period of 90 days), rest of the functionality is the same, this too is a limit order.

        GTC/GTD Order

        GTC order is active until the trade is executed or trader cancels the order.GTD orders remains active until a user specified date/7 days whichever is earlier or it has been filled or cancelled.

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : GTC/GTD

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        - `DTDays` : Date for GTD Orders in dd/MM/yyyy format

        """
        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'ordTyp': Order_Type,
                'qty': Quantity, 'lmPrc': Limit_Price, 'prdCode': Product_Code,
                'dtDays': DTDays, 'ordSrc': 'API', 'vnCode': '', 'oprtn': '<=', 'srcExp': '', 'tgtId': '',
                'brnchNm': '',
                'brk': '', }
        url = self.__config.PlaceGtcGtdTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(data))

    def ModifyTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                    Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                    ProductCode="CNC"):
        """
        Modify orders allows a user to change certain aspects of the order once it is placed. Depending on the execution state of the order (i.e. either completely open, partially open) there are various levels of modification allowed. As a user you can edit the product type, order quantity, order validity and certain other parameters. Please note that any modifications made to an order will be sent back to the risk system for validation before being submitted and there are chances that an already placed order may get rejected in case of a modification.

        Modify Order

        `Trading_Symbol` : Trading Symbol of the Scrip

        `Exchange` : Exchange

        `Action` : BUY/SELL

        `Duration` : DAY/IOC/EOS(for BSE)

        `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        `Quantity` : Quantity of the scrip

        `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        `Limit_Price` : Limit price of scrip

        `Disclosed_Quantity` : Quantity to be disclosed while order placement

        `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        `ProductCode` : CNC/MIS/NRML/MTF


        """
        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        url = self.__config.ModifyTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    def ModifyCoverTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                         Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                         ProductCode="CNC"):

        """

        Modify Cover Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        url = self.__config.ModifyCoverTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    def CancelTrade(self, OrderId):
        """
        An order can be cancelled, as long as on order is open or pending in the system

        Cancel Order

        OrderId : Nest OrderId

        """
        url = self.__config.CancelTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps({"nstOID": OrderId}))

    def MFOrderBook(self, fromDate, toDate):
        '''

        This method will retrieve the MF Order Book.
         fromDate: From Date
         toDate: To Date
         :return: MF Order Book

         Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        '''

        url = self.__config.OrderBookMFURL().format(userid=self.__constants.get_AccId(), fromDate=fromDate,
                                                    toDate=toDate)
        return self.__http.GetMethod(url)

    def ExitCoverTrade(self, OrderId):
        """
        This functionality allows you to completely exit a cover order which includes cancelling any unplaced orders and also completely squaring off any executed orders. For the orders which were executed it will usually modify the stop loss order leg and place it as a market order to ensure execution, while any non executed quantity order will get cancelled.

       Exit Cover Order

       OrderId : Nest OrderId

       """
        url = self.__config.ExitCoverTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps({"nstOID": OrderId}))

    def ExitBracketTrade(self, Order_Id, Syom_Id, Status):
        """
        Similar to Exit Cover order the functionality will ensure that any non executed open order will be cancelled. However for any orders which are executed it will automatically cancel one of the target or stop loss legs and modify the other leg to be placed as a market order. This will ensure that any executed orders will be squared off in position terms.

       Exit Bracket Order

       OrderId : Nest OrderId

       Syom_Id : Syom_Id obtained post placing Bracket Order

       Status: Current Status of the Bracket Order

       """
        data = {'nstOrdNo': Order_Id, 'syomID': Syom_Id, 'sts': Status}
        params = locals()
        del (params["self"])
        url = self.__config.ExitBracketTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.DeleteMethod(url, json.dumps(data))

    def PlaceBracketTrade(self, Exchange, Streaming_Symbol, Transaction_Type, Quantity, Duration, Disclosed_Quantity,
                          Limit_Price, Target, StopLoss, Trailing_Stop_Loss='Y', Trailing_Stop_Loss_Value="1"):

        """

        Bracket Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        Target : Absolute Target value

        StopLoss :Absolute Stop Loss value

        Trailing_Stop_Loss : Y/N

        Trailing_Stop_Loss_Value : Number

        """

        data = {'exc': Exchange, 'sym': Streaming_Symbol,
                'trnsTyp': Transaction_Type, 'qty': Quantity, 'dur': Duration, 'dsQty': Disclosed_Quantity,
                'prc': Limit_Price, 'trdBsdOn': "LTP", 'sqOffBsdOn': 'Absolute', 'sqOffVal': Target,
                'slBsdOn': 'Absolute', 'slVal': StopLoss, 'trlSl': Trailing_Stop_Loss,
                'trlSlVal': Trailing_Stop_Loss_Value, 'ordSrc': 'API'}

        url = self.__config.PlaceBracketTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(data))

    def PlaceBasketTrade(self, orderlist):
        """

        Basket order allows user to place multiple orders at one time. User can place orders for multiple scrips all at once. One just creates multiple orders for same or different securities and club these orders together to be placed in one go. This helps save time.

        orderlist : List of Order to be placed, Refer: Order Class

        """
        lst = []
        for x in orderlist:
            data = {'trdSym': x.trdSym, 'exc': x.exc, 'action': x.action, 'dur': x.dur,
                    'ordTyp': x.ordTyp, 'qty': x.qty, 'dscQty': x.dscQty,
                    'price': x.price, 'trgPrc': x.trgPrc, 'prdCode': x.prdCode, 'vnCode': '',
                    'rmk': ''}
            lst.append(data)

        fd = {
            "ordLst": lst,
            "ordSrc": "API"
        }

        url = self.__config.PlaceBasketTradeURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(fd))

    def Limits(self):
        """
        Limits refers to the cumulative margins available in your account which can be used for trading and investing in various products. Limits is a combination of the free cash you have (i.e. un-utilized cash), cash equivalent securities (usually margin pledged securities), any money which is in transit (T1/T2 day sell transaction values) and others, all of which can be used for placing orders. Usually whenever you place an order in a given asset and product type our risk management system assesses your limits available and then lets the orders go through or blocks the orders. Limits are dynamic in nature and can be influenced by the Mark to Markets in your positions and sometimes even by the LTP of your holdings.

        Get limits


        """
        url = self.__config.LimitsURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def GetAMOStatus(self):
        """

        Get AMO status

        """
        url = self.__config.GetAMOFlag().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    def PlaceAMOTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                      Streaming_Symbol, Limit_Price, Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):

        """
        After market order or AMO in short refers to orders which can be placed once the markets or exchanges are closed for trading. You can place AMO post market hours which will result in the order in question being placed automatically by 9:15 AM - 9:30 AM the next business day. AMO orders usually need to be limit orders in order to prevent inadvertent execution in case of adverse price movement in markets at beginning of day. AMO is a useful way to place your orders in case you do not have time to place orders during market hours.

        After Market Order trade

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}

        url = self.__config.PlaceAMOTrade().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(data))

    def ModifyAMOTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                       Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                       ProductCode="CNC"):

        """

        Modify After Market Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}

        url = self.__config.ModifyAMOTrade().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    def CancelAMOTrade(self, OrderId):
        """

        Cancel After Market Order

        OrderId : Nest Order Id

        """
        url = self.__config.CancelAMOTrade().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps({"nstOID": OrderId}))

    def PositionSquareOff(self, orderlist):
        """

        Square off is a term used in intraday and simply means closing all open positions by the end of the trading day

        orderList : List of orders to be Squared Off. Refer : Orders class.

        """
        lst = []
        for x in orderlist:
            data = {'trdSym': x.trdSym, 'exc': x.exc, 'action': x.action, 'dur': x.dur, 'flQty': "0",
                    'ordTyp': x.ordTyp, 'qty': x.qty, 'dscQty': x.dscQty, 'sym': x.sym,
                    'mktPro': "",
                    'lmPrc': x.price, 'trgPrc': x.trgPrc, 'prdCode': x.prdCode, 'dtDays': '', 'posSqr': "true",
                    'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}
            lst.append(data)
        url = self.__config.PositionSqOffURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(lst))

    def ConvertPosition(self, Order_Id, Fill_Id, New_Product_Code, Old_Product_Code):
        """

        Convert Position : converts your holding position from MIS to CNC and vice-versa

        Order_Id : Nest Order id

        Fill_Id : Fill Id of the trade obtained from Trade API

        New_Product_Code: New Product code of the trade

        Old_Product_Code : Existing Product Code of the trade

        """
        data = {'nstOID': Order_Id, 'flID': Fill_Id, 'prdCodeCh': New_Product_Code, 'prdCode': Old_Product_Code}

        url = self.__config.ConvertPositionURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    # MF Methods

    def PlaceMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                ReInv_Flag, Folio_Number,
                Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                Generate_First_Order_Today, Scheme_Plan, Scheme_Code):

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''

        data = {'currentOrdSts': '', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': 'Z', 'folioNo': Folio_Number,
                'ordTyp': 'FRESH', 'txnId': '0', 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': '',
                'closeAccountFlag': '',
                'kycflag': '', 'euinflag': '', 'physicalFlag': ''}

        url = self.__config.PlaceMFURL().format(userid=self.__constants.get_AccId())
        return self.__http.PostMethod(url, json.dumps(data))

    def ModifyMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                 ReInv_Flag, Folio_Number,
                 Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                 Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id):

        '''

        certain attributes of a MF order may be modified., as long as on order is open or pending in the system

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''

        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': 'Z', 'folioNo': Folio_Number,
                'ordTyp': 'MODIFY', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': '',
                'closeAccountFlag': '',
                'kycflag': '', 'euinflag': '', 'physicalFlag': ''}

        url = self.__config.ModifyMFURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    def CancelMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                 ReInv_Flag, Folio_Number,
                 Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                 Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id):

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:

        '''

        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': 'Z', 'folioNo': Folio_Number,
                'ordTyp': 'CANCEL', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': '',
                'closeAccountFlag': '',
                'kycflag': '', 'euinflag': '', 'physicalFlag': ''}

        url = self.__config.CancelMFURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, json.dumps(data))

    def HoldingsMF(self):
        '''

         Mutual Fund Holdings

        '''
        params = locals()
        del (params["self"])
        url = self.__config.HoldingsMFURL().format(userid=self.__constants.get_AccId())
        return self.__http.GetMethod(url)

    # MF methods

    def Login(self, source, password):
        params = locals()
        del (params["self"])
        url = self.__config.LoginURL().format(vendorId=source)
        rep = self.__http.PostMethod(url, json.dumps({"pwd": password}), )
        if rep != "":
            vt = rep['msg']
            self.__constants.set_VendorSession(vt)
        else:
            sys.exit()

    def Token(self, reqId):
        params = locals()
        del (params["self"])
        url = self.__config.TokenURL()
        rep = self.__http.PostMethod(url, json.dumps({"reqId": reqId}), False)

        if rep != "":
            self.__constants.set_Data(rep)
            self.__constants.set_AccId(rep['data']['lgnData']['accs']['eqAccID'])
            self.__constants.set_JSession(rep['data']['auth'])

            prop = json.dumps({'vt': self.__constants.get_VendorSession(),
                               'auth': self.__constants.get_JSession(),
                               'accid': self.__constants.get_AccId(),
                               'data': self.__constants.get_Data(),
                               'appidkey': self.__constants.get_AppIdKey()})
            writetofile = open("readme.txt", 'w').write(prop)
        else:
            sys.exit()

    def Logout(self):
        params = locals()
        del (params["self"])
        url = self.__config.LogoutURL().format(userid=self.__constants.get_AccId())
        return self.__http.PutMethod(url, {})

    class __Constants:

        def __init__(self):
            self.__VendorSession = ""
            self.__ApiKey = ""
            self.__AccId = ""
            self.__JSessionId = ""
            self.__AppIdKey = ""
            self.__Data = ""

        def set_VendorSession(self, val):
            self.__VendorSession = val

        def get_VendorSession(self):
            return self.__VendorSession

        def set_ApiKey(self, val):
            self.__ApiKey = val

        def get_ApiKey(self):
            return self.__ApiKey

        def set_AccId(self, val):
            self.__AccId = val

        def get_AccId(self):
            return self.__AccId

        def set_JSession(self, val):
            self.__JSessionId = val

        def get_JSession(self):
            return self.__JSessionId

        def set_AppIdKey(self, val):
            self.__AppIdKey = val

        def get_AppIdKey(self):
            return self.__AppIdKey

        def set_Data(self, val):
            self.__Data = val

        def get_Data(self):
            return self.__Data

    class __Config:

        def __init__(self):
            self.baseurleq = "https://client.edelweiss.in/edelmw-eq/eq/"
            self.baseurlcontent = "https://client.edelweiss.in/edelmw-content/content/"
            self.baseurllogin = "https://client.edelweiss.in/edelmw-login/login/"
            self.basemflogin = "http://client.edelweiss.in/edelmw-mf/mf/"
            self.websocketURL = "wss://mstream.edelweiss.in:8443/"
            self.ContractURL = "https://client.edelweiss.in/app/toccontracts/instruments.zip"

            # self.baseurleq = "https://emtuat.edelweiss.in/edelmw-eq-uat/eq/"
            # self.baseurlcontent = "https://emtuat.edelweiss.in/edelmw-content-uat/content/"
            # self.baseurllogin = "https://emtuat.edelweiss.in/edelmw-login-uat/login/"
            # self.basemflogin = "http://emtuat.edelweiss.in/edelmw-mf-uat/mf/"
            # self.websocketURL = "wss://mstreamuat.edelweiss.in:12007/"
            # self.ContractURL = "http://emtuat.edelweiss.in/app/toccontracts/instruments.zip"

        def CheckUpdateURl(self):
            return self.baseurlcontent + "adhoc/lib/version"

        def OrderBookURL(self):
            return self.baseurleq + "order/book/{userid}/v1"

        def TradeBookURL(self):
            return self.baseurleq + "tradebook/v1/{userid}"

        def NetPositionURL(self):
            return self.baseurleq + "positions/net/{userid}"

        def PlaceTradeURL(self):
            return self.baseurleq + "trade/placetrade/{userid}"

        def PlaceBracketTradeURL(self):
            return self.baseurleq + "trade/placebrackettrade/{userid}"

        def PlaceCoverTradeURL(self):
            return self.baseurleq + "trade/covertrade/{userid}"

        def ModifyCoverTradeURL(self):
            return self.baseurleq + "trade/modifycovertrade/{userid}"

        def ExitCoverTradeURL(self):
            return self.baseurleq + "trade/exitcovertrade/{userid}"

        def PlaceBasketTradeURL(self):
            return self.baseurleq + "trade/basketorder/{userid}"

        def ExitBracketTradeURL(self):
            return self.baseurleq + "trade/exitbrackettrade/{userid}"

        def PlaceGtcGtdTradeURL(self):
            return self.baseurleq + "trade/placegtcgtdtrade/{userid}"

        def OrderDetailsURL(self):
            return self.baseurleq + "order/details/{userid}?nOID={orderid}"

        def OrderHistoryURL(self):
            return self.baseurleq + "order/history/{userid}?sDt={StartDate}&eDt={EndDate}"

        def ModifyTradeURL(self):
            return self.baseurleq + "trade/modifytrade/{userid}"

        def CancelTradeURL(self):
            return self.baseurleq + "trade/canceltrade/{userid}"

        def HoldingURL(self):
            return self.baseurleq + "holdings/v1/rmsholdings/{userid}"

        def LimitsURL(self):
            return self.baseurleq + "limits/rmssublimits/{userid}"

        def GetAMOFlag(self):
            return self.baseurleq + "trade/amoflag"

        def PositionSqOffURL(self):
            return self.baseurleq + "trade/position/sqroff/{userid}"

        def ConvertPositionURL(self):
            return self.baseurleq + "trade/convertposition/{userid}"

        def PlaceAMOTrade(self):
            return self.baseurleq + "trade/amo/placetrade/{userid}"

        def ModifyAMOTrade(self):
            return self.baseurleq + "trade/amo/modifytrade/{userid}"

        def CancelAMOTrade(self):
            return self.baseurleq + "trade/amo/canceltrade/{userid}"

        # MF Related APIs

        def PlaceMFURL(self):
            return self.basemflogin + "trade/{userid}"

        def ModifyMFURL(self):
            return self.basemflogin + "trade/{userid}"

        def CancelMFURL(self):
            return self.basemflogin + "trade/{userid}"

        def HoldingsMFURL(self):
            return self.basemflogin + "holding/{userid}"

        def OrderBookMFURL(self):
            return self.basemflogin + "order/{userid}?frDt={fromDate}&toDt={toDate}"

        # Login related APIs

        def LoginURL(self):
            return self.baseurllogin + "accounts/loginvendor/{vendorId}"

        def TokenURL(self):
            return self.baseurllogin + "accounts/logindata"

        def LogoutURL(self):
            return self.baseurllogin + "accounts/logoutvendor/{vendorId}"

    class __Http:

        def __init__(self, constants):
            self.__constants = constants

        def GetMethod(self, url, sendSource=True):

            if sendSource:
                response = requests.get(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "Source": self.__constants.get_ApiKey(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey()
                })
            else:
                response = requests.get(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey()
                })
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:

                if "data" in json.loads(response.content):
                    return json.loads(response.content)['data']
                else:
                    return 'Please enter new Session code and try again'
                    sys.exit()
            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists("readme.txt"):
                        os.remove("readme.txt")
                        sys.exit()
                print(response.content)
                return ""

        def PostMethod(self, url, data, sendSource=True):
            if sendSource:
                response = requests.post(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "Source": self.__constants.get_ApiKey(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey(),
                    "Content-type": "application/json"}, data=data)


            else:
                response = requests.post(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey(),
                    "Content-type": "application/json"}, data=data)

            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)

            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists("readme.txt"):
                        os.remove("readme.txt")
                print(response.content)
                return ""

        def PutMethod(self, url, data: json):
            response = requests.put(url, headers={"Authorization": self.__constants.get_JSession(),
                                                  "Source": self.__constants.get_ApiKey(),
                                                  "SourceToken": self.__constants.get_VendorSession(),
                                                  "Content-type": "application/json"}, data=data)
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)
            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists("readme.txt"):
                        os.remove("readme.txt")
                print(response.content)
                return ""

        def DeleteMethod(self, url, data: json):
            response = requests.delete(url, headers={"Authorization": self.__constants.get_JSession(),
                                                     "Source": self.__constants.get_ApiKey(),
                                                     "SourceToken": self.__constants.get_VendorSession(),
                                                     "Content-type": "application/json"}, data=data)
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)
            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists("readme.txt"):
                        os.remove("readme.txt")
                print(response.content)
                return ""


class Feed:

    def __init__(self, symbols, accid, userid, callBack, subscribe_order: bool = True, subscribe_quote: bool = True):

        '''
        Streamer

        To subscribe to the streamer, Create the single instance of this mentioning `callback` method. After successsful subscription, `callback` method will be called whenever packet is available at the streamer.

         - symbols: Symbol list for subscription : Symbol_exchange to be obtained from Contract File

         - accid: Customer Account ID

         - messageCallback: Callback to receive the Feed in

         - subscribe_order

         - subscribe_quote

        '''
        self.cb = callBack
        self.userid = userid
        self.accid = accid
        self.symbols = symbols
        self.__appID = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjE2Mzk3NDQxLCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjAiLCJhcHBpZCI6IjE2OTExYTA1ZDU4ZTI5YjVmNTMyZTE3MzRkYzQyMjI2IiwiaXNzIjoiZW10IiwiZXhwIjoxNjE2NDM3ODAwLCJpYXQiOjE2MTYzOTc3NDF9.X2L9kMZjK2yzK5wLiOk2gnF73j5q4WnQtAq26W9XFM4"

        # New code TCP
        sock = socket.create_connection(["mstreamuat.edelweiss.in", 12009], 10000)
        # sock = socket.create_connection(["mstream.edelweiss.in", 8443], 10000)

        # Send data
        if subscribe_quote:
            quote = self.__CreateMessage_quote(symbols)
            sock.sendall(bytes(quote, 'UTF-8'))

        if subscribe_order:
            orderfiler = self.__CreateMessage_OrderFiler()
            sock.sendall(bytes(orderfiler, "UTF-8"))

        while True:
            resp = sock.recv(2048).decode()
            self.cb(resp)

    def __CreateMessage_quote(self, symbols):

        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})

        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "M",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe"
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def __CreateMessage_OrderFiler(self):

        req = {
            "request":
                {
                    "streaming_type": "orderFiler",
                    "data":
                        {
                            "accType": "EQ",
                            "userID": self.userid,
                            "accID": self.accid,
                            "responseType": ["ORDER_UPDATE", "TRADE_UPDATE"]
                        },
                    "formFactor": "M",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe",
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def unsubscribe(self, symbols):
        '''

         This method will unsubscribe the symbols from the streamer. After successful invokation of this, will stop the streamer packets of these symbols.

         symbols: `streaming symbol` for the scrips which need to be unsubscribed

         void
        '''
        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})
        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "M",
                    "appID": self.appID,
                    "response_format": "json",
                    "request_type": "unsubscribe"
                },
            "echo": {}
        }
        self.ws.send(json.dumps(req) + "\n")


class Order:

    def __init__(self, Exchange, TradingSymbol, StreamingSymbol, Action, ProductCode,
                 OrderType, Duration, Price, TriggerPrice, Quantity, DisclosedQuantity,
                 GTDDate, Remark):
        '''

         Exchange: Exchange of the scrip

         TradingSymbol: Trading Symbol, to be obtained from Contract Notes

         StreamingSymbol: ScripCode_exchange

         Action: BUY/SELL

         ProductCode: CNC/MIS/NRML

         OrderType: LIMIT/MARKET

         Duration: Validity DAY/IOC

         Price: Limit price of the scrip

         TriggerPrice: Trigger Price in case of SL/SL-M Order

         Quantity: Quantity of scrip to be purchased

         DisclosedQuantity: Disclosed Quantiy for the Order

         GTDDate: Good Till Date in dd/MM/yyyy format

         Remark: remark

        '''
        self.exc = Exchange
        self.trdSym = TradingSymbol
        self.sym = StreamingSymbol
        self.action = Action
        self.prdCode = ProductCode
        self.ordTyp = OrderType
        self.dur = Duration
        self.price = Price
        self.trgPrc = TriggerPrice
        self.qty = Quantity
        self.dscQty = DisclosedQuantity
        self.GTDDate = GTDDate
        self.rmk = Remark
