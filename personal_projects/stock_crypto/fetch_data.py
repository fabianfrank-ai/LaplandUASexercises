import yfinance as yf



def fetch_stock_data(ticker_symbol, period):
    """Fetch historical stock data for a given ticker symbol and period."""

    #search for ticker in yahoo and get all the data connected to that ticker
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        return None
   
    

def fetch_large_data(ticker_symbol, start_date, end_date):
    """Fetch historical stock data for a given ticker symbol between start and end dates."""

    
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    
    return data