import streamlit as st  # need streamlit for session_state
from data.fetch_data import stock_data
import pandas as pd

# Aliad for session state for convenience
sst = st.session_state

# Initialize empty lists to store portfolio data temporarily
# These lists are used to build the DataFrame
ticker_list = []
amount_list = []
buy_in_list = []
current_price_list = []
change_list = []
invested_overall_list = []
value_now_list = []
overall_profit_list = []


# Initialize session_state DataFrame if it doesn't exist yet
# This ensures the portfolio persists across Streamlit reruns
if 'portfolio_dataframe' not in sst:
    sst.portfolio_dataframe = pd.DataFrame(columns=["Ticker", "Amount", "Buy-In", "Current Price", "Change%",
                                                    "Invested overall", "Value Now", "Overall profit"])


def generate_portfolio(ticker: str, amount: float, buy_in: float) -> pd.DataFrame:
    """
    Add a stock to the user's portfolio and return the updated DataFrame.

    Parameters
    ----------
    ticker : str
        Stock symbol (e.g., 'AAPL').
    amount : float
        Number of shares purchased.
    buy_in : float
        Purchase price per share.

    Returns
    -------
    pd.DataFrame
        Updated portfolio DataFrame stored in Streamlit session_state.

    Notes
    -----
    - Prevents duplicate entries for the same ticker.
    - Calculates current price, price change %, invested amount, current value, and profit.
    - Uses Streamlit session_state to maintain data across reruns.
    """

    # Skip if the ticker is already in the portfolio
    if ticker not in ticker_list:

        # get the most recent price as list (for the index) and as float (as output)
        current_price_index = stock_data.fetch_stock_data(ticker, '1d', '1d')

        # calculate indicators and round if necessary
        # then insert into a list for the datafframe

        current_price = float(current_price_index['Close'].iloc[-1])
        current_price = round(current_price, 2)

        # Calculate percentage change from buy-in price
        price_change = ((current_price - buy_in) / buy_in) * 100
        price_change = round(price_change, 2)

        overall_bought = amount * buy_in
        overall_bought = round(overall_bought, 2)

        # Calculate total invested amount and current portfolio value
        value_now = current_price * amount
        value_now = round(value_now, 2)

        # Calculate profit per stock
        profit_per_stock = value_now - overall_bought
        profit_per_stock = round(profit_per_stock, 2)

        # Append all computed values to the lists
        ticker_list.append(ticker)
        amount_list.append(amount)
        buy_in_list.append(buy_in)
        value_now_list.append(value_now)
        invested_overall_list.append(overall_bought)
        change_list.append(price_change)
        current_price_list.append(current_price)

        overall_profit_list.append(profit_per_stock)

        # create a dataframe that does'nt get deleted
        sst.portfolio_dataframe = pd.DataFrame({'Ticker': ticker_list,
                                                'Amount': amount_list,
                                                'Buy-In': buy_in_list,
                                                'Current Price': current_price_list,
                                                'Change%': change_list,
                                                'Invested overall': invested_overall_list,
                                                'Value Now': value_now_list,
                                                'Overall profit': overall_profit_list})
    else:
        pass

    return sst.portfolio_dataframe
