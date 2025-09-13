import yfinance as yf



def fetch_stock_data(ticker_symbol, period):
    """Fetch historical stock data for a given ticker symbol and period."""


    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period)
   
    return data

def fetch_large_data(ticker_symbol, start_date, end_date):
    """Fetch historical stock data for a given ticker symbol between start and end dates."""

    
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    
    return data