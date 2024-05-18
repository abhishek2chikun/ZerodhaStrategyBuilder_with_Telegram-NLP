from kiteconnect import KiteTicker, KiteConnect
import datetime
import sys
import pandas as pd
import os
import sqlite3
from datetime import date
import json

# cwd = os.chdir("C:\\Users\\Balaji\\Desktop\\kite\\")
with open(f'./Info/User.json','r') as f:
  Info = json.load(f)
#generate trading session
access_token = open("Access_token.txt",'r').read()
key_secret = [Info['APIKey'],Info['APISecret']]
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

d = date.today().strftime("%d%b%Y")
db = sqlite3.connect('./WData/' + d +'.db')

def create_tables(tokens):
    c=db.cursor()
    for i in tokens:
        c.execute("CREATE TABLE IF NOT EXISTS TOKEN{} (ts datetime primary key,price real(15,5), volume integer,oi integer,buy_quantity integer,sell_quantity integer,oi_day_high integer,oi_day_low integer)".format(i))
    try:
        db.commit()
    except:
        db.rollback()

def insert_ticks(ticks):
    c=db.cursor()
    for tick in ticks:
        try:
            tok = "TOKEN"+str(tick['instrument_token'])
            vals = [tick['timestamp'],tick['last_price'], tick['last_quantity'], tick['oi'], tick['buy_quantity'], tick['sell_quantity'], tick['oi_day_high'], tick['oi_day_low']]
            query = "INSERT INTO {}(ts,price,volume,oi,buy_quantity,sell_quantity,oi_day_high,oi_day_low) VALUES (?,?,?,?,?,?,?,?)".format(tok)
            c.execute(query,vals)
        except:
            pass
    try:
        db.commit()
    except:
        db.rollback()    


#get dump of all NSE instruments
instrument_dump = kite.instruments('NSE')
instrument_df = pd.DataFrame(instrument_dump)

def tokenLookup(instrument_df,symbol_list):
    """Looks up instrument token for a given script from instrument dump"""
    token_list = []
    token_dict = {}
    for symbol in symbol_list:
        token = int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0])
        token_list.append(token)
        token_dict[token] = symbol
    with open('./token.json','w') as f:
        
        json.dump(token_dict,f)

    return token_list


Symbols = pd.read_csv(f'./Info/Symbols.csv')
tickers = list(Symbols.Symbol)
#create KiteTicker object
# tickers =['BANKNIFTY2221737800CE', 'BANKNIFTY2221737900CE', 'BANKNIFTY2221738000CE','BANKNIFTY2221737600PE', 'BANKNIFTY2221737500PE', 'BANKNIFTY2221737400PE']
kws = KiteTicker(key_secret[0],kite.access_token)
tokens = tokenLookup(instrument_df,tickers)

#create table
create_tables(tokens)


def on_ticks(ws,ticks):
    insert_tick=insert_ticks(ticks)
    print(ticks)

def on_connect(ws,response):
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL,tokens)
    

while True:
    now = datetime.datetime.now()
    print(now.hour,now.minute)
    if (now.hour >= 15 and now.minute >= 30):
        print("Market Closed")
        db.close()
        
        sys.exit()
    if (now.hour >= 9 and now.minute >= 14 ):
        kws.on_ticks=on_ticks
        kws.on_connect=on_connect
        kws.connect()
   
