"""
Defines the base verdict structure used across technical analysis components.
Provides shared logic, interfaces, and utilities for generating consistent
verdict outputs from various indicator-specific evaluators.
"""

from indicators_verdict.ma_verdict import ma_verdict
from indicators_verdict.rsi_verdict import rsi_verdict
from indicators_verdict.macd_verdict import macd_verdict
from indicators_verdict.bollinger_verdict import bollinger_verdict


class Verdict:
    """
    Aggregates multiple technical indicators into a single trading verdict.

    Each indicator contributes to a "buyer score", which is then mapped to a final
    recommendation: 'Strong Buy', 'Buy', 'Hold', 'Sell', or 'Strong Sell'.

    Indicators considered:
    ----------------------
    - SMA & EMA: Momentum and relative price position (max 3 points each)
    - Moving Average Crossovers: Golden/Death crosses (±5 points)
    - RSI: Overbought/oversold signals (max 3 points)
    - MACD: Movement, relative position, and crossovers (1-5 points)
    - Bollinger Bands: Bullish/bearish signal (max 3 points)
    - ATR: Adjusts score based on volatility (multiplier)

    Parameters
    ----------
    data : pd.DataFrame
        Historical stock data containing 'Close' prices.
    sma_long, sma_short : pd.Series
        Long-term and short-term SMA values.
    ema_Long, ema_short : pd.Series
        Long-term and short-term EMA values.
    rsi : pd.Series
        Relative Strength Index values.
    signal_line, macd_line : pd.Series
        MACD lines used for MACD-based scoring.
    lower_band, upper_band : pd.Series
        Bollinger Bands for bullish/bearish assessment.
    atr : float
        Average True Range used to adjust score for volatility.
    """

    def __init__(self, data, sma_long, sma_short, ema_Long, ema_short, rsi, signal_line, macd_line, lower_band, upper_band, atr):
        """Initialize Verdict with all relevant indicators and calculate buyer score."""
        # Store the latest values of the indicators
        self.price = data['Close'].iloc[-1]

        self.sma_short = sma_short
        self.sma_long = sma_long
        self.buyer_score = 0

        # sma verdict contribution
        ma_verdict_sma = ma_verdict(
            self.price, self.sma_short, self.sma_long)
        self.buyer_score += ma_verdict_sma.buyer_score

        # ema verdict contribution
        ma_verdict_ema = ma_verdict(
            self.price, ema_short, ema_Long)
        self.buyer_score += ma_verdict_ema.buyer_score

        # rsi verdict contribution
        rsi_verdict_instance = rsi_verdict(rsi)
        self.buyer_score += rsi_verdict_instance.buyer_score

        # macd verdict contribution
        macd_verdict_instance = macd_verdict(macd_line, signal_line)
        self.buyer_score += macd_verdict_instance.buyer_score

        # bollinger bands contribution
        bollinger_verdict_instance = bollinger_verdict(
            self.price, lower_band, upper_band, sma_long)
        self.buyer_score += bollinger_verdict_instance.buyer_score

        # adjust score based on volatility
        if atr > 70:
            self.buyer_score *= 0.8
        elif atr < 30:
            self.buyer_score *= 1.2
        else:
            pass

        self.verdict = self.get_verdict()

    def get_verdict(self):
        """
        Convert the aggregated buyer score into a discrete trading recommendation.

        Returns
        -------
        str
            One of 'Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'.
        """

        if self.buyer_score >= 18:
            return "Strong Buy"
        elif self.buyer_score <= -18:
            return "Strong Sell"
        elif 10 <= self.buyer_score < 18:
            return "Buy"
        elif -18 < self.buyer_score <= -10:
            return "Sell"
        else:
            return "Hold"
