import yfinance as yf

# https://algotrading101.com/learn/yahoo-finance-api-guide/


class stock_data:
    """
    Handles fetching of historical stock data from Yahoo Finance.

    Methods allow fetching data for single tickers or multiple tickers, 
    either for a set period (e.g., last 6 months) or a custom date range.
    """

    def __init__(self):
        pass

    @staticmethod
    def fetch_stock_data(ticker_symbol: str, period: str, interval: str):
        """
        Fetch historical stock data for a single ticker over a given period.

        Parameters
        ----------
        ticker_symbol : str
            Stock symbol (e.g., 'AAPL').
        period : str
            Time period to fetch (e.g., '6mo', '1y').
        interval : str
            Data interval (e.g., '1d', '1h').

        Returns
        -------
        pd.DataFrame or None
            DataFrame with columns ['Close', 'Open', 'High', 'Low'].
            Returns None if the ticker does not exist or fetching fails.
        """

        # search for ticker in yahoo and get all the data connected to that ticker
        try:

            ticker = yf.Ticker(ticker_symbol)
            data = ticker.history(period=period, interval=interval)

            return data[['Close', 'Open', 'High', 'Low']]

        except Exception as e:
            # fails if ticker is not existent and give me debugging options
            print(f"{e}")
            return None

    @staticmethod
    def fetch_stock_data_set_dates(ticker_symbol: str, start, end):
        """
        Fetch historical stock data for a single ticker within a custom date range.

        Useful for historical analyses or quarterly heatmaps.

        Parameters
        ----------
        ticker_symbol : str
            Stock symbol.
        start : str or datetime
            Start date of the data.
        end : str or datetime
            End date of the data.

        Returns
        -------
        pd.DataFrame or None
            DataFrame with all available OHLC data.
        """

        try:
            ticker = yf.Ticker(ticker_symbol)
            data = ticker.history(start=start, end=end)

            return data

        except Exception as e:
            print(f"{e}")
            return None

    @staticmethod
    def fetch_multiple_stocks_data(ticker_symbols, period: str, interval: str):
        """
        Fetch historical stock data for multiple tickers over a given period.

        Ideal for heatmaps or analyses requiring many tickers at once.
        Using yfinance's batch download is much faster than looping over tickers individually.

        Parameters
        ----------
        ticker_symbols : list
            List of ticker symbols.
        period : str
            Time period to fetch (e.g., '6mo').
        interval : str
            Data interval (e.g., '1d').

        Returns
        -------
        pd.DataFrame
            Multi-index DataFrame with tickers as top-level columns.
        """

        # get data for multiple tickers, way way way faster than looping through them one by one
        tickers = yf.download(ticker_symbols, period=period, interval=interval,
                              group_by='ticker', threads=True, auto_adjust=True, progress=False)

        return tickers

    @staticmethod
    def fetch_multiple_stocks_data_set_dates(ticker_symbols, start, end):
        """
        Fetch historical stock data for multiple tickers within a custom date range.

        Useful for database operations or historical heatmaps for specific quarters.

        Parameters
        ----------
        ticker_symbols : list
            List of ticker symbols.
        start : str or datetime
            Start date of the data.
        end : str or datetime
            End date of the data.

        Returns
        -------
        pd.DataFrame
            Multi-index DataFrame with tickers as top-level columns.
        """
        tickers = yf.download(ticker_symbols, start=start, end=end,
                              group_by='ticker', threads=True, auto_adjust=True, progress=False)

        return tickers
