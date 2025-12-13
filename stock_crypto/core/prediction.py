"""
Handles generation of predictive signals based on processed market data.
Implements logic for estimating future movements, aggregating indicator
verdicts, and producing a consolidated prediction output.
"""

from core.indicators import Indicators
import pandas as pd


class Prediction:
    """
    Generates a simple predictive estimate of future stock prices using technical indicators.

    The prediction is based on a weighted combination of SMA, EMA, RSI, Bollinger Bands, and MACD signals.
    The calculated trend score is applied to the last closing price to project future prices.

    Parameters
    ----------
    data : pd.DataFrame
        Historical stock data containing at least the 'Close' column.
    timeframe : int
        Number of trading days to predict into the future.
    """

    def __init__(self, data, timeframe):
        self.data = data
        self.timeframe = timeframe

        # run the prediction immediately upon initialization
        self.prediction()

    def retreive_data(self):
        """
        Calculate indicator-based trend score for the latest data point.

        Steps:
        1. Compute SMA, EMA, RSI, Bollinger Bands, and MACD indicators.
        2. Align SMAs and EMAs to calculate relative differences.
        3. Convert indicators into discrete scores (-1, 0, 1) based on thresholds.
        4. Combine weighted scores into a single trend_score.
        """

        indicators = Indicators(self.data)
        # I explained the idea in the notebook in notebooks/

        # Compute technical indicators
        sma_short = indicators.sma(30)
        sma_long = indicators.sma(100)
        ema_short = indicators.ema(12)
        ema_long = indicators.ema(26)
        rsi_14 = indicators.rsi(14)
        lower_band, upper_band = indicators.bollinger_bands(30)
        macd_line, signal_line = indicators.macd()

        # Align moving averages for safe difference calculation
        sma_short, sma_long = sma_short.align(sma_long, join='inner')
        sma_diff = (sma_short - sma_long) / sma_long

        ema_short, ema_long = ema_short.align(ema_long, join='inner')
        ema_diff = (ema_short - ema_long) / ema_long

        # if a desired indicator is good, it's score is 1, otherwise -1

        # RSI scoring: overbought -> 1, oversold -> -1, neutral -> 0
        if rsi_14.iloc[-1] > 70:
            rsi_score = 1

        elif rsi_14.iloc[-1] < 30:
            rsi_score = -1

        else:
            rsi_score = 0

        # Bollinger Bands scoring: near lower band -> -1, above mid-point -> 1, else 0
        bollinger_percentage = (self.data['Close'].iloc[-1] - lower_band.iloc[-1]
                                ) / (upper_band.iloc[-1] - lower_band.iloc[-1])

        if bollinger_percentage < 0.2:
            bb_score = -1

        elif bollinger_percentage > 0.5:
            bb_score = 1

        else:
            bb_score = 0

        # MACD scoring: bullish -> 1, bearish -> -1, neutral -> 0
        if macd_line.iloc[-1] > signal_line.iloc[-1]:
            macd_score = 1

        elif macd_line.iloc[-1] < signal_line.iloc[-1]:
            macd_score = -1

        else:
            macd_score = 0

        # Combine weighted scores into a single trend score
        # Weights chosen heuristically; can be tuned based on performance
        self.trend_score = sma_diff.iloc[-1] * 0.25 + ema_diff.iloc[-1] * \
            0.25 + rsi_score * 0.2 + bb_score * 0.2 + macd_score * 0.2

    def prediction(self):
        """
        Generate predicted future prices based on the trend score.

        Steps:
        1. Copy original data to avoid overwriting.
        2. Calculate rolling 30-day standard deviation to scale predictions.
        3. Iteratively predict 'timeframe' future days:
           - Compute trend score using retreive_data().
           - Adjust last closing price using trend_score * scaled std.
           - Append new predicted price as a new row with the next business day index.
        """

        # copy data to avoid modifying original dataframe
        self.data_pred = self.data.copy()

        std = self.data_pred['Close'].rolling(window=30).std()
        std_val = min(std.iloc[-1], 10)

        # predict the first 100 days for simplicity and as placeholder

        for i in range(self.timeframe):

            self.retreive_data()

            next_close = self.data_pred['Close'].iloc[-1] + \
                self.trend_score * std_val * 0.1

            next_date = pd.bdate_range(
                start=self.data_pred.index[-1], periods=2)[1]

            # Create a new row as a DataFrame
            new_row = pd.DataFrame({'Close': [next_close]},  index=[next_date])

            # Concatenate the new row
            # https://pandas.pydata.org/docs/reference/api/pandas.concat.html
            self.data_pred = pd.concat([self.data_pred, new_row])
