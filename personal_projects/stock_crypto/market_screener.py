#this program will screen the maket to find eligible stocks to buy 

import pandas as pd
import urllib.request
from fetch_data import fetch_stock_data
from indicators import sma, bollinger_bands, rsi
from verdict import generate_verdict
from database import insert_buy

buys=[]

#Get the list of S&P 500 companies from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
tables = pd.read_html(html)
sp500_tickers = tables[0]['Symbol'].tolist()

for ticker in sp500_tickers:
    try:
        data = fetch_stock_data(ticker, "30d")
        sma_30 = sma(data, 30)
        sma_100 = sma(data, 100)
        lower_band, upper_band = bollinger_bands(data, 30)
        rsi_14 = rsi(data, 14)
        verdict = generate_verdict(data, sma_30, sma_100, lower_band, upper_band, rsi_14)
        if verdict == "Buy" :
           insert_buy(data)
           print(f"{ticker}: {verdict}")
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

