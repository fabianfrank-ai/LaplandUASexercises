''''
The market screener takes tickers, either from input or wikipedia html and uses indicators, pandas 
and more in order to create dataframes for for example Heatmaps or correlation dataframes for 
network Graphing

'''
import pandas as pd
import numpy as np
import urllib.request
from data.fetch_data import stock_data
from core.indicators import Indicators
from core.verdict import Verdict


class get_data:
    """
    Fetch and organize S&P 500 stock data.

    This class provides methods to:
    - Get a list of current S&P 500 tickers from Wikipedia.
    - Fetch historical stock data for multiple tickers efficiently 
      and return it as a dictionary of DataFrames.
    """

    def get_tickers() -> list[str]:
        """
        Retrieve the list of S&P 500 tickers from Wikipedia.

        Returns
        -------
        list[str]
            A list of stock symbols for all companies currently in the S&P 500.
            Tickers are formatted for use with yfinance (dots replaced by dashes).

        Notes
        -----
        - Wikipedia often changes its tables, so this method scans all tables for a 'Symbol' column.
        - Converts tickers like 'BRK.B' to 'BRK-B' for compatibility with yfinance.
        """

        # Get the list of S&P 500 companies from Wikipedia
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        tables = pd.read_html(html)

        # more robust way because Wikipedia loves changing their site, checks all tables
        for table in tables:
            try:
                sp500_tickers = table["Symbol"].tolist()
            except Exception:
                pass

        # wikipedia uses dots in some ticker symbols, but yfinance needs dashes (e.g. BF.B -> BF-B)
        sp500_tickers = [t.replace(".", "-") for t in sp500_tickers]

        return sp500_tickers

    def get_dataframe(tickers: list[str], start, end) -> dict[str, pd.DataFrame]:
        """
        Fetch historical stock data for multiple tickers and organize it into a dictionary.

        Parameters
        ----------
        tickers : list[str]
            List of stock symbols (e.g., from get_tickers()).
        start : datetime or None
            Optional start date for historical data. If None, uses a default period.
        end : datetime or None
            Optional end date for historical data. Ignored if start is None.

        Returns
        -------
        dict[str, pd.DataFrame]
            Dictionary where each key is a ticker symbol and each value is a DataFrame
            with historical stock data for that ticker.

        Notes
        -----
        - Fetching all tickers at once is significantly faster than looping over tickers individually.
        - This method handles different fetching strategies depending on whether start/end dates are provided.
        """

        if start is None and end is None:
            # fetch data for all tickers at once to improve performance
            ticker_dataframe = stock_data.fetch_multiple_stocks_data(
                tickers, period="6mo", interval='1d')

        else:
            # fetch data for all tickers at once to improve performance
            ticker_dataframe = stock_data.fetch_multiple_stocks_data_set_dates(
                tickers, start, end)

        # Build a dictionary of Dataframes for each Ticker
        dfs = {
            ticker: ticker_dataframe[ticker] for ticker in tickers if ticker in ticker_dataframe.columns.get_level_values(0)
        }

        return dfs


class Heatmaps:
    """
        Generate heatmaps and related data analyses for S&P 500 or portfolio tickers.

        This class provides methods to calculate performance metrics, technical indicators,
        and generate heatmaps for visual analysis of stocks.

        Methods
        -------
        heatmap(start=None, end=None)
            Compute indicators and metrics for all S&P 500 tickers and return a DataFrame.
        heatmap_portfolio(portfolio_dataframe)
            Compute indicators and metrics for a specific portfolio of tickers.
        """

    def heatmap(start, end) -> pd.DataFrame:
        """
            Generate a DataFrame with key performance indicators for S&P 500 companies.

            Parameters
            ----------
            start : datetime or None
                Optional start date for historical data. If None, uses all available data.
            end : datetime or None
                Optional end date for historical data. If None, uses latest available date.

            Returns
            -------
            pd.DataFrame
                DataFrame containing the following columns for each ticker:
                - 'Ticker': str, stock symbol
                - 'Change': float, percentage gain/loss over the period
                - 'SMA Diff': float, difference between short and long simple moving averages (%)
                - 'Bollinger %': float, position within Bollinger Bands
                - 'RSI': float, relative strength index
                - 'EMA Diff': float, difference between short and long exponential moving averages (%)
                - 'MACD Diff': float, difference between MACD line and signal line
                - 'Verdict': str, trading signal or rating
                - 'Risk': float, ATR (average true range) as a measure of volatility

            Notes
            -----
            - Handles missing or insufficient data by skipping tickers.
            - Exceptions during indicator calculation are caught and logged.
        """

        # create an empty list, to append the rows as dict into a dataframe later
        rows = []

        sp500_tickers = get_data.get_tickers()
        dfs = get_data.get_dataframe(sp500_tickers, start, end)

        # for every ticker in sp500(whatever is in the dataframe)
        for ticker in list(dfs.keys()):
            data = dfs[ticker]

            try:

                # fetch data, depending on whether start and end dates are provided (for database or not)
                if start is None and end is None:
                    # initialize indicators
                    indicators = Indicators(data)

                    window_long = 100
                    window_short = 30

                    latest_close = data['Close'].iloc[-1]
                    previous_close = data['Close'].iloc[-2]
                    latest_change = (
                        (latest_close - previous_close) / previous_close) * 100
                    latest_change = round(latest_change, 2)

                else:
                    # initialise indicators with the fetched data
                    indicators = Indicators(data)

                    # adjust the window ranges because a quarter doesn't have as many possible dates to get data from
                    window_long = 50
                    window_short = 20

                    # calculate the change from the first to the last available data point, for more meaningful results
                    latest_close = data['Close'].iloc[-1]
                    previous_close = data['Close'].iloc[0]
                    latest_change = indicators.price_change()
                    latest_change = round(latest_change, 2)

                # check if data is valid
                if data is None or len(data) < 2:
                    print(f"Not enough data for {ticker}")
                    continue

                # calculate the indicators and round them, so they can be added to the dataframe later on
                sma_percentage = (
                    indicators.sma(window_short).iloc[-1] - indicators.sma(window_long).iloc[-1]) / indicators.sma(window_long).iloc[-1] * 100
                ema_percentage = (
                    indicators.ema(12).iloc[-1] - indicators.ema(26).iloc[-1]) / indicators.ema(26).iloc[-1] * 100
                ema_percentage = round(ema_percentage, 2)
                sma_percentage = round(sma_percentage, 2)

                macd_line, signal_line = indicators.macd()
                macd_difference = macd_line.iloc[-1] - signal_line.iloc[-1]
                macd_difference = round(macd_difference, 2)

                lower_band, upper_band = indicators.bollinger_bands()
                bollinger_percentage = (
                    data['Close'].iloc[-1] - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])
                bollinger_percentage = round(bollinger_percentage, 2)

                rsi_value = indicators.rsi().iloc[-1]

                rsi_value = round(rsi_value, 2)

                atr_value = indicators.atr()
                atr_value = round(atr_value, 2)

                # generate and append the verdict for the ticker
                verdict = Verdict(data, indicators.sma(window_long), indicators.sma(window_short),
                                  indicators.ema(26), indicators.ema(12), indicators.rsi(), signal_line, macd_line, lower_band, upper_band, atr_value)
                verdict = verdict.verdict

                rows.append({
                    'Ticker': ticker,
                    'Change': latest_change,
                    'SMA Diff': sma_percentage,
                    'Bollinger %': bollinger_percentage,
                    'RSI': rsi_value,
                    'EMA Diff': ema_percentage,
                    'MACD Diff': macd_difference,
                    'Verdict': verdict,
                    'Risk': atr_value
                })

            # Print any errors and continue with the next ticker
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue

            # create a dataframe from the lists
            df = pd.DataFrame(rows)

    # return the dataframe
        return df

    def heatmap_portfolio(portfolio: pd.DataFrame) -> pd.Dataframe:
        """
        Generate a DataFrame of a custom portfolio of tickers with technical indicators.

        Parameters
        ----------
        portfolio_dataframe: A dataframe with all of the tickers entered by the user

        Returns
        -------
        pd.DataFrame
            DataFrame structured like `heatmap`, but only for the selected tickers.

        Notes
        -----
        - Useful for users who want to analyze a subset of the market.
        - Calculation logic is identical to `heatmap`, but limited to the portfolio.
        """

        # create empty lists to store the data, lists are then used to create a dataframe at the end
        rows = []

        # filter all the tickers from the table on wikipedia
        portfolio = portfolio['Ticker'].to_list()

        # for every ticker in sp500
        for ticker in portfolio:
            try:

                # fetch data
                data = stock_data.fetch_stock_data(ticker, "6mo", '1d')
                indicators = Indicators(data)

                # check if data is valid
                if data is None or len(data) < 2:
                    print(f"Not enough data for {ticker}")
                    continue

                # calculate the percentage change from the previous close to the latest close
                latest_close = data['Close'].iloc[-1]
                previous_close = data['Close'].iloc[-2]
                latest_change = (
                    (latest_close - previous_close) / previous_close) * 100

                ema_percentage = (
                    indicators.ema(12).iloc[-1] - indicators.ema(26).iloc[-1]) / indicators.ema(26).iloc[-1] * 100
                sma_percentage = (
                    indicators.sma(30).iloc[-1] - indicators.sma(100).iloc[-1]) / indicators.sma(100).iloc[-1] * 100

                macd_line, signal_line = indicators.macd()
                macd_difference = macd_line.iloc[-1] - signal_line.iloc[-1]

                # calculate indicators for the ticker
                lower_band, upper_band = indicators.bollinger_bands()
                bollinger_percentage = (
                    data['Close'].iloc[-1] - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])

                macd_line, signal_line = indicators.macd()

                rsi_value = indicators.rsi().iloc[-1]
                rsi_value = round(rsi_value, 2)

                atr_value = indicators.atr()

                # generate and append the verdict for the ticker
                verdict = Verdict(data, indicators.sma(100), indicators.sma(30),
                                  indicators.ema(26), indicators.ema(12), indicators.rsi(14), signal_line, macd_line, lower_band, upper_band, indicators.atr())
                verdict = verdict.verdict

                # aooend the values to the lists, later to be added to the dataframe
                rows.append({
                    'Ticker': ticker,
                    'Change': latest_change,
                    'SMA Diff': sma_percentage,
                    'Bollinger %': bollinger_percentage,
                    'RSI': rsi_value,
                    'EMA Diff': ema_percentage,
                    'MACD Diff': macd_difference,
                    'Verdict': verdict,
                    'Risk': atr_value
                })

            # Print any errors and continue with the next ticker
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue

            # create a dataframe from the lists
            df = pd.DataFrame(rows)

    # return the dataframe
        return df


def correlations(start, end) -> pd.DataFrame:
    """
    Calculate pairwise correlations of S&P 500 stock movements over a given timeframe.

    This function computes the percentage daily changes for each ticker and returns
    a correlation matrix of these changes. It can either use the last 6 months of
    data (default) or a user-specified start and end date.

    Parameters
    ----------
    start : datetime or None
        Optional start date for the data. If None, defaults to last 6 months.
    end : datetime or None
        Optional end date for the data. Ignored if start is None.

    Returns
    -------
    pd.DataFrame
        A square DataFrame where both rows and columns are tickers and each value
        represents the Pearson correlation coefficient between the daily changes
        of the two tickers.

    Notes
    -----
    - Handles tickers with missing or insufficient data by skipping them.
    - Aligns tickers with different lengths by padding with NaN where necessary.
    - Exceptions for individual tickers are logged but do not stop processing.
    """

    dfs = get_data.get_tickers()

    data_dictionary = {}

    # Loop over each ticker in the S&P 500 to claculate daily changes
    for ticker in list(dfs.keys()):
        try:

            # fetch data
            if start is None and end is None:
                data = dfs[ticker]
            else:
                data = stock_data.fetch_stock_data_set_dates(
                    ticker, start, end)

            changes = []

            # Compute the percentage change from the previous close to the current close
            # This represents daily stock movement in %
            for i in range(len(data['Close']) - 1):
                latest_close = data['Close'].iloc[i + 1]
                previous_close = data['Close'].iloc[i]
                latest_change = (
                    (latest_close - previous_close) / previous_close) * 100

                changes.append(latest_change)

            if changes:
                data_dictionary[ticker] = changes

        # Print any errors and continue with the next ticker
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    if data_dictionary:
     # Some tickers may have shorter time series due to IPOs or missing data
     # Pad with NaN to align all series before computing correlations

        try:
            df = pd.DataFrame(data_dictionary)

        except Exception as e:

            # Fallback if lengths do not allign
            max_length = max(len(v) for v in data_dictionary.values())

            padded_dict = {}

            for ticker, changes in data_dictionary.items():
                current_length = len(changes)

                if current_length < max_length:

                    # fill with nAn
                    padded_changes = changes + \
                        [np.nan] * (max_length - current_length)
                    padded_dict[ticker] = padded_changes

                else:
                    padded_dict[ticker] = changes

            df = pd.DataFrame(padded_dict)

    # Compute the Pearson correlation matrix of daily changes
    df_correlation = df.corr()


# return the dataframe
    return df_correlation
