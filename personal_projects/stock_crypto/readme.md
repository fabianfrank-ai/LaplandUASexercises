## Stock market analyser : LIVE DEMO: https://mainpy-vyjpplzax43gsxoeteg3dg.streamlit.app

# How does it work?
It fetches data from yfinance(yahoo finance), uses simple indication techniques like sma, rsi and bollinger bands. The user can see all 5 indicators in a chart on a web app, created with streamlit. The user can search for stocks with tickers and manually change the desired length of the development. The user can also see the rsi line in a seperate axis. Not only can the user use those indications with explanations given by the program, the program also creates a verdict over the state of a desired stock(buy,sell,hold) based on the 5 indicators.

The project is still under construction and still lacks finetuning, this is only a broad framework.

# Explanation for all the files:
Main.py - Framework for streamlit, also works as a bridge between the user and all programs listed below

Database.py - is not used due to inconvenience, might be added in the future. It creates databases and saves desired data

Fetch_data.py - fetches data from yfinance , integral part for the incoming data

indicators.py - uses common indicators(SMA,RSI,MACD etc) used in economics to evaluate stocks and give a verdict on whether to buy, hold or sell

market_screener.py - screens the market for the S&P 500 stocks to create the heatmap or give verdicts to main

verdict.py - Uses SMA, RSI, MACD, EMA and Bollinger and checks for certain thresholds that indicate a good or bad stock to buy
