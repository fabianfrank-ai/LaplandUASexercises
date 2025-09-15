#Verdict.py tries to use the sma, bollinger bands,ema and macd and rsi in order to create a verdict how the user should trade
#The verdict is based on the following rules:
#Out of the 5 indicators, if 3 or more indicate buy/sell, the verdict is buy/sell
#If only 1,2 indicator indicates buy/sell, the verdict is hold
#If none of the indicators indicate buy/sell, the verdict is hold
#Note: This is a very simple approach and should not be used for real trading decisions. It is just for educational purposes.

import pandas as pd
from indicators import ema, macd

def generate_verdict(data,short_sma,long_sma,lower_band,upper_band,rsi):
    """Generate a trading verdict based on multiple technical indicators."""
  
    # at the beginning of the function, set the signals to 0, as there is no data yet
    buy_signals = 0
    sell_signals = 0


    # SMA signal
    # as market prices may vary, we will use the percantage difference between long and short SMA
    sma_diff=(short_sma - long_sma) / long_sma * 100



   # use 0.3 as threshold to decide whether the difference between sma differences is noteworthy enough
    if sma_diff.iloc[-1] > 0.3: 
        buy_signals += 1
    elif sma_diff.iloc[-1] < -0.3:
        sell_signals += 1
    else:
        pass  # No signal from SMA

 

    # Bollinger Bands signal
    if upper_band.iloc[-1] < data['Close'].iloc[-1]:  
        sell_signals += 1
    elif lower_band.iloc[-1] > data['Close'].iloc[-1]:  
        buy_signals += 1
    else:
        pass  # No signal from Bollinger Bands
    


    # RSI signal
    if rsi.iloc[-1] > 70:  
        sell_signals += 1
    elif rsi.iloc[-1] < 30:  
        buy_signals += 1
    else:
        pass  # No signal from RSI


    # EMA signal
    ema_short=ema(data, 12)
    ema_long=ema(data, 26)


    if ema_short.iloc[-1] > ema_long.iloc[-1]:
        buy_signals += 1
    elif ema_short.iloc[-1] < ema_long.iloc[-1]:
        sell_signals += 1
    else:
        pass  # No signal from EMA


    # MACD signal
    macd_line, signal_line=macd(data)
    if macd_line.iloc[-1] > signal_line.iloc[-1]:
        buy_signals += 1
    elif macd_line.iloc[-1] < signal_line.iloc[-1]:
        sell_signals += 1
    else:
        pass  # No signal from MACD
     

    # return verdict
    if buy_signals >= 3 and buy_signals < 5:
        return "Buy"
    if buy_signals >=4:
        return "Strong Buy"
    elif sell_signals >=3 and sell_signals < 5:
        return "Sell"
    elif sell_signals >= 4:
        return "Strong Sell"
    else:
        return "Hold"
    

