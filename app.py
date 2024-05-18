
import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
from helperUI import *
from kiteconnect import KiteConnect
import Login
import Trade
import pandas as pd
import json
st.set_page_config(layout="wide")

# st.cache(ttl=60)
# def LIVE_Update():
#   while True:
#     _,buy,sell = st.columns(3)
#     Buy = pd.read_csv('./Info/buy.csv')
#     Sell = pd.read_csv('./Info/sell.csv')
#     with buy:
#       st.markdown("<h2 style='text-align: left; color: green;'>To Buy</h2>", unsafe_allow_html=True)

#       st.dataframe(Buy)
#     with sell:
#       st.markdown("<h2 style='text-align: left; color: red;'>To Sell </h2>", unsafe_allow_html=True)

#       st.dataframe(Sell)
      
# LIVE_Update()

# @st.experimental_singleton
def Kite_login(Info,access_token):

    
    try:
        kite = KiteConnect(Info['APIKey'], access_token)
        print('Login Successful')

    except:
        try:
            kite = Login.login(Info['APIKey'],Info['APISecret'],Info['ClientID'],Info['ZerodhaPassword'],Info['Totp'])
            
            print("Login Successful")
        except Exception as e:
            print(e)


    return kite

with open(f'./Info/User.json','r') as f:
  Info = json.load(f)

with open(f'./Access_token.txt','r') as f:
    access_token = f.read()


kite=Kite_login(Info,access_token)
print(type(kite))
# kite = None

def Widget(height=600, scrolling=True):
    components.html(
        """<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">Ticker Tape</span></a> by TradingView</div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {
      "description": "BankNifty",
      "proName": "NSE:BANKNIFTY"
    },
    {
      "description": "SenSex",
      "proName": "INDEX:SENSEX"
    },
    {
      "description": "Nifty50",
      "proName": "NSE:NIFTY"
    },
    {
      "description": "NiftyIT",
      "proName": "NSE:CNXIT"
    },
    {
      "description": "NiftyNext50",
      "proName": "NSE:NIFTYJR"
    }
  ],
  "showSymbolLogo": false,
  "colorTheme": "dark",
  "isTransparent": true,
  "displayMode": "regular",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->
  """,
    )

Widget()
from streamlit_autorefresh import st_autorefresh

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=10000, limit=10000000, key="fizzbuzzcounter")
if count !=0:
  _,buy,sell = st.columns(3)
  with buy:
    st.markdown("<h3 style='text-align: left; color: green;'>To Long</h3>", unsafe_allow_html=True)
    try:
      st.dataframe(pd.read_csv('./Info/buy.csv'))
    except:
      st.write("No Stocks to Buy")
  with sell:
    st.markdown("<h3 style='text-align: left; color: red;'>To Short</h3>", unsafe_allow_html=True)
    try:
      st.dataframe(pd.read_csv('./Info/sell.csv'))
    except:
      st.write('No Stocks to Sell')
  st.sidebar.markdown("<h1 style='text-align: center; color: red;'>Trade</h1>", unsafe_allow_html=True)

df = pd.read_csv('./Info/Symbols.csv')

symbol_list = df.Symbol

a,b,c = st.columns([1,1,1])
# with b:
Place_order=False
Symbol, Type, Quantity, Order_type = None,None,None,None
Symbol = st.sidebar.selectbox("Search Symbols", symbol_list)
if Symbol:
    Type = st.sidebar.selectbox("Type",['BUY','SELL'])
    if Type:
        Quantity= st.sidebar.number_input('Quantity',0,10000,1,1,'%d')
        if Quantity:
            Order_type = st.sidebar.selectbox('Order Type',['Limit','Market'])
            if Order_type:
                if Order_type == 'Limit':
                    Limit_price = st.sidebar.number_input("Enter Limit price",format='%5f')
                    market = False
                else:
                    market = True
                    Limit_price = None

                Product = st.sidebar.selectbox("Select Product Type",['Intraday','CNC'])
                try:
                  if Product == 'Intraday':
                    product = kite.PRODUCT_MIS
                  else:
                    product = kite.PRODUCT_CNC
                except:
                  pass
                Place_order =st.sidebar.button("Place Order")

                if Place_order:
                    if Symbol is not None and Type is not None and Quantity is not None and Order_type is not None:
                        #print(Symbol,Type,Quantity,Order_type,market,Limit_price)
                        

                        if Order_type == 'Market':
                          
                            if Type=='BUY':

                              Trade_Status =Trade.Place_order(kite,Symbol,Quantity,kite.TRANSACTION_TYPE_BUY,kite.EXCHANGE_NSE,product,kite.ORDER_TYPE_MARKET)
                            else:
                              Trade_Status= Trade.Place_order(kite,Symbol,Quantity,kite.TRANSACTION_TYPE_SELL,kite.EXCHANGE_NSE,product,kite.ORDER_TYPE_MARKET)

                        else:
                            if Type=='BUY':
                              print("LIMIT_____",Limit_price)
                              Trade_Status = Trade.Place_Limit(kite,Symbol,Quantity,kite.TRANSACTION_TYPE_BUY,kite.EXCHANGE_NSE,product,kite.ORDER_TYPE_MARKET,Limit_price)
                            else:
                              Trade_Status = Trade.Place_Limit(kite,Symbol,Quantity,kite.TRANSACTION_TYPE_SELL,kite.EXCHANGE_NSE,product,kite.ORDER_TYPE_MARKET,Limit_price)
                        print(Trade_Status)
                        if Trade_Status == 'Done':
                          st.sidebar.success(f'Order place for {Symbol} Successful')
                        else:  
                          st.sidebar.error(f'Unable to place Order for {Symbol}')
                          st.sidebar.write(Trade_Status)
                        # Order_df.loc[len(Order_df.index)] = [Symbol,Type, Quantity, Order_type,Limit_price,'Filled',False,str(datetime.datetime.now())]
                        # Order_df.to_csv('./Action/Order.csv',index=False)

                        


st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
task=st.radio('',("Stock Alert","Stock Trend"))
if task =="Stock Alert":

  col11,col22,col33 = st.columns(3)

  indicators = ['','Bollinger Band','RSI','Moving Average','MACD','Supertrend']

  functions = {'Bollinger_Band':Bollinger_Band,'RSI':RSI,'Moving_Average':Moving_Average,'MACD':MACD,'Supertrend':Supertrend}
              

  with col22:
    timeFrame = st.text_input("BB TimeFrame",value='15Min',help="e.g.1Min,1H,1D,1W,1M")

    noIndicatorEntry = st.text_input('Enter number of Indicator') 

  
  def helper_indicator(type,key,noIndicatorEntry):
      
    x=[]
    Entry_Stretegy = {}
    Indicator_list = []

    if noIndicatorEntry != '':
      x = st.columns(int(noIndicatorEntry))
      for i in range(int(noIndicatorEntry)):
        with x[i]:
          Indicator = st.selectbox(f'Select Indicator {str(i)+str(1)}',indicators,key=str(key)+str(i))
          Indicator_list.append(Indicator)
          #Get the indicator and call show the parameters
          #print(Entry_Stretegy.keys(),"--Entry S")
          ind_str = Indicator_list[i].replace(' ','_')
          if ind_str != '':
  
            if ind_str in Entry_Stretegy.keys():
                
              Entry_Stretegy[ind_str+f'{i}'] = functions[ind_str](str(key)+str(i))
            else:
              Entry_Stretegy[ind_str] = functions[ind_str](str(key)+str(i))
          #print("Entry Stretegy:",Entry_Stretegy)

          for key,val in Entry_Stretegy.items():
            if val == None:
              st.warning(f"Please Save {key} by checking")
        
                
      return Entry_Stretegy
      
  Entry_Stretegy = helper_indicator('Strategy',1,noIndicatorEntry)


  aaa,bbb,ccc = st.columns(3)


  with bbb:
    Save = st.checkbox('Save Strategy')
    if Save:
      Entry_Stretegy['TimeFrame'] = timeFrame
      with open(f'./Info/Strategy.json','w') as f:
                json.dump(Entry_Stretegy,f)


#------TRend ----

else:
  a,b,c = st.columns(3)
  with b:
    st.markdown("<h2 style='text-align: left; color: red;'>Stock Sentiment Today!</h2>", unsafe_allow_html=True)
    Trend = pd.read_csv('./Info/Trend.csv')
    st.dataframe(Trend)

