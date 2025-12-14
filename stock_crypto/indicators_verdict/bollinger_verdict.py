"""
Generates verdicts based on Bollinger Bands. Evaluates band touches,
volatility expansion or contraction, and price position within the bands.
"""


class bollinger_verdict:
    """
    Interprets Bollinger Band behavior to produce a market verdict score.

    The score considers:
    - Price position relative to the upper and lower bands
    - Overall market context (bullish or bearish) using the long-term SMA
    - Potential breakout, overbought, or oversold conditions
    """

    def __init__(self, price, lower_band, upper_band, sma_long):
        """
        Initialize the Bollinger Bands verdict.

        Parameters
        ----------
        price : float
            Current closing price of the stock.
        lower_band : pd.Series
            Lower Bollinger Band values.
        upper_band : pd.Series
            Upper Bollinger Band values.
        sma_long : pd.Series
            Long-term SMA used to determine market trend.
        """

        self.price = price
        self.lower_band = lower_band
        self.upper_band = upper_band
        self.sma_long = sma_long

        # calculate the buyer score
        self.buyer_score = self.calculate_buyer_score()

    def calculate_buyer_score(self):
        """
        Calculate the buyer score based on Bollinger Band analysis.

        Logic:
        - Determine the relative position of price between upper and lower bands
          as a percentage (0–100%).
        - If price is above long-term SMA (bullish market):
            - High relative position (>80%) → strong bullish momentum (+3)
            - Moderate position (>20%) → mild bullish signal (+1)
        - If price is below long-term SMA (bearish market):
            - Low relative position (<20%) → strong bearish signal (-3)
            - Moderate position (<80%) → mild bearish signal (-1)

        Returns
        -------
        int
            Buyer score based on Bollinger Band position and market trend.
        """

        buyer_score = 0
        bollinger_percentage = (self.price - self.lower_band.iloc[-1]) / (
            self.upper_band.iloc[-1] - self.lower_band.iloc[-1]) * 100

        if self.price > self.sma_long.iloc[-1]:
            # Price is above long-term SMA -> Bullish context, Higher BB% could indicate breakout
            # if price is below momentum a high BB% could mean overbought
            if bollinger_percentage > 0.8:
                buyer_score += 3
            elif bollinger_percentage > 0.2:
                buyer_score += 1
            else:
                pass

        elif self.price < self.sma_long.iloc[-1]:
            # Price is below long-term SMA -> Bearish context, Lower BB% could indicate breakdown
            # if price is above momentum a low BB% could mean oversold
            if bollinger_percentage < 0.2:
                buyer_score -= 3
            elif bollinger_percentage < 0.8:
                buyer_score -= 1
            else:
                pass
        return buyer_score
