"""
Generates verdicts based on moving averages, supporting both EMA and SMA.
Evaluates trend direction, price relative to averages, and crossover behavior.
"""


class ma_verdict:
    """
    Produces a market verdict score using moving average analysis.

    This class examines:
    - Price relative to short and long moving averages
    - Trend strength and slope of moving averages
    - Crossover events (golden/death crosses)

    The resulting `buyer_score` reflects bullish or bearish momentum.
    """

    def __init__(self, price, ma_short, ma_long):
        """
        Initialize the MA verdict with current price and moving averages.

        Parameters
        ----------
        price : float
            Current closing price.
        ma_short : pd.Series
            Short-term moving average series.
        ma_long : pd.Series
            Long-term moving average series.
        """

        self.ma_short = ma_short
        self.ma_long = ma_long
        self.price = price

        # aggregates scores from different ma-based signals
        buyer_score = 0
        buyer_score = self.difference_verdict()
        buyer_score += self.change_verdict()
        buyer_score += self.crossover_verdict()

        self.buyer_score = buyer_score

    def get_difference(self, price, ma):
        """
        Calculate the percentage difference between a price and a moving average.

        Parameters
        ----------
        price : float
            Current price.
        ma : float
            Moving average value.

        Returns
        -------
        float
            Percentage difference between price and MA.
        """

        return ((price - ma) / ma) * 100

    def difference_verdict(self):
        """
        Generate verdict based on difference between price and moving averages.

        Logic:
        - Large positive difference → strong bullish momentum
        - Large negative difference → strong bearish momentum
        - Different thresholds for short vs. long MA due to volatility differences

        Returns
        -------
        int
            Buyer score contribution from price-MA differences.
        """

        buyer_score = 0
        # Calculate the percentage differences
        short_diff = self.get_difference(self.price, self.ma_long.iloc[-1])

        long_diff = self.get_difference(self.price, self.ma_short.iloc[-1])

        # Determine verdict based on the differences
        if short_diff > 4:
            buyer_score += 2
        elif 2 < short_diff <= 4:
            buyer_score += 1
        elif short_diff < -4:
            buyer_score -= 2
        elif -4 <= short_diff < -2:
            buyer_score -= 1
        else:
            buyer_score += 0

        # use 8 as threshold for long difference because long ma is less volatile
        if long_diff > 8:
            buyer_score += 2
        elif 4 < long_diff <= 8:
            buyer_score += 1
        elif long_diff < -8:
            buyer_score -= 2
        elif -8 <= long_diff < -4:
            buyer_score -= 1
        else:
            buyer_score += 0

        return buyer_score

    def change_verdict(self):
        """
        Generate verdict based on daily change of moving averages.

        Logic:
        - Positive change → small bullish signal
        - Negative change → small bearish signal

        Returns
        -------
        int
            Buyer score contribution from MA trend changes.
        """
        buyer_score = 0
        # Calculate the changes in moving averages
        short_change = self.ma_short.iloc[-1] - self.ma_short.iloc[-2]
        long_change = self.ma_long.iloc[-1] - self.ma_long.iloc[-2]

        # Determine verdict based on the changes
        if short_change > 0:
            buyer_score += 1
        elif short_change < 0:
            buyer_score -= 1

        if long_change > 0:
            buyer_score += 1
        elif long_change < 0:
            buyer_score -= 1

        return buyer_score

    def crossover_verdict(self):
        """
        Generate verdict based on moving average crossovers.

        Logic:
        - Golden cross (short MA crosses above long MA) → strong bullish (+5)
        - Death cross (short MA crosses below long MA) → strong bearish (-5)

        Returns
        -------
        int
            Buyer score contribution from crossover signals.
        """
        buyer_score = 0
        # Check for crossover -> very strong buy/sell signal

        if self.ma_short.iloc[-2] < self.ma_long.iloc[-2] and self.ma_short.iloc[-1] > self.ma_long.iloc[-1]:
            buyer_score += 5
        elif self.ma_short.iloc[-2] > self.ma_long.iloc[-2] and self.ma_short.iloc[-1] < self.ma_long.iloc[-1]:
            buyer_score -= 5

        return buyer_score
