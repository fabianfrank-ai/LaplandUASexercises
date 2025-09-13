#Verdict.py tries to use the sma, bollinger bands and rsi in order to create a verdict how the user should trade
#The verdict is based on the following rules:
#Out of the 3 indicators, if 2 or more indicate buy/sell, the verdict is buy/sell
#If only 1 indicator indicates buy/sell, the verdict is hold
#If none of the indicators indicate buy/sell, the verdict is hold
#Note: This is a very simple approach and should not be used for real trading decisions. It is just for educational purposes.

import pandas as pd

def generate_verdict(data,short_sma,long_sma,lower_band,upper_band,rsi):
    #at the beginning of the function, set the signals to 0, as there is no data yet
    buy_signals=0
    sell_signals=0
    

    #SMA signal
    #as market prices vary, we will use the percantage difference between long and short SMA
    sma_diff=(short_sma - long_sma) / long_sma * 100


    if sma_diff.iloc[-1] > 0.3: 
        buy_signals += 1
    elif sma_diff.iloc[-1] < -0.3:
        sell_signals += 1
    else:
        pass  # No signal from SMA


    #Bollinger Bands signal
    if upper_band.iloc[-1] < data['Close'].iloc[-1]:  # Price above upper band
        sell_signals += 1
    elif lower_band.iloc[-1] > data['Close'].iloc[-1]:  # Price below lower band
        buy_signals += 1
    else:
        pass  # No signal from Bollinger Bands

    #RSI signal
    if rsi.iloc[-1] > 70:  # Overbought
        sell_signals += 1
    elif rsi.iloc[-1] < 30:  # Oversold
        buy_signals += 1
    else:
        pass  # No signal from RSI

    if buy_signals >=2:
        return "Buy"
    elif sell_signals >=2:
        return "Sell"
    else:
        return "Hold"
    

