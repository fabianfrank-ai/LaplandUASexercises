"""
Generates a verdict based on Relative Strength Index (RSI) values.
Provides utilities for interpreting RSI signals and producing a final decision.
"""


class rsi_verdict:
    """
    Produces a market verdict score using RSI analysis.

    This class interprets the RSI value according to standard thresholds:
    - RSI > 70: overbought → bearish signal
    - RSI < 30: oversold → bullish signal
    - Intermediate values produce milder signals.
    """

    def __init__(self, rsi_value):
        """
        Initialize RSI verdict with the latest RSI value.

        Parameters
        ----------
        rsi_value : pd.Series
            Series of RSI values; the last value is used.
        """

        self.rsi_value = rsi_value.iloc[-1]
        self.buyer_score = self.calculate_verdict()

    def calculate_verdict(self):
        """
        Calculate the buyer score based on the latest RSI value.

        Logic:
        - RSI > 70 → strong bearish (-3)
        - 50 < RSI ≤ 70 → mild bearish (-1)
        - 30 ≤ RSI ≤ 50 → mild bullish (+1)
        - RSI < 30 → strong bullish (+3)

        Returns
        -------
        int
            Buyer score based on RSI thresholds.
        """

        if self.rsi_value > 70:
            return -3
        elif 50 < self.rsi_value <= 70:
            return -1
        elif 30 <= self.rsi_value <= 50:
            return 1
        elif self.rsi_value < 30:
            return 3
