#Indicators Function
import streamlit as st
import random 

def Bollinger_Band(i):
    # timeFrame = st.text_input("BB TimeFrame",value='1D',help="e.g.1Min,1H,1D,1W,1M",key=i + str(random.randint(1,100)))

    Length =  int(st.number_input("BB Length",value=14,step=1,key=i + str(random.randint(1,100))))

    Std = st.number_input("BB StdDev",value=2,step=1,key=i + str(random.randint(1,100)))
    
   
    if st.checkbox('Save paramters for BB ',key=i + str(random.randint(1,100))):
        return {'length':Length,'std':Std}

def RSI(i):
    # timeFrame = st.text_input("RSI TimeFrame",value='1D',help="e.g.1Min,1H,1D,1W,1M",key=i + str(random.randint(1,100)))

    Length =  int(st.number_input("RSI Length",value=4,step=1,key=i + str(random.randint(1,100))))
    
    RSI_Overbrought = st.number_input("Enter RSI Overbrought threshold Value",value=70)

    RSI_Oversold = st.number_input("Enter RSI Oversold threshold Value",value=30)


    if st.checkbox('Save paramters for RSI ',key=i + str(random.randint(1,100))):
        return {'length':Length,'RSI_Overbrought':RSI_Overbrought,'RSI_Oversold':RSI_Oversold}

def Moving_Average(i):
    # timeFrame = st.text_input(f"MA TimeFrame{i}",value='1D',help="e.g.1Min,1H,1D,1W,1M",key=i + str(random.randint(1,100)))

    Length =  int(st.number_input("MA Length",value=14,step=1,key=i + str(random.randint(1,100))))
    
    if st.checkbox('Save paramters for MA',key=i + str(random.randint(1,100))):
        return {'length':Length}


def MACD(i):
    # timeFrame = st.text_input("MACD Cross TimeFrame",value='1D',help="e.g.1Min,1H,1D,1W,1M",key=i + str(random.randint(1,100)))

    slowLength =  int(st.number_input("Slow MACD Length",value=20,step=1,key=i + str(random.randint(1,100))))
    fastLength =  int(st.number_input("Fast MACD Length",value=9,step=1,key=i + str(random.randint(1,100))))

    

    if st.checkbox('Save paramters for MACD Cross',key=i + str(random.randint(1,100))):
        return {'slow':slowLength,'fast':fastLength}

def Supertrend(i):
    # timeFrame = st.text_input("Supertrend TimeFrame",value='1D',help="e.g.1Min,1H,1D,1W,1M",key=i + str(random.randint(1,100)))

    ATR_length =  int(st.number_input("Supertrend ATR Length",value=10,step=1,key=i + str(random.randint(1,100))))

    Factor = st.number_input("Supertrend Factor",value=3,step=1,key=i + str(random.randint(1,100)))
    
    if st.checkbox('Save paramters for Supertrend ',key=i + str(random.randint(1,100))):
        return {'ATR_length':ATR_length,'Factor':Factor}

