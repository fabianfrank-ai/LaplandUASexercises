import streamlit as st
import matplotlib.pyplot as plt
from fetch_data import fetch_stock_data
from indicators import sma,  bollinger_bands, rsi, price_change, ema, macd , moving_average_crossover, atr
from verdict import generate_verdict
from market_screener import market_screener, heatmap
from colour_coding import color_code, verdict_color, rsi_color, ema_color, macd_color, sma_color, bollinger_color, atr_color



# change the style of the plot to dark mode (Hex colors used from ChatGPT, I don't like the default dark mode by matplotlib)
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



# Streamlit app layout with title and description
st.title ('Stock Price Viewer')
st.write('This app fetches and displays historical stock price data using yfinance and Streamlit.')



# create a sidebar with useful texts and information and some instructions
with st.sidebar:
   
    with st.sidebar.expander('About this app'):
   
        st.write('This app was created by Fabian Frank. It uses yfinance to fetch stock data and Streamlit for the web interface. You can view stock prices along with technical indicators like Simple Moving Averages (SMA) and Bollinger Bands.')
        st.write('Feel free to explore and modify the code for your own projects!')
        st.write('DISCLAIMER: This app is for educational purposes only and should not be used for real trading decisions. Always do your own research and consult with a financial advisor before making investment decisions.')
  
    with st.sidebar.expander('SMA? Bollinger Bands? RSI? MACD? EMA?'):
  
        st.write('Simple Moving Averages (SMA) smooth out price data to identify trends. The 30-day SMA reacts faster to price changes than the 100-day SMA.')
        st.write('Bollinger Bands consist of a middle band (SMA), an upper band, and a lower band. Prices near the upper band may indicate overbought conditions, while prices near the lower band may indicate oversold conditions.')
        st.write('Relative Strength Index (RSI) measures the speed and change of price movements. An RSI above 70 indicates overbought conditions, while an RSI below 30 indicates oversold conditions.')
        st.write('Exponential Moving Average (EMA) gives more weight to recent prices, making it more responsive to new information.')
        st.write('Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.')
        st.write('These indicators help traders make informed decisions about buying or selling stocks.')
  
    with st.sidebar.expander('Instructions'):
   
        st.write('1. Select the stock ticker symbol (e.g., AMZN, MSFT, META) in the input box.')
        st.write('2. Use the slider to choose the period (in years) for which you want to fetch historical data. Note: indicatiors like SMA and Bollinger Bands are more visiblie with smaller periods')
        st.write('3. The app will display the stock price along with the 30-day and 100-day SMAs and Bollinger Bands on the chart.')
        st.write('4. You can select additional technical indicators to display on the chart from the sidebar.')
        st.write('5. The verdict (Buy, Hold, Sell) is generated based on multiple technical indicators and displayed above the chart.')
        st.write('6. You can also run the Signal Searcher to scan the S&P 500 for potential buy opportunities.')
        st.write('7. Click the "Show S&P 500 Heatmap" button to generate a heatmap of S&P 500 companies based on their daily gain/loss percentage.')
   
    with st.sidebar.expander('What are Stock Tickers and where can I find them ?'):
     
        st.write('You can find stock ticker symbols on financial websites like Yahoo Finance, Google Finance, or your brokerage platform. Common examples include AAPL for Apple, MSFT for Microsoft, and AMZN for Amazon.') 
  
    with st.sidebar.expander('How does the verdict work?'):
      
        st.write('The new verdict system still uses the five main indicators: SMA, Bollinger Bands, RSI, EMA and MACD.')
        st.write('However, the strength of the signals has been increased. Now, if an indicator shows a very strong buy/sell signal (e.g., RSI > 80 or < 20), it counts as 3 buy/sell signals instead of just 1. This way, the verdict is more responsive to significant market movements.')
        st.write('If 9 or more buy/sell signals are generated, the verdict will be "Strong Buy" or "Strong Sell". If 3-8 buy/sell signals are generated, the verdict will be "Buy" or "Sell". If only 1-2 buy/sell signals are generated, the verdict will be "Hold". If no buy/sell signals are generated, the verdict will also be "Hold".')
    with st.sidebar.expander('Signal Searcher'):
       
        st.write('The Signal Searcher is a tool that scans the S&P 500 companies to identify potential buy opportunities based on technical indicators. It fetches data for each company, calculates indicators like SMA, Bollinger Bands, and RSI, and generates a verdict (Buy, Sell, Hold) for each stock.')
        st.write('If a stock receives a "Buy" verdict from the indicators, it is highlighted as a potential buy opportunity. This tool helps users discover stocks that may be worth further research and consideration for investment.')
        st.write('Note: The Signal Searcher is for educational purposes only and should not be used for real trading decisions. Always conduct your own research and consult with a financial advisor before making investment decisions.')
       
        if st.button('Run Signal Searcher', help='Click to scan the S&P 500 for potential buy opportunities'):

            result = market_screener()
            if result:
                ticker, verdict = result
                st.success(f'Potential Buy Opportunity Found: {ticker} - Verdict: {verdict}')
            else:
                st.info('No Buy Opportunities Found at this time.')
   
    with st.sidebar.expander('Indicators'):

        options = ['SMA', 'Bollinger Bands', 'EMA', 'MACD', 'RSI']
        selected_indicators = st.multiselect('Select Indicators to Display', options, default=['SMA', 'Bollinger Bands', 'RSI'])
        st.write('You can select which technical indicators to display on the chart. By default, SMA, Bollinger Bands, and RSI are selected.')
    
    with st.sidebar.expander('Future Improvements'):

        st.write('- Add more technical indicators like Volume, Stochastic Oscillator, etc.')
        st.write('- Implement user authentication for saving preferences.')
        st.write('- Allow users to save and compare multiple stocks.')
        st.write('- Integrate real-time data updates for live stock prices.')
        st.write('- Add educational resources about stock trading and technical analysis.')



# create a matplotlib figure and axis, so both axes can share the same x axis
# the first axis will be used for the stock price and the second for the rsi and macd
# the figsize is set to 16:9 ratio, as it is the most common screen ratio
fig ,(ax,ax2) = plt.subplots(2,1, figsize=(16,20), sharex=True)
fig.tight_layout(pad=5.0)



# name the axes and add a grid
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)') 
ax.grid()
ax2.grid()
ax2.set_ylabel('RSI')



# user inputs for stock ticker and period as streamlit widgets
period = st.slider('Select Period', min_value=1, max_value=20, value=10, help='Select the number of years to fetch data for (1-20 years)')
stock = st.text_input('Select Stock ticker (AMZN, MSFT, META)',  help='Select the stock symbol to fetch data for', value='AMZN')



# fetch the stock data
data = fetch_stock_data(stock, f'{period}y')


# handle errors in case the stock ticker is invalid
if data is None or data.empty:
    st.error('Error fetching data. Please check the stock ticker symbol and try again.')
    st.stop()


# create the smas, ema, macd and other indicators
data_sma_30 = sma(data, 30) 
data_sma_100 = sma(data, 100)


ema_12 = ema(data, 12)
ema_26 = ema(data, 26)


macd_line, signal_line = macd(data)


# create the bollinger bands and rsi
lower_band, upper_band = bollinger_bands(data, 30)
rsi = rsi(data, 14)



# create a verdict for the data(buy/hold/sell)
verdict = generate_verdict(data, data_sma_30, data_sma_100, lower_band, upper_band, rsi)

crossover_type_sma = moving_average_crossover(data, data_sma_30, data_sma_100)
crossover_data_sma = crossover_type_sma.index 

crossover_type_ema = moving_average_crossover(data, ema_12, ema_26)
crossover_data_ema = crossover_type_ema.index

# calculate the price change percentage over the selected period
price_change = price_change(data)


atr = atr(data)




if st.button('Show S&P 500 Heatmap', help='Click to generate a heatmap of S&P 500 companies based on their gain/loss percentage over the last day'):
   
    with st.spinner('Generating heatmap... This may take a moment.'):
        heatmap_data = heatmap()
    st.write('S&P 500 Daily Change Percentage:')
    st.dataframe(heatmap_data.style
                 .map(color_code, subset=['Change'])
                 .map(verdict_color, subset=['Verdict'])
                 .map(sma_color, subset=['SMA Diff'])
                 .map(rsi_color, subset=['RSI'])
                 .map(bollinger_color, subset=['Bollinger %']) 
                 .map(ema_color, subset=['EMA Diff'])
                 .map(macd_color, subset=['MACD Diff'])
                 .map(atr_color, subset=['Risk']))





## plot the data
# check if the price change is positive or negative and change the background color accordingly
if price_change>0:

    # dark green background for positive price change
    ax.set_facecolor('#003f3f')
    ax.plot(data.index, data['Close'], label=f'Close Price \u25B2 {price_change}%', color='white')

else:

    # dark red background for negative price change
    ax.set_facecolor('#3f0000') 
    ax.plot(data.index, data['Close'], label=f'Close Price \u25BC {price_change}%', color='#ff4d4d')




# plot the selected indicators, if any are selected
if 'SMA' in selected_indicators:

    ax.plot(data_sma_100.index, data_sma_100, label='100 Day SMA', color='#f000ff',linestyle='dashdot')
    ax.plot(data_sma_30.index, data_sma_30, label='30 Day SMA', color="#ffc800", linestyle='dashdot')

    if crossover_data_sma is not None:  

        for date, ctype in zip(crossover_data_sma, crossover_type_sma):

            if ctype == 'Golden Cross':
                # there was some trouble with plotting the markers directly on the date, so I had to find the closest date in the data index
                # very hacky but it works

                closest_date = data.index.get_indexer([date], method='nearest')
                ax.plot(data.index[closest_date][0], data.loc[data.index[closest_date][0], 'Close'],
                            marker='^', color='gold', markersize=15 , zorder=5)
                
            elif ctype == 'Death Cross':

                closest_date = data.index.get_indexer([date], method='nearest')
                ax.plot(data.index[closest_date][0], data.loc[data.index[closest_date][0], 'Close'],
                            marker='v', color='black', markersize=15, zorder=5)




if 'Bollinger Bands' in selected_indicators:

    ax.plot(upper_band.index, upper_band, label='Upper Bollinger Band', color='limegreen', linestyle='--')
    ax.plot(lower_band.index, lower_band, label='Lower Bollinger Band', color='red', linestyle='--')




if 'EMA' in selected_indicators:

    ax.plot(ema_12.index, ema_12, label='12 Day EMA', color="#99f5ff", linestyle='dotted')
    ax.plot(ema_26.index, ema_26, label='26 Day EMA', color='#ff00ff', linestyle='dotted')

    if crossover_data_ema is not None:

        for date, ctype in zip(crossover_data_ema, crossover_type_ema):

            if ctype == 'Golden Cross':
                closest_date = data.index.get_indexer([date], method='nearest')
                ax.plot(data.index[closest_date][0], data.loc[data.index[closest_date][0], 'Close'],
                            marker='^', color='cyan', markersize=15)
                
            elif ctype == 'Death Cross':

                closest_date = data.index.get_indexer([date], method='nearest')
                ax.plot(data.index[closest_date][0], data.loc[data.index[closest_date][0], 'Close'],
                            marker='v', color='magenta', markersize=15)
                




if 'MACD' in selected_indicators:
    
    ax2.plot(macd_line.index, macd_line, label='MACD Line', color='#00ff00')
    ax2.plot(signal_line.index, signal_line, label='Signal Line', color='#ff0000')
    ax2.axhline(0, color='grey', linestyle='--')
    ax2.set_ylabel('MACD')




if 'RSI' in selected_indicators:

    ax2.plot(rsi.index, rsi, label='14 Day RSI', color='#ffa500')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='limegreen', linestyle='--')
    ax2.fill_between(rsi.index, rsi, 70, where=(rsi >= 70), color='red', alpha=0.3)
    ax2.fill_between(rsi.index, rsi, 30, where=(rsi <= 30), color='limegreen', alpha=0.3)
    ax2.set_ylabel('RSI')



# add a title and legend
ax.set_title(f'{stock} Stock Price between {data.index[0].date()} and {data.index[-1].date()}')
ax.legend()
ax2.legend()




# Give the user feedback whether to buy,sell or hold a product
if verdict == "Buy":
    st.success(f'Verdict: {verdict}. According to the indicators, it might be a good time to buy {stock}. Look at the sidebar for an explanation!')
elif verdict == "Strong Buy":
    st.success(f'Verdict: {verdict}. According to the indicators, it might be a very good time to buy {stock}. Look at the sidebar for an explanation!')
elif verdict == "Strong Sell":
    st.error(f'Verdict: {verdict}. According to the indicators, it might be a very good time to sell {stock}.')
elif verdict == "Sell":
    st.error(f'Verdict: {verdict}. According to the indicators, it might be a good time to sell {stock}.')
else:
    st.warning(f'Verdict: {verdict}. According to the indicators, it might be best to hold {stock} for now.')


if atr is not None:
    
    if atr > 70:

        st.error(f'Risk (ATR): {atr:.2f}%. The stock seems highly volatile. Investing in it could be a huge rist.')

    elif atr > 40 and atr <= 70:

        st.warning(f'Risk (ATR): {atr:.2f}%. The stock seems volatile. Investing in it could be a risk.')

    elif atr > 20 and atr <= 40:

        st.info(f'Risk (ATR): {atr:.2f}%. The stock seems somewhat volatile. Investing in it could be a moderate risk.')

    else:
        st.success(f'Risk (ATR): {atr:.2f}%. The stock seems not very volatile. Investing in it should be relatively safe.')


# create steamlit plot
st.pyplot(fig)
