# chatgpt was used to suggest equations for suitable indicatiors
import pandas as pd

sma=pd.DataFrame()
crossings=[]



def sma(data, window):
    """Calculate Simple Moving Average (SMA)"""


    # SMA = sum of closing prices over the window / window size (SMA30 and 100 are used, so window=100)
    # https://medium.com/analytics-vidhya/sma-short-moving-average-in-python-c656956a08f8
    
    sma=data['Close'].rolling(window=window).mean()


    return sma
   


def bollinger_bands(data,window):
    """Calculate Bollinger Bands"""


    # Bollinger Bands consist of a middle band (SMA), an upper band, and a lower band.
    # The upper band is typically 2 standard deviations above the SMA, and the lower band is 2 standard deviations below the SMA.
    # typically if the current market price is near/above the upper band, the asset is considered overbought
    # if the price is near/below the lower band, the asset is considered oversold
    sma= data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2) 


    return lower_band, upper_band



def rsi(data, window):
    """Calculate Relative Strength Index (RSI)"""


    # RSI = 100 - (100 / (1 + RS))
    # RS = Average Gain / Average Loss over the specified window
    # Typically, an RSI above 70 indicates overbought conditions, while an RSI below 30 indicates oversold conditions.
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi



def price_change(data):
    """Calculate Price Change Percentage"""


    # Price Change Percentage = ((Current Price - Previous Price) / Previous Price) * 100
    price_change=((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) *100


    return price_change.round(2)



def ema(data, window):
    """Calculate Exponential Moving Average (EMA)"""


    # EMA gives more weight to recent prices, making it more responsive to new information.
    # EMA_today = (Price_today * (smoothing / (1 + window))) + (EMA_yesterday * (1 - (smoothing / (1 + window))))
    # A common smoothing factor is 2.
    ema = data['Close'].ewm(span=window, adjust=False).mean()
    return ema



def macd(data, short_window=12, long_window=26, signal_window=9):
    """Calculate Moving Average Convergence Divergence (MACD)"""


    # MACD = 12-day EMA - 26-day EMA
    # Signal Line = 9-day EMA of MACD
    ema_short = ema(data, short_window)
    ema_long = ema(data, long_window)
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    return macd_line, signal_line


# Further indicators can be added here in the future

