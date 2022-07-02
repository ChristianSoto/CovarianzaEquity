import pandas as pd
import seaborn as sb
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import requests
import math

#La API de Yahoo requiere headers para establecer la conexión y devolver la data
USER_AGENT = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                   ' Chrome/91.0.4472.124 Safari/537.36')
    }
sesh = requests.Session()
sesh.headers.update(USER_AGENT)

def stock_data(stocks, start='1-1-2000', end=dt.datetime.strftime(dt.datetime.today(),"%d-%m-%Y")):
  data=pd.DataFrame()
  for stock in stocks:
    data[stock]= pdr.DataReader(stock,'yahoo',start=start,end=end,session=sesh)['Adj Close']
  return data

def pct_ret_log(stocks):
  change= np.log(stocks/stocks.shift(1))
  return change.dropna()

stocks=['QQQ','SPY','XLP','XLE','USO','XLRE','GLD','SLV','XLV','XLK','XLY','TLT','DBA','EEM','UVXY']
stocks.sort()
a=stock_data(stocks)
a=a.dropna()


b=pct_ret_log(a)

plt.style.use('dark_background')
desvest= pd.DataFrame(round(b.std()*100*math.sqrt(250),2))
desvest.columns=['Volatilidad']
fig,ax=plt.subplots(figsize=(30,15),ncols=2)
sb.heatmap(round(b.corr(),2), vmin=-1, vmax=1, annot=True,ax=ax[0])
ax[0].tick_params(axis='y', labelsize=14)
ax[0].tick_params(axis='x', labelsize=14)
ax[1].bar(desvest.index,desvest['Volatilidad'],color='red')
ax[1].grid(alpha=0.5)
ax[1].set_title('Volatilidad anual del activo',fontsize=14)
ax[1].tick_params(axis='y', labelsize=14)
ax[1].tick_params(axis='x', labelsize=14)

plt.show()