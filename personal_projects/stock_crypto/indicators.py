#chatgpt was used to suggest equations for suitable indicatiors
import pandas as pd

sma=pd.DataFrame()
crossings=[]

def sma(data, window):
    """Calculate Simple Moving Average (SMA)"""
    #SMA = sum of closing prices over the window / window size (SMA20 is used, so window=20)
    #https://medium.com/analytics-vidhya/sma-short-moving-average-in-python-c656956a08f8
    
    sma=data['Close'].rolling(window=window).mean()
    return sma


def crossing(short_sma, long_sma):
    """Return a DataFrame with the crossing points of short and long SMA."""
    for i in range(1, len(short_sma)):
        if short_sma.iloc[i-1] > long_sma.iloc[i-1] and short_sma.iloc[i-2] <= long_sma.iloc[i-2]:
            crossings.append((short_sma.index[i-1], short_sma.iloc[i-1]))
            return crossings
        elif short_sma.iloc[i-1] < long_sma.iloc[i-1] and short_sma.iloc[i-2] >= long_sma.iloc[i-2]:
            crossings.append((short_sma.index[i-1], short_sma.iloc[i-1]))
            return crossings
    return []
   

def bollinger_bands(data,window):
    """Calculate Bollinger Bands"""
    #Bollinger Bands consist of a middle band (SMA), an upper band, and a lower band.
    #The upper band is typically 2 standard deviations above the SMA, and the lower band is 2 standard deviations below the SMA.
    #typically if the current market price is near/above the upper band, the asset is considered overbought
    #if the price is near/below the lower band, the asset is considered oversold
    sma= data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2) 
    return lower_band, upper_band


def rsi(data, window):
    """Calculate Relative Strength Index (RSI)"""
    #RSI = 100 - (100 / (1 + RS))
    #RS = Average Gain / Average Loss over the specified window
    #Typically, an RSI above 70 indicates overbought conditions, while an RSI below 30 indicates oversold conditions.
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Further indicators can be added here in the future

