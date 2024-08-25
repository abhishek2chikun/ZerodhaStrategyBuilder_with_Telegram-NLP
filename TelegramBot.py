import schedule
import telebot
from threading import Thread
import pandas as pd
import dataframe_image
from time import sleep


API_KEY ='APIKEY'
bot = telebot.TeleBot(API_KEY)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

chart_id = 'xxxxx'

def Alert():

  try:
    Buy = pd.read_csv('./Info/buy.csv')
    Sell = pd.read_csv('./Info/sell.csv')
    Trend = pd.read_csv('./Info/Trend.csv')
  
    dataframe_image.export(Buy, "./Info/buy.png")
    dataframe_image.export(Sell, "./Info/sell.png")
    dataframe_image.export(Trend,"./Info/trend.png")

    bot.send_photo(chart_id, photo= open("./Info/buy.png", 'rb')  , caption="Buy")
    bot.send_photo(chart_id, photo= open("./Info/sell.png", 'rb')  , caption="Sell")
    bot.send_photo(chart_id, photo= open("./Info/trend.png", 'rb')  , caption="Trend")
  except:
    pass
 

#If needed can change the frequency 
Frequency_in_minutes = 1
schedule.every(Frequency_in_minutes).minutes.do(Alert)


Thread(target=schedule_checker).start() 
