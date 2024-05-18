import yfinance as yf
import datetime
import pandas as pd
import glob
import os
import time
import datetime as dt

def YFDownload(Symbol):
    files = glob.glob('./YData/*')
    file_symbols = [i.split('.')[0] for i in files]
    if Symbol not in file_symbols:
        start_date = datetime.datetime.now() - dt.timedelta(days=30)
        
        end_date = datetime.datetime.now() - dt.timedelta(days=1)

        data = yf.download(Symbol, start=start_date, end=end_date)
        
        data.to_csv(f'./YData/{Symbol.split(".")[0]}.csv')
    
    return 'Done'

df = pd.read_csv('./Info/Symbols.csv')
Symbols = list(df['Symbol'])
for symbol in Symbols:
    YFDownload(symbol+'.NS')
