# This file is part of the mt5se package
#  mt5se home: https://github.com/paulo-al-castro/mt5se
# Author: Paulo Al Castro
# Date: 2020-11-17


# mt5se main module
import MetaTrader5 as mt5
import pandas as pd 
import numpy as np 

import random
from math import *
from datetime import datetime
from datetime import timedelta
# importamos o módulo pytz para trabalhar com o fuso horário
import pytz
from pytz import timezone



#sptz=pytz.timezone('Brazil/East')
etctz=pytz.timezone('etc/utc') # os tempos sao armazenados na timezone ETC (Greenwich sem horario de verao)

path=None # Metatrader program file path
datapath=None # Metatrader path to data folder
commonDatapath=None # Metatrader common data path
company=None  #broker name
platform=None  # digital plataform (M)
connected=False

"""
   login,                    // número da conta  (TODO)
   password="PASSWORD",      // senha
   server="SERVER",          // nome do servidor como definido no terminal
   timeout=TIMEOUT           // tempo de espera esgotado
"""
def connect(account=None,passw=None,mt5path=None):
	#if not se.connect():
	#print(“Error on connection”, se.last_error())
	#exit():
    if account==None and passw==None:
        if mt5path==None:
            res= mt5.initialize()
        else:
            res= mt5.initialize(mt5path)
    else:
        account=int(account)
        if mt5path==None:
            res= mt5.initialize(login=account, password=passw)
        else:
            res= mt5.initialize(mt5path,login=account, password=passw)
    global ac,path,datapath,commonDatapath,company,platform,connected
    if res!=True:
        if account==None:
            print('Error trying to connect to last account!!', ' Error code:',mt5.last_error())
        else:
            print('Error trying to connect to account: ',account, ' Error code:',mt5.last_error())
        return False
    info=mt5.account_info()
    if info.margin_so_mode !=mt5.ACCOUNT_MARGIN_MODE_RETAIL_NETTING:
        print("It is NOT netting, but the stock exchange should be netting trade mode!! Error!!")  # B3 is also Netting!!
        return False
    #elif info.margin_so_mode ==mt5.ACCOUNT_MARGIN_MODE_RETAIL_HEDGING:
    #    print("It is hedding, not netting")
    #else:
    #    print("It is something elese!!")
    #if info.margin_so_mode ==mt5.ACCOUNT_MARGIN_MODE_RETAIL_NETTING:
    #    print("It is netting, not hedding")  # se is Netting!!
    #elif info.margin_so_mode ==mt5.ACCOUNT_MARGIN_MODE_RETAIL_HEDGING:
    #    print("It is hedding, not netting")
    #else:
    #    print("It is something elese!!")
    if res:
        ac=mt5.terminal_info()
        path=ac.path
        datapath=ac.data_path
        commonDatapath=ac.commondata_path
        company=ac.company
        platform=ac.name
        connected=True
    return res

def terminalInfo():
    if not connected:
        print("In order to use this function, you must be connected to the . Use function connect()")
        return
    term_info = mt5.terminal_info()
    return term_info

def accountInfo():
#acc=se.accountInfo()    # it returns a dictionary
#acc['login']   # Account id
#acc['balance'] # Account balance in the deposit currency
# acc['equity'] # Account equity in the deposit currency
#acc['margin']  #Account margin used in the deposit currency
#acc['margin_free'] # Free margin of an account in the deposit currency
#acc['assets'] # The current assets of an account
# acc['name'] #Client name
#  acc['server'] # Trade server name
#  acc['currency'] # Account currency, BRL for Brazilian Real 
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    account_info = mt5.account_info()
    #print("account info")
    return account_info
"""
    returns the current number of assets of the given symbol
"""
def get_shares(symbolId):
   if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
   pos= mt5.positions_get(symbol=symbolId)
   if pos!=None and pos!=():
      d=pos[0]._asdict() 
      return d['volume']
   else:
       return 0

   return pos['volume']


"""
  It returns if the market is open or not for new orders.
     Note that markets can close in different times for different assets, therefore
     you need to inform the target asset. The default target assets is B3 stock (it will work only in B3 stock exchange)
     For other exchanges inform a valid asset ticker (For instance, GOOG should work for Nasdaq).
     It there is no tick for 60 seconds, the market is considered closed!
"""
def isMarketOpen(asset='B3SA3'):
  if not connected:
    print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
    return
   # si=mt5.symbol_info(asset)
   # if si!=None:
  #      if si.trade_mode==mt5.SYMBOL_TRADE_MODE_FULL: # it does not work in XP/B3 (always True)
  #          return True
  #      else:
  #          return False
  #  return False
  mt5.symbol_select(asset) # it makes sure that the symbol is present in Market Watch View
  t_secs=mt5.symbol_info_tick(asset).time # time in seconds
  now_dt=datetime.now(etctz)+timedelta(hours=-3)
  last_tick_dt=datetime.fromtimestamp(t_secs,etctz)
  #print(last_tick_dt)
  #print(now_dt)
  if now_dt>last_tick_dt+timedelta(seconds=60):
      return False
  else: 
      return True


"""
It returns the today datetime (hours=minutes=seconds=0)
 You can define an offset in days.
    today(1) returns tomorrow
    today(-1) returns yesterday
"""
def today(offset=None):
    dt=datetime.now()
    dt=datetime(dt.year,dt.month,dt.day,0,0,0)
    if offset==None:
        return dt
    if type(offset)!=int:
        print('Offset should a int with the number of dates. Returning today date without offset')
        return dt
    else:
        dt=dt+timedelta(days=offset)
        return dt

"""
It returns the today datetime (hours=minutes=seconds=0)
 You can define an offset in days.
    today(1) returns tomorrow
    today(-1) returns yesterday
"""
def now(hourOffset=None,minOffset=None):
    dt=datetime.now()
    if hours!=None:
        dt=dt+timedelta(hours=hourOffset)
    if minOffset!=None:
        dt=dt+timedelta(minutes=minOffset) 
    return dt

"""
  It returns if the market is still open but just for closing orders.
     Note that markets can close in different times for different assets, therefore
     you need to inform the target asset. The default target assets is B3 stock
"""
#def isMarketClosing(asset='B3SA3'): # it does not work in XP/B3 (always false)
#    si=mt5.symbol_info(asset)
#    if si!=None:
 #       if si.trade_mode==mt5.SYMBOL_TRADE_MODE_CLOSEONLY:
  #          return True
  #      else:
  #          return False
  #  return False


def getFreeMargin():
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    return mt5.account_info().margin_free


"""
  Returns the volume step for an asset
"""
def getVolumeStep(assetId):
    step=mt5.symbol_info(assetId).volume_step
    return step
    
"""
    returns the max volume of shares thay you can buy, with your balance
        it also observes the volume step (a.k.a minimum number of shares you can trade)
"""
def getAfforShares(assetId,money=None,price=None,volumeStep=None):
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if money==None:
        money=mt5.account_info().balance
    if money <=0:
        return 0.0
        
    if price==None:
        close=mt5.symbol_info_tick(assetId).last
    else:
        close=price
    if volumeStep==None:
        step=mt5.symbol_info(assetId).volume_step
    else:
        step=volumeStep    


    free=np.floor(money/(step*close))
    while free*close<money:
        free=free+step
    return free-step

def get_sharesStep(assetId,money=None): # todo: duplicada com getVolumeStep
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    return mt5.symbol_info(assetId).volume_step
 
# Saldo da conta em BRL
def get_balance():
    return mt5.account_info().balance

def get_shares(symbolId):
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    pos=get_position(symbolId)
    if len(pos)==0:
        return 0
    return pos['volume']

# Valor da posição total, saldo em reais mais valores correntes dos ativos 
def get_total_position(symbolId=None):
    pos=getPosition(symbolId)
    if len(pos)>0:
        return sum(pos['volume']*pos['price_current'])
    else:
        return 0.0
#se.getPosition( symbol_id) # return the current position in a given asset (symbol_id)
#Examples:
#se.getPosition('PETR4')
#pos=se.getPosition('ITUse')
#pos['volume'] # position volume
#pos['open'] # position open price
#pos['time'] #position open time
#pos['symbol'] # position symbol id
#pos['price']  #current price of the asset
# se.getPosition(group='PETR*') # returns a list of positions that are part of the group
  #print("get position")

def get_position(symbolId=None):  # return the current value of assets (it does not include balance or margin)
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if symbolId==None:
        positions=mt5.positions_get()
    else:
        positions=mt5.positions_get(symbol=symbolId)
    if len(positions)>0:
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        df=df[['symbol','profit','volume', 'price_open', 'price_current']]
        return df
    else:
        return pd.DataFrame()



def buyOrder(symbolId,volume,price=None,sl=None,tp=None): # Buying !!
#b=se.buy(symbol_id,volume, price, sl, tp ))
#if se.checkorder(b):
#    if se.send(b): #buying
#	print('order sent to the Stock Exchange')
#    else:
#	print('Error : ',se.getLastError())
#else:
#    print('Error : ',se.getLastError())
   if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
   symbol_info = mt5.symbol_info(symbolId)
   #print("symbol=",symbolId," info=",symbol_info)
   if symbol_info is None:
        setLastError(symbolId + " not found, can not create buy order")
        return None
 
# se o símbolo não estiver disponível no MarketWatch, adicionamo-lo
   if not symbol_info.visible:
        #print(symbolId, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbolId,True):
            setLastError("symbol_select({}}) failed! symbol=" +symbolId)
            return None   
   point = mt5.symbol_info(symbolId).point
   deviation = 20
   
   request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbolId,
    "volume": float(volume),
    "type": mt5.ORDER_TYPE_BUY,

    "deviation": deviation,
    "magic": random.randrange(100,100000),
    "comment": "order by mt5se",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
    }
   if price==None:  # order a mercado
       request['action']=mt5.TRADE_ACTION_DEAL
       request['type']=mt5.ORDER_TYPE_BUY
       request['price']=mt5.symbol_info_tick(symbolId).ask
   else:  # order limitada
       request['action']=mt5.TRADE_ACTION_PENDING
       request['type']=mt5.ORDER_TYPE_BUY_LIMIT
       request['price']=float(price)
   if sl!=None:
       request["sl"]=sl
   if tp!=None:
        request["tp"]= tp
  

   return request

def sellOrder(symbolId,volume,price=None,sl=None,tp=None): # Selling !!
    symbol_info = mt5.symbol_info(symbolId)
    #print("symbol=",symbolId," info=",symbol_info)
    if symbol_info is None:
        setLastError(symbolId + " not found, can not create buy order")
        return None
# se o símbolo não estiver disponível no MarketWatch, adicionamo-lo
    if not symbol_info.visible:
        #print(symbolId, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbolId,True):
            setLastError("symbol_select({}}) failed! symbol=" +symbolId)
            return None   
    point = mt5.symbol_info(symbolId).point
    deviation = 20
    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbolId,
    "volume": float(volume),
    "type": mt5.ORDER_TYPE_SELL,
    
    "deviation": deviation,
    "magic": random.randrange(100,100000),
    "comment": "order by mt5se",
    "type_time": mt5.ORDER_TIME_DAY,
    "type_filling": mt5.ORDER_FILLING_FOK,
    }

    if price==None:  # order a mercado
       request['action']=mt5.TRADE_ACTION_DEAL
       request['type']=mt5.ORDER_TYPE_SELL
       request['price']=mt5.symbol_info_tick(symbolId).ask
    else:  # order limitada
       request['action']=mt5.TRADE_ACTION_PENDING
       request['type']=mt5.ORDER_TYPE_SELL_LIMIT
       request['price']=float(price)

    if sl!=None:
       request["sl"]=sl
   
    if tp!=None:
        request["tp"]= tp
    
    return request


def isSellOrder(req):
    if req==None:
        print("Error! Order is None!!!!")
        return False
    if req['type']==mt5.ORDER_TYPE_SELL_LIMIT or req['type']==mt5.ORDER_TYPE_SELL:
        return True
    elif req['type']==mt5.ORDER_TYPE_BUY_LIMIT or req['type']==mt5.ORDER_TYPE_BUY:
        return False
    else:
        print("Error! Order is not buy our sell!!!!")
        return False
    

def checkOrder(req):
    if req==None:
        return False
    result = mt5.order_check(req)
    #print('result=',result, 'req=',req)
    if result==None: # error
        setLastError(mt5.last_error())
        return False
    d=result._asdict()
    #for k in d.keys():
    #    print('{} = {}',k,d[k])
    if d['margin_free']>=d['request'].volume*d['request'].price : # checa se não ficaria negativo com a execução
        return True
    else:
        setLastError('Trade would make the balance negative! Therefore, it does not check!')
        return False

lastErrorText=""
def getLastError():
    global lastErrorText
    if lastErrorText==None or lastErrorText=="":
        return mt5.last_error()
    else:
        aux=lastErrorText
        lastErrorText=None  
        return aux    
    
def setLastError(error):
    global lastErrorText
    lastErrorText=error


def sendOrder(order):
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if order==None:
        return False
    # enviamos a solicitação de negociação
    result = mt5.order_send(order)
    if result.retcode != mt5.TRADE_RETCODE_DONE:  # if error
        print("Sent order failed < {} > retcode={}".format(result.comment,result.retcode))
        # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
        dic=result._asdict()
        setLastError(dic['comment'])
       # for field in dic.keys():
       #     print("   {}={}".format(field,dic[field]))
       #     #se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
       #     if field=="request":
       #         traderequest_dict=dic[field]._asdict()
       #         for tradereq_filed in traderequest_dict:
       #             print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        return False
    else:
        return True

    
def cancelOrder(o):# TO DO
   # action= TRADE_ACTION_REMOVE
    print("To do....")

def numOrders(): #returns the number of active orders
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    result=mt5.orders_total()
    if result==None:
        setLastError("Error on getting orders total")
        return -1
    else:
        return result

#order fields  description:
    #order_id | buy_sell | volume | price | sl | tp | 
    #ticket | time_setup  time_setup_msc  time_expiration  type  type_time  type_filling  state  magic  
    # volume_current  price_open   sl   tp  price_current  symbol comment external_id
    #   ulong                         magic;            // Expert Advisor -conselheiro- ID (número mágico)
   #  ulong                         order;            // Bilhetagem da ordem
   #string                        symbol;           // Símbolo de negociação
  # double                        volume;           // Volume solicitado para uma encomenda em lotes
  # double                        price;            // Preço
  # double                        stoplimit;        // Nível StopLimit da ordem
  # double                        sl;               // Nível Stop Loss da ordem
  # double                        tp;               // Nível Take Profit da ordem
  # ulong                         deviation;        // Máximo desvio possível a partir do preço requisitado
 #  ENUM_ORDER_TYPE               type;             // Tipo de ordem
    #  ORDER_TYPE_BUY  Ordem de Comprar a Mercado
    #  ORDER_TYPE_SELL Ordem de Vender a Mercado
    #  ORDER_TYPE_BUY_LIMIT Ordem pendente Buy Limit
    #  ORDER_TYPE_SELL_LIMIT Ordem pendente Sell Limit
    #  ORDER_TYPE_BUY_STOP Ordem pendente Buy Stop
    #  ORDER_TYPE_SELL_STOP Ordem pendente Sell Stop
    #  ORDER_TYPE_BUY_STOP_LIMIT Ao alcançar o preço da ordem, uma ordem pendente Buy Limit é colocada no preço StopLimit
    #  ORDER_TYPE_SELL_STOP_LIMIT Ao alcançar o preço da ordem, uma ordem pendente Sell Limit é colocada no preço StopLimit
    #  ORDER_TYPE_CLOSE_BY  Ordem de fechamento da posição oposta
  # ENUM_ORDER_TYPE_FILLING       type_filling;     // Tipo de execução da ordem
    #ORDER_FILLING_FOK  Esta política de preenchimento significa que uma ordem pode ser preenchida somente na quantidade especificada. Se a quantidade desejada do ativo não está disponível no mercado, a ordem não será executada. 
  #  ENUM_ORDER_TYPE_TIME          type_time;        // Tipo de expiração da ordem
    # ORDER_TIME_DAY     Ordem válida até o final do dia corrente de negociação
  # datetime                      expiration;       // Hora de expiração da ordem (para ordens do tipo ORDER_TIME_SPECIFIED))
  # string                        comment;          // Comentário sobre a ordem
  # ulong                         position;         // Bilhete da posição
  # ulong                         position_by;      // Bilhete para uma posição oposta

def getOrders():  # returns a dataframe with all active orders
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    orders=mt5.orders_get()
    if orders == None or len(orders)==0:
        print("No orders, error code={}".format(mt5.last_error()))
        return None
    else:
        print("Total orders:",len(orders))
        df=pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())
        return df
      


def getDailYBars(symbol, start,end=None): # sao inclusas barras com  tempo de abertura <= end.
    # definimos o fuso horário como UTC
    #timezone = pytz.timezone("Etc/UTC")
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if end==None:
        end=datetime.now()
    if type(start).__name__!='datetime':
        if type(start).__name__!='int':
            print('Error, start should be a datetime from package datetime or int')
        else:
            start_day=datetime.now() #- timedelta(days=start)
            rates=mt5.copy_rates_from(symbol,mt5.TIMEFRAME_D1,start_day,start)
             # criamos a partir dos dados obtidos DataFrame
            rates_frame=pd.DataFrame(rates)
            rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
            return rates_frame
    else:
       rates=mt5.copy_rates_range(symbol,mt5.TIMEFRAME_D1,start,end)
       # criamos a partir dos dados obtidos DataFrame
       rates_frame=pd.DataFrame(rates)
       rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
       return rates_frame
DAILY=1 # daily bars
INTRADAY=2 # 1 minute bars
H1=3 # 1 hour bars

"""
  returns open-close serie of returns from bars
   the same order from bars (older-[0] to newer-[len-1])
"""
def getReturns(bars,offset=1):
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    x=[]
    offset=abs(offset)
    if offset==1:
        for i in range(len(bars)):
            x.append(bars['close'][i]/bars['open'][i]-1)
    else:
        for i in range(len(bars)-offset):
            x.append(bars['close'][i+offset]/bars['open'][i]-1)

    return x

def getLastPrice(bars): # argumento deve ser bars nao vazia, retorna erro se estiver vazia
    return bars['close'].iloc[-1]

def getFirstPrice(bars):# argumento deve ser bars nao vazia, retorna erro se estiver vazia
    return bars['open'][0]

def getMaxPrice(bars):# argumento deve ser bars nao vazia, retorna erro se estiver vazia
    return max(bars['high'])


def getMinPrice(bars):# argumento deve ser bars nao vazia, retorna erro se estiver vazia
    return max(bars['low'])

def getLastTime(bars): # argumento deve ser bars nao vazia, retorna erro se estiver vazia
    return bars['time'].iloc[-1]

def getFirstTime(bars):# argumento deve ser bars nao vazia, retorna erro se estiver vazia
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    return bars['time'][0]

def readBarsFile(fileName):
    df=pd.read_csv(fileName,delimiter='\t',names=['date','time','open','high','low','close','vol', 'tickvol','spread'],header=0) 
    if df==None or len(df.columns)!=9:
        print("The bars file should be a csv file with nine columns: date,time,open,high,low,close,vol, tickvol,spread")
        return None
    else:
        return df

def getBars(symbol, start,end=None,timeFrame=DAILY):
 # definimos o fuso horário como UTC
    #timezone = pytz.timezone("Etc/UTC")
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if symbol==None or type(symbol)!=str:
        return None
    else:
        symbol=symbol.upper()
    if timeFrame==DAILY:
        timeFrame=mt5.TIMEFRAME_D1
    elif timeFrame==INTRADAY:
        timeFrame=mt5.TIMEFRAME_M1
    elif timeFrame==H1:
        timeFrame=mt5.TIMEFRAME_H1
    else:
        timeFrame=mt5.TIMEFRAME_D1
    if end==None:
        end=datetime.now()
    if type(start).__name__!='datetime' and type(start).__name__!='Timestamp':
        if type(start).__name__!='int':
            print('Error, start should be a datetime or int, but it is ',type(start).__name__)
            return None
        else:
            start_day=datetime.now() #- timedelta(days=start)
            rates=mt5.copy_rates_from(symbol,timeFrame,start_day,start)
             # criamos a partir dos dados obtidos DataFrame
            rates_frame=pd.DataFrame(rates)
            if len(rates_frame)>0:
                rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
            return rates_frame
    else:
        if type(end).__name__=='int':
            rates=mt5.copy_rates_from(symbol,timeFrame,start,end)
        else:
            rates=mt5.copy_rates_range(symbol,timeFrame,start,end)
       # criamos a partir dos dados obtidos DataFrame
        rates_frame=pd.DataFrame(rates)
        if len(rates_frame)>0:
            rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        return rates_frame


def getIntradayBars(symbol, day):
    # definimos o fuso horário como UTC
    #timezone = pytz.timezone("Etc/UTC")
    if not connected:
        print("In order to use this function, you must be connected to the Stock Exchange. Use function connect()")
        return
    if type(day).__name__!='datetime':
        print('Error, start should be a datetime from package datetime')
    else:
       rates=mt5.copy_rates_range(symbol,mt5.TIMEFRAME_M1,\
       day,datetime(day.year,day.month,day.day,23,59))
       rates_frame=pd.DataFrame(rates)
       rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
       # criamos a partir dos dados obtidos DataFrame
       return rates_frame


def roll_bars(bars, new_bars):
    len_new=len(new_bars)
    if len(bars)<=len_new:
        print('The length of bars',len(bars),' should be bigger than the lenght of new_bars ',len(new_bars))
        return bars
    for i in range(len_new):
        bars=bars.drop(i)
    bars=bars.append(new_bars)
    bars=bars.reset_index()
    del bars['index']
    return bars



####### 
# pyportfolioopt auxiliary functions

## It returns a pd.DataFrame like this:
#                XOM        RRC        BBY         MA        PFE        JPM
#date
#2010-01-04  54.068794  51.300568  32.524055  22.062426  13.940202  35.175220
#2010-01-05  54.279907  51.993038  33.349487  21.997149  13.741367  35.856571
#2010-01-06  54.749043  51.690697  33.090542  22.081820  13.697187  36.053574
#2010-01-07  54.577045  51.593170  33.616547  21.937523  13.645634  36.767757
#2010-01-08  54.358093  52.597733  32.297466  21.945297  13.756095  36.677460
# Note that 'date' column is the index, the others are assets' close prices
def get_close_prices(assets,start,end=None,timeFrame=DAILY):
    df=pd.DataFrame()
    first=True
    for asset in assets:
        bars=getBars(asset,start,end,timeFrame)
        if first:
            df['date']=bars['time']
            first=False
        df[asset]=bars['close']
    df=df.set_index('date')
    return df
## It returns a pd.DataFrame like this:
#                XOM        RRC        BBY         MA        PFE        JPM
#date
#2010-01-04  54.068794  51.300568  32.524055  22.062426  13.940202  35.175220
#2010-01-05  54.279907  51.993038  33.349487  21.997149  13.741367  35.856571
#2010-01-06  54.749043  51.690697  33.090542  22.081820  13.697187  36.053574
#2010-01-07  54.577045  51.593170  33.616547  21.937523  13.645634  36.767757
#2010-01-08  54.358093  52.597733  32.297466  21.945297  13.756095  36.677460
# Note that 'date' column is the index, the others are assets' close prices
def get_close_prices_from_dbars(assets,dbars):
    df=pd.DataFrame()
    first=True
    for asset in assets:
        bars=dbars[asset]
        if first:
            df['date']=bars['time']
            first=False
        df[asset]=bars['close']
    df=df.set_index('date')
    return df
  

def get_last_prices(assets):
    last_prices=dict()
    for asset in assets:
        bars=getBars(asset,1,timeFrame=INTRADAY)
        last_prices[asset]=getLastPrice(bars)
    return last_prices

#def adjust_weights(assets,w,capital):
   # sum=0
    #for asset in assets:
    #    aval_capital=w[asset]*capital
    #    last_price=get_last_prices(asset)
    #    shares=se.getAfforShares(asset,aval_capital,last_price)
    #    if shares<=0:
    #        w[asset]=0
    #    else:
    #        w[asset]=(shares*last_price)/capital
    #    sum=sum+w[asset]
    # it can result in small amount of capital not used (remaining capital)
    #   it should be allocated to the risk free asset, so it does not increases portfolio risk
  #  return w

def get_last_prices(assets,dbars):
    last_prices=dict()
    for asset in assets:
        last_prices[asset]=getLastPrice(dbars[asset])
    return last_prices

def get_volume_steps(assets):
    steps=dict()
    for asset in assets:
        steps[asset]=getVolumeStep(asset)
    return steps

def get_curr_shares(assets):
    steps=dict()
    for asset in assets:
        steps[asset]=get_shares(asset)
    return steps

def orders_from_weights(assets,weights,last_prices,capital):
    # sort weights from highest to lowest
    weights=dict(sorted(weights.items(), key=lambda item:item[1],reverse=True))
    #round 1 - buy while never exceeds the desired weight
    sum=0
    curr=dict() # current weights
    volumes=dict() #  order's volumes
    steps=get_volume_steps(assets)
    for asset in assets:
        aval_capital=weights[asset]*capital
        shares=getAfforShares(asset,aval_capital,last_prices[asset],steps[asset])
        if shares<=0:
            curr[asset]=0
            volumes[asset]=0
        else:
            curr[asset]=(shares*last_prices[asset])/capital
            volumes[asset]=shares
        sum=sum+curr[asset]
    #round 2 - if there is remainig capital, buy more lot according weight order 
    remain_capital=capital-sum*capital
    if remain_capital<=0:
        return volumes
    for asset in weights.keys():
        s=steps[asset]
        p=last_prices[asset]
        missing=(weights[asset]-curr[asset])*capital
        while s*p<remain_capital and s*p<missing:
            s=s+steps[asset]
        if s*p>remain_capital :
            s=s-steps[asset]
        curr[asset]=curr[asset]+(s*p)/capital
        volumes[asset]=volumes[asset]+s
        remain_capital=remain_capital-s*p
        if remain_capital<=0:
            break
    return volumes

"""
Old version
def orders_from_weights(assets,weights,last_prices,capital,greedy):
    #if type(weights)!=dict or type(last_prices)!=dict:
    #    raise TypeError("weights, last_prices should be dict() with asset ticker as key")
    #round 1
    sum=0
    curr=dict() # current weights
    volumes=dict() #  order's volumes
    steps=get_volume_steps(assets)
    for asset in assets:
        aval_capital=weights[asset]*capital
        shares=getAfforShares(asset,aval_capital,last_prices[asset],steps[asset])
        if shares<=0:
            curr[asset]=0
            volumes[asset]=0
        else:
            curr[asset]=(shares*steps[asset]*last_prices[asset])/capital
            volumes[asset]=shares
        sum=sum+curr[asset]
    #round 2
    remain_capital=capital-sum*capital
   # if greedy:
        #order by weights
     #   weights=sorted(weights.items(),key=lambda kv:kv[1],reverse=True)
    #else:
        #order by difference 
    if remain_capital<=0:
        return volumes
    sum=0
    for asset in weights.keys():
        aval_capital=weights[asset]*remain_capital
        shares=getAfforShares(asset,aval_capital,last_prices[asset],steps[asset])
        if shares>0:
            curr[asset]=curr[asset]+(shares*steps[asset]*last_prices[asset])/capital
            volumes[asset]=volumes[asset]+shares
        sum=sum+curr[asset]
    return volumes

"""


def get_orders_from_curr_shares(orders,curr_shares):
    new_orders=dict()
    for k in orders.keys():
        new_orders[k]=orders[k]-curr_shares[k]
    return new_orders



##############
# datetime auxiliary functions

def date(year,month,day,hour=0,min=0,sec=0):
    return datetime(year,month,day,hour,min,sec)
###############################


# used in inverse control trader and backtest!!
class Trader:
    def __init__(self):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and setups the operation
    def setup(self,dbars):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and returns a dictionary with the order for each asset
    def analyze(self,dbars):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and frees resources used by the Trader
    def ending(self,dbars):
        pass
 

# used for the Trader to get expected returns
class Analyst:
    def __init__(self):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and setups the operation
    def setup(self,dbars):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and returns a dictionary with the annualized expected returns for each asset
    def analyze(self,dbars):
        pass
    # Receives dbars[asset] - a bars dataframe for each asset in a dictionary
    #   and frees resources used by the Analyst
    def ending(self,dbars):
        pass