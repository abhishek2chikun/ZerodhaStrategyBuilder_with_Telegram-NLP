import pandas_ta  as ta
import pandas as pd
import json
import time
import sqlite3
from datetime import date
import glob
import os

def Create_Strategy(Input,Token):

      Buy_symbol = []
      Sell_symbol = []
      Buy_price = []
      Sell_price = []
      TA = []
  
      Keys = Input.keys()
      for i in Keys:
        if i == 'Bollinger_Band' or i == 'RSI' or i == 'Moving_Average':
          if i =='Bollinger_Band':
            TA.append({'kind':'bbands','length':Input[i]['length'],'std':Input[i]['std']})
          elif i == 'Moving_Average':
            TA.append({'kind':'sma','length':Input[i]['length']})
          else:
            TA.append({'kind':'rsi','length':Input[i]['length']})

        elif i =='Supertrend':
            TA.append({'kind':'supertrend','length':Input[i]['ATR_length'],'multiplier':Input[i]['Factor']}) 
        
       
      CustomStrategy = ta.Strategy(
          name="Strategy",
          description="Custom Strategy",
          ta=TA
      )
      if Input['TimeFrame'] == '1D':
        tokens = glob.glob('./YData/*')
      else:
        d = date.today().strftime("%d%b%Y")
        
        db = sqlite3.connect('./WData/' + d +'.db')
        c=db.cursor()
        c.execute('SELECT name from sqlite_master where type= "table"')
        tokens = c.fetchall()
      # print(tokens)

      # c.execute('''PRAGMA table_info(TOKEN975873)''')
      # c.fetchall()
      for token in tokens:
        # print(token)
        
        # for m in c.execute(f'''SELECT * FROM {token[0]}'''):
        if Input['TimeFrame'] == '1D':
          df = pd.read_csv(token,parse_dates=['Date'])
        else:
          df_ = pd.read_sql(f'''SELECT * FROM {token[0]}''',db,parse_dates={'ts': {"format": "%Y-%m-%d %H:%M:%S"}})[:-900]
          # print(df_.tail())
          df = pd.DataFrame(columns=['High','Low','Open','Close'])
          print(df)
          df['High'] = df_.resample(Input['TimeFrame'],on='ts')['price'].max()
          df['Low'] = df_.resample(Input['TimeFrame'],on='ts')['price'].min()
          
          df['Open'] = df_.resample(Input['TimeFrame'],on='ts')['price'].first()
          df['Close'] = df_.resample(Input['TimeFrame'],on='ts')['price'].last()

        
        if  Keys != 'MACD':
            
          df.ta.strategy(CustomStrategy)
        
        buy_flage = False
        sell_flage = False
        Time = df.index[-1]
        
        for i in Keys:
          print(i)
          if i == 'RSI':
            if list(df[f'RSI_{Input["RSI"]["length"]}'])[-1] < Input["RSI"]["RSI_Oversold"]:
                buy_flage = True
            elif list(df[f'RSI_{Input["RSI"]["length"]}'])[-1] > Input["RSI"]["RSI_Overbrought"]:
                sell_flage = True
              
          elif i == 'MACD':
            ewm_short = df.Close.ewm(span=Input["MACD"]["slow"], adjust=False).mean()
            ewm_long = df.Close.ewm(span=Input["MACD"]["fast"], adjust=False).mean()
            df['MACD']=ewm_short-ewm_long
            df['signal_MACD']=df['MACD'].ewm(span=9, adjust=False).mean()

            if list(df[f'MACD'])[-2] < list(df[f'signal_MACD'])[-2] and list(df[f'MACD'])[-1] > list(df[f'signal_MACD'])[-1] :
              buy_flage = True
            elif list(df[f'MACD'])[-2] > list(df[f'signal_MACD'])[-2] and list(df[f'MACD'])[-1] < list(df[f'signal_MACD'])[-1] :
              sell_flage = True
            
          elif i == 'Bollinger_Band':
            if list(df[f'BBU_{Input["Bollinger_Band"]["length"]}_{Input["Bollinger_Band"]["std"]}.0'])[-1] < list(df['Close'])[-1]:
              buy_flage = True
            if list(df[f'BBL_{Input["Bollinger_Band"]["length"]}_{Input["Bollinger_Band"]["std"]}.0'])[-1] > list(df['Close'])[-1]:
              sell_flage = True

          elif i == 'Moving_Average':
            if list(df[f'SMA_{Input["Moving_Average"]["length"]}'])[-1] < list(df['Close'])[-1]:
                buy_flage = True
            if list(df[f'SMA_{Input["Moving_Average"]["length"]}'])[-1] > list(df['Close'])[-1]:
                sell_flage = True
            
          elif i == 'Supertrend':
            
            green = df[f'SUPERTl_{Input["Supertrend"]["ATR_length"]}_{int(Input["Supertrend"]["Factor"])}.0']
            red = df[f'SUPERTl_{Input["Supertrend"]["ATR_length"]}_{int(Input["Supertrend"]["Factor"])}.0']
            green = green.fillna(0)
            red = red.fillna(0)
           
            if list(green)[-1] !=0:
              buy_flage = True
            if list(green)[-1] ==0:
              sell_flage = True

          if Input['TimeFrame'] == '1D':
            if buy_flage == True and os.path.basename(token).split('.')[0] not in Buy_symbol:
                Buy_symbol.append(os.path.basename(token).split('.')[0])
                Buy_price.append(list(df['Close'])[-1])
            elif sell_flage == True and os.path.basename(token).split('.')[0] not in Sell_symbol:
                Sell_symbol.append(os.path.basename(token).split('.')[0])
                Sell_price.append(list(df['Close'])[-1])

          else:

            if buy_flage == True and Token[token[0][5:]] not in Buy_symbol:
                Buy_symbol.append(Token[token[0][5:]])
                Buy_price.append(df['Close'][-1])
            elif sell_flage == True and Token[token[0][5:]] not in Sell_symbol:
                Sell_symbol.append(Token[token[0][5:]])
                Sell_price.append(df['Close'][-1])
      print(Buy_symbol,Sell_symbol)
      print(Buy_price,Sell_price)
      if len(Buy_symbol) !=0:
        df_buy = pd.DataFrame({'Symbol':Buy_symbol,'Price':Buy_price})
        df_buy['Time'] = Time
        # df_buy.to_csv('./Info/buy.csv',index=False)
      else:
        df_buy = pd.DataFrame(columns=['Symbol','Price'])
      
      
      df_buy.to_csv('./Info/buy.csv',index=False)
      if len(Sell_symbol) !=0:
        df_sell = pd.DataFrame({'Symbol':Sell_symbol,'Price':Sell_price})
        df_sell['Time'] = Time
      else:
        df_sell = pd.DataFrame(columns=['Symbol','Price'])
      
     
      df_sell.to_csv('./Info/sell.csv',index=False)


      return "Done"

if __name__ == '__main__':
    while True:
      try:
        with open('./Info/Strategy.json','r') as f:
            Input = json.load(f)
        with open('./token.json','r') as f:
            Token = json.load(f)
        Create_Strategy(Input,Token)
        time.sleep(20)
      except Exception as e:
        print("Error!!!",e)
