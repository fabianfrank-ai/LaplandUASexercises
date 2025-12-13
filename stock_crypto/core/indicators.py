'''
Here you find essential indicators in the Indicators class, easy maintenance and modularity allow for adding of more tickers,
if you desire to get further input, please do not hesitate to look at the indicators_guide notebook in notebooks, code is
briefly explained here but for further insight it might be sensible to look at a complete explanation.
'''


# chatgpt was used to suggest equations for suitable indicatiors
import pandas as pd


class Indicators:
    """
    Calculate common technical indicators for a stock DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing stock data with columns ['Open', 'High', 'Low', 'Close', ...].

    Examples
    --------
    indicators = Indicators(data)
    sma_30 = indicators.sma(30)
    rsi_14 = indicators.rsi()
    macd_line, signal_line = indicators.macd()

    Notes
    -----
    - All methods operate on the 'Close' price column by default unless otherwise specified.
    - Designed to be modular: new indicators can be added easily.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Store stock data for indicator calculations.

        Parameters
        ----------
        data : pd.DataFrame
            Historical stock data for a single ticker.
        """

        self.data = data
# ==============================================================================================================================

    def sma(self, window: int) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA) over a given window.

        Parameters
        ----------
        window : int
            Number of periods to calculate the SMA.

        Returns
        -------
        pd.Series
            SMA values.
        """

        # SMA = sum of closing prices over the window / window size (SMA30 and 100 are used, so window=100)
        # https://medium.com/analytics-vidhya/sma-short-moving-average-in-python-c656956a08f8
        sma = self.data['Close'].rolling(window=window).mean()

        return sma

  # ===========================================================================================================================
    def moving_average_crossover(self, short_ma: pd.Series, long_ma: pd.Series) -> pd.Series:
        """
        Identify moving average crossovers: Golden Crosses and Death Crosses.

        Parameters
        ----------
        short_ma : pd.Series
            Short-term moving average.
        long_ma : pd.Series
            Long-term moving average.

        Returns
        -------
        pd.Series
            Series of crossover types ('Golden Cross' or 'Death Cross') indexed by date.
        """

        # empty DataFrame to store crossover signals
        crossings = pd.DataFrame()
        crossings_data = []

        # A golden cross occurs when a short-term moving average crosses above a long-term moving average, indicating a potential bullish trend.
        for i in range(1, len(self.data)):
            if i < len(self.data) - 1:

                if short_ma.iloc[i+1] > long_ma.iloc[i+1] and short_ma.iloc[i-1] <= long_ma.iloc[i-1]:
                    crossings_data.append((self.data.index[i], 'Golden Cross'))

                elif short_ma.iloc[i+1] < long_ma.iloc[i+1] and short_ma.iloc[i-1] >= long_ma.iloc[i-1]:
                    crossings_data.append((self.data.index[i], 'Death Cross'))

                else:
                    continue

        if crossings_data:
            crossings = pd.DataFrame(crossings_data, columns=[
                'Date', 'Crossover Type']).set_index('Date')

        return crossings['Crossover Type']
# ==============================================================================================================================================

    def bollinger_bands(self, window: int = 30) -> tuple[pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands.

        Parameters
        ----------
        window : int
            Rolling window for SMA and standard deviation.

        Returns
        -------
        tuple[pd.Series, pd.Series]
            (lower_band, upper_band)
        """

        # Bollinger Bands consist of a middle band (SMA), an upper band, and a lower band.
        # The upper band is typically 2 standard deviations above the SMA, and the lower band is 2 standard deviations below the SMA.
        # typically if the current market price is near/above the upper band, the asset is considered overbought
        # if the price is near/below the lower band, the asset is considered oversold
        sma = self.sma(window)
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.std.html
        std = self.data['Close'].rolling(window=window).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)

        return lower_band, upper_band
# ================================================================================================================================================

    def rsi(self, window: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).

        Parameters
        ----------
        window : int
            Lookback period for gains and losses.

        Returns
        -------
        pd.Series
            RSI values (0-100 scale).
        """

        # RSI = 100 - (100 / (1 + RS))
        # RS = Average Gain / Average Loss over the specified window
        # Typically, an RSI above 70 indicates overbought conditions, while an RSI below 30 indicates oversold conditions.
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi
# ===================================================================================================================================================

    def price_change(self) -> float:
        """
        Calculate overall price change percentage for the data.

        Returns
        -------
        float
            Price change between first and last closing price, rounded to 2 decimals.
        """

        # Price Change Percentage = ((Current Price - Previous Price) / Previous Price) * 100
        price_change = (
            (self.data['Close'].iloc[-1] - self.data['Close'].iloc[0]) / self.data['Close'].iloc[0]) * 100

        return price_change.round(2)
# =================================================================================================================================================

    def ema(self, window: int) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).

        Parameters
        ----------
        window : int
            Lookback period for EMA.

        Returns
        -------
        pd.Series
            EMA values.
        """
        # EMA gives more weight to recent prices, making it more responsive to new information.
        # EMA_today = (Price_today * (smoothing / (1 + window))) + (EMA_yesterday * (1 - (smoothing / (1 + window))))
        # A common smoothing factor is 2.
        ema = self.data['Close'].ewm(span=window, adjust=False).mean()
        return ema
# =================================================================================================================================================

    def macd(self, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> tuple[pd.Series, pd.Series]:
        """
        Calculate MACD and Signal Line.

        Returns
        -------
        tuple[pd.Series, pd.Series]
            (macd_line, signal_line)
        """

        # MACD = 12-day EMA - 26-day EMA
        # Signal Line = 9-day EMA of MACD
        ema_short = self.ema(short_window)
        ema_long = self.ema(long_window)
        macd_line = ema_short - ema_long
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

        return macd_line, signal_line

# ====================================================================================================================================================
    def atr(self, window: int = 14) -> float:
        """
        Calculate Average True Range (ATR) scaled to 0-100.

        Parameters
        ----------
        window : int
            Lookback period for ATR calculation.

        Returns
        -------
        float
            ATR value representing recent volatility.
        """

        # Average true range is an indicator for market volatility and therefore risk

        true_ranges = pd.DataFrame()
        true_ranges['H-L'] = self.data['High'] - self.data['Low']
        true_ranges['H-PC'] = abs(self.data['High'] -
                                  self.data['Close'].shift(1))
        true_ranges['L-PC'] = abs(self.data['Low'] -
                                  self.data['Close'].shift(1))
        true_range = true_ranges.max(axis=1)

        atr = true_range.rolling(window=window).mean()

        # scale atr to be between 0 and 100 : easier to understand percentages
        atr_scaled = (atr / atr.max()) * 100

        return atr_scaled.iloc[-1]

    # Further indicators can be added here in the future
