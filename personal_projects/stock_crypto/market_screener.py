#this program will screen the maket to find eligible stocks to buy 

import pandas as pd
import urllib.request
from fetch_data import fetch_stock_data
from indicators import sma, bollinger_bands, rsi
from verdict import generate_verdict
from database import insert_buy


def market_screener():
   """Screen the market for potential buy opportunities in S&P 500 companies."""
   #Get the list of S&P 500 companies from Wikipedia
   url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
   req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html = urllib.request.urlopen(req).read()
   tables = pd.read_html(html)


   #filter all the tickers from the table on wikipedia
   sp500_tickers = tables[0]['Symbol'].tolist()


   #for every ticker in sp500
   for ticker in sp500_tickers:


      #try, in order to prevent false tickers in eg wikipedia or conversion errors
      try:
         #fetch data, create smas, bollinger bands and rsi for every ticker
         data = fetch_stock_data(ticker, "5mo")
         sma_30 = sma(data, 30)
         sma_100 = sma(data, 100)
         lower_band, upper_band = bollinger_bands(data, 30)
         rsi_14 = rsi(data, 14)


         #create a verdict for the ticker 
         verdict = generate_verdict(data, sma_30, sma_100, lower_band, upper_band, rsi_14)


         #save the tickers with a buy verdict 
         if verdict == "Buy" :
            return ticker, verdict
         else:
            pass  # No action for "Sell" or "Hold"



      except Exception as e:
         print(f"Error processing {ticker}: {e}")
         continue

