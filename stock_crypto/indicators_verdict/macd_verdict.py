"""
Generates a verdict based on MACD behavior. Evaluates line positions,
momentum shifts, and crossover events to produce a signal.
"""


class macd_verdict:
    """
    Produces a market verdict score using MACD analysis.

    This class examines:
    - MACD line relative to signal line
    - Direction/momentum of MACD and signal lines
    - Recent crossover events (bullish/bearish)

    The resulting `buyer_score` reflects momentum and trend shifts.
    """

    def __init__(self, macd_line, signal_line):
        """
        Initialize MACD verdict with MACD and signal lines.

        Parameters
        ----------
        macd_line : pd.Series
            MACD line values.
        signal_line : pd.Series
            Signal line values.
        """

        self.macd_line = macd_line
        self.signal_line = signal_line
        self.buyer_score = 0

        # Calculate MACD verdict
        self.buyer_score = self.calculate_verdict()
        self.buyer_score += self.movement_verdict()
        self.buyer_score += self.crossover_verdict()

    def calculate_verdict(self):
        """
        Generate verdict based on relative position of MACD line vs. signal line.

        Logic:
        - MACD above signal → bullish (+2)
        - MACD below signal → bearish (-2)

        Returns
        -------
        int
            Buyer score contribution from MACD line position.
        """

        buyer_score = 0

        # Determine verdict based on MACD line and signal line
        if self.macd_line.iloc[-1] > self.signal_line.iloc[-1]:
            buyer_score += 2
        elif self.macd_line.iloc[-1] < self.signal_line.iloc[-1]:
            buyer_score -= 2
        else:
            buyer_score += 0

        return buyer_score

    def movement_verdict(self):
        """
        Generate verdict based on movement (momentum) of MACD and signal lines.

        Logic:
        - Upward movement → small bullish (+1)
        - Downward movement → small bearish (-1)

        Returns
        -------
        int
            Buyer score contribution from MACD momentum.
        """

        buyer_score = 0
        # Calculate the movements
        macd_movement = self.macd_line.iloc[-1] - self.macd_line.iloc[-2]
        signal_movement = self.signal_line.iloc[-1] - self.signal_line.iloc[-2]

        # Determine verdict based on the movements
        if macd_movement > 0:
            buyer_score += 1
        elif macd_movement < 0:
            buyer_score -= 1

        if signal_movement > 0:
            buyer_score += 1
        elif signal_movement < 0:
            buyer_score -= 1

        return buyer_score

    def crossover_verdict(self):
        """
        Generate verdict based on recent MACD crossover events.

        Logic:
        - Golden cross (MACD crosses above signal) → strong bullish (+5)
        - Death cross (MACD crosses below signal) → strong bearish (-5)

        Returns
        -------
        int
            Buyer score contribution from MACD crossover signals.
        """

        buyer_score = 0
        # Check for recent crossover events
        if self.macd_line.iloc[-2] < self.signal_line.iloc[-2] and self.macd_line.iloc[-1] > self.signal_line.iloc[-1]:
            buyer_score += 5
        elif self.macd_line.iloc[-2] > self.signal_line.iloc[-2] and self.macd_line.iloc[-1] < self.signal_line.iloc[-1]:
            buyer_score -= 5

        return buyer_score
