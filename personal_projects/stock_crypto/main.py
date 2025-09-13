import yfinance as yf  #suggested by chatgpt
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
from fetch_data import fetch_stock_data
from indicators import sma, crossing, bollinger_bands, rsi
from verdict import generate_verdict


#change the style of the plot to dark mode (Hex colors used from ChatGPT, I don't like the default dark mode by matplotlib)
plt.rcParams.update({
    "figure.facecolor": "#2e2e2e",  
    "axes.facecolor":   "#2e2e2e",
    "axes.edgecolor":   "#cccccc",   
    "axes.labelcolor":  "#ffffff",  
    "xtick.color":      "#dddddd",  
    "ytick.color":      "#dddddd",
    "grid.color":       "#555555",   
    "text.color":       "#ffffff",   
    "figure.edgecolor": "#2e2e2e"
})


#Streamlit app layout

st.title ('Stock Price Viewer')
st.write('This app fetches and displays historical stock price data using yfinance and Streamlit.')


with st.sidebar:
    with st.sidebar.expander('About this app'):
        st.write('This app was created by Fabian Frank. It uses yfinance to fetch stock data and Streamlit for the web interface. You can view stock prices along with technical indicators like Simple Moving Averages (SMA) and Bollinger Bands.')
        st.write('Feel free to explore and modify the code for your own projects!')
        st.write('DISCLAIMER: This app is for educational purposes only and should not be used for real trading decisions. Always do your own research and consult with a financial advisor before making investment decisions.')
    with st.sidebar.expander('What are SMAs and Bollinger Bands?'):
        st.write('Simple Moving Averages (SMA) are used to smooth out price data and identify trends by averaging closing prices over a specified period. For example, a 30-day SMA averages the closing prices of the last 30 days.')
        st.write('Bollinger Bands consist of a middle band (SMA), an upper band, and a lower band. The upper band is typically 2 standard deviations above the SMA, and the lower band is 2 standard deviations below the SMA. They help identify overbought or oversold conditions in the market.')
    with st.sidebar.expander('Instructions'):
        st.write('1. Select the stock ticker symbol (e.g., AMZN, MSFT, META) in the input box.')
        st.write('2. Use the slider to choose the period (in years) for which you want to fetch historical data. Note: indicatiors like SMA and Bollinger Bands are more visiblie with smaller periods')
        st.write('3. The app will display the stock price along with the 30-day and 100-day SMAs and Bollinger Bands on the chart.')
    with st.sidebar.expander('What are Stock Tickers and where can I find them ?'):
        st.write('You can find stock ticker symbols on financial websites like Yahoo Finance, Google Finance, or your brokerage platform. Common examples include AAPL for Apple, MSFT for Microsoft, and AMZN for Amazon.')
    with st.sidebar.expander('Hot contenders'):
        st.write("Here are all buy suggestions from the S&P 500 by the program! ")
        st.write("Remember to do your own research before investing in any stock!")
    with st.sidebar.expander('Future Improvements'):
        st.write('- Add more technical indicators like RSI, MACD, etc.')
        st.write('- Implement user authentication for saving preferences.')
        st.write('- Add news sentiment analysis related to the selected stock.')
        st.write('Crypto data integration (e.g., Bitcoin, Ethereum).')
    with st.sidebar.expander('How does the verdict work?'):
        st.write('The verdict is generated based on three technical indicators: Simple Moving Averages (SMA), Bollinger Bands, and Relative Strength Index (RSI).')
        st.write('The rules for generating the verdict are as follows:')
        st.write('- If 2 or more indicators suggest a "Buy" signal, the verdict is "Buy".')
        st.write('- If 2 or more indicators suggest a "Sell" signal, the verdict is "Sell".')
        st.write('- If only 1 indicator suggests a "Buy" or "Sell" signal, the verdict is "Hold".')
        st.write('- If none of the indicators suggest a "Buy" or "Sell" signal, the verdict is "Hold".')
        st.write('Note: This is a simplified approach for educational purposes and should not be used for real trading decisions.')
    with st.sidebar.expander('Contact'):
        st.write('For any questions or suggestions, feel free to reach out to me on:')
        st.write('- [GitHub](fabianfrank-ai)')
        st.write('- email: frankfabian945@outlook.de')
        st.write('- Discord: tntgurke94')
        
    

#create a matplotlib figure and axis
fig ,(ax,ax2)=plt.subplots(2,1, figsize=(16,20), sharex=True)


#name the axes and add a grid
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)') 
ax.grid()
ax2.grid()
ax2.set_ylabel('RSI')


#user inputs for stock ticker and period as streamlit widgets
period=st.slider('Select Period', min_value=1, max_value=20, value=10, help='Select the number of years to fetch data for (1-20 years)')
stock=st.text_input('Select Stock ticker (AMZN, MSFT, META)',  help='Select the stock symbol to fetch data for', value='AMZN')

#fetch the stock data
data=fetch_stock_data(stock, f'{period}y')
data_sma_30=sma(data, 30)
data_sma_100=sma(data, 100)


lower_band, upper_band= bollinger_bands(data, 30)
rsi=rsi(data, 14)

verdict=generate_verdict(data, data_sma_30, data_sma_100, lower_band, upper_band, rsi)

#calculate the crosses between the two SMAs
#crossings=crossing(data_sma_30, data_sma_100)

#get x and y values for the crossings
#x_intersections, y_intersections = zip(*crossings)

#plot/scatter the data
ax.plot(data.index, data['Close'], label='Close Price', color='#4deeea')
ax.plot(data_sma_100.index, data_sma_100, label='100 Day SMA', color='#f000ff',linestyle='dashdot', alpha=0.7)
ax.plot(data_sma_30.index, data_sma_30, label='30 Day SMA', color="#ffc800", linestyle='dashdot', alpha=0.7)
ax.plot(upper_band.index, upper_band, label='Upper Bollinger Band', color='limegreen', linestyle='--', alpha=0.5)
ax.plot(lower_band.index, lower_band, label='Lower Bollinger Band', color='red', linestyle='--', alpha=0.5)
ax2.plot(rsi.index, rsi, label='14 Day RSI', color='#ffa500')
ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
ax2.axhline(30, color='limegreen', linestyle='--', alpha=0.5)
ax2.set_ylim(0, 100)
ax2.fill_between(rsi.index, rsi, 70, where=(rsi >= 70), color='red', alpha=0.3)
ax2.fill_between(rsi.index, rsi, 30, where=(rsi <= 30), color='limegreen', alpha=0.3)
#ax.scatter(x_intersections, y_intersections, label='Crossings', color='#ff0000', marker='x',zorder=5)


#add a title and legend
ax.set_title(f'{stock} Stock Price between {data.index[0].date()} and {data.index[-1].date()}')
ax.legend()

if verdict=="Buy":
    st.success(f'Verdict: {verdict}. According to the indicators, it might be a good time to buy {stock}.')
elif verdict=="Sell":
    st.error(f'Verdict: {verdict}. According to the indicators, it might be a good time to sell {stock}.')
else:
    st.warning(f'Verdict: {verdict}. According to the indicators, it might be best to hold {stock} for now.')


st.pyplot(fig)