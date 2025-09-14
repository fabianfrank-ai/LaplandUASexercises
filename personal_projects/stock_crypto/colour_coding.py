#this is mainly used to colour code the dataframe in streamlit

def color_code(val):
    """Color code the dataframe based on the percentage change."""


    # Define color thresholds, bigger changes get darker colors, to emphasize them
    if val > 0 and val <=1:
        color = '#90ee90'  # lightgreen
    elif val > 1 and val <=3:
        color = '#32cd32'  # limegreen
    elif val > 3:
        color = '#008000'  # green
    elif val < 0 and val >= -1:
        color = '#ffcccb'  # lightcoral
    elif val < -1 and val >= -3:
        color = '#ff6347'  # tomato
    elif val < -3:
        color = '#ff0000'  # red
    else:
        color = '#000000'  # black for no change or invalid data

    return 'background-color: {}'.format(color) # return the background color style as css string





def verdict_color(val):
    """Color code the verdict column."""


    # give every verdict a specific color for the heatmap
    if val == 'Buy':
        color = '#00ff00'  # green
    elif val == 'Strong Buy':
        color = '#008000'  # dark green
    elif val == 'Strong Sell':
        color = '#800000'  # dark red
    elif val == 'Hold':
        color = '#ffff00'  # yellow
    elif val == 'Sell':
        color = '#ff0000'  # red
    else:
        color = '#000000'  # black for invalid data
    

    return 'background-color: {}'.format(color)





def rsi_color(val):
    """Color code the RSI values."""


    if val > 70:
        color = '#ff0000'  # red for overbought
    elif val < 30:
        color = '#00ff00'  # green for oversold
    else:
        color = '#ffff00'  # yellow for neutral

    return 'background-color: {}'.format(color)





def ema_color(val):
    """Color code the EMA values."""


    if val > 0:
        color = '#00ff00'  # green for bullish
    elif val < 0:
        color = '#ff0000'  # red for bearish
    else:
        color = '#ffff00'  # yellow for neutral

    return 'background-color: {}'.format(color)





def macd_color(val):
    """Color code the MACD values."""


    if val > 0:
        color = '#00ff00'  # green for bullish
    elif val < 0:
        color = '#ff0000'  # red for bearish
    else:
        color = '#ffff00'  # yellow for neutral

    return 'background-color: {}'.format(color)





def sma_color(val):
    """Color code the SMA values."""


    if val > 0.3:
        color = '#00ff00'  # green for bullish
    elif val < -0.3:
        color = '#ff0000'  # red for bearish
    else:
        color = '#ffff00'  # yellow for neutral

    return 'background-color: {}'.format(color)





def bollinger_color(val):
    """Color code the Bollinger Band values."""


    if val > 0.8:
        color = '#00ff00'  # green for strong position
    elif val < 0.2:
        color = '#ff0000'  # red for weak position
    else:
        color = '#ffff00'  # yellow for neutral

    return 'background-color: {}'.format(color)