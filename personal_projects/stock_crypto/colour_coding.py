#this is mainly used to colour code the dataframe in streamlit
#Mostly the colours represent a traffic light(green, red, orange) depending on how good/bad a value is

def color_code(val):
    """Color code the dataframe based on the percentage change."""


    # Define color thresholds, bigger changes get darker colors, to emphasize them
    if val > 0 and val <=1:
        color = '#90ee90'  
    elif val > 1 and val <=3:
        color = '#32cd32' 
    elif val > 3:
        color = '#008000' 
    elif val < 0 and val >= -1:
        color = '#ffcccb'  
    elif val < -1 and val >= -3:
        color = '#ff6347' 
    elif val < -3:
        color = '#ff0000'  
    else:
        color = '#000000'  

    return 'background-color: {}'.format(color) 





def verdict_color(val):
    """Color code the verdict column."""


    # give every verdict a specific color for the heatmap
    if val == 'Buy':
        color = '#00ff00'  
    elif val == 'Strong Buy':
        color = '#008000'  
    elif val == 'Strong Sell':
        color = '#800000'  
    elif val == 'Hold':
        color = '#ffa700' 
    elif val == 'Sell':
        color = '#ff0000' 
    else:
        color = '#000000'  
    

    return 'background-color: {}'.format(color)





def rsi_color(val):
    """Color code the RSI values."""


    if val > 70:
        color = '#ff0000' 
    elif val < 30:
        color = '#00ff00' 
    else:
        color = '#ffa700' 

    return 'background-color: {}'.format(color)





def ema_color(val):
    """Color code the EMA values."""


    if val > 0:
        color = '#00ff00'  
    elif val < 0:
        color = '#ff0000' 
    else:
        color = '#ffa700'  

    return 'background-color: {}'.format(color)





def macd_color(val):
    """Color code the MACD values."""


    if val > 0:
        color = '#00ff00' 
    elif val < 0:
        color = '#ff0000' 
    else:
        color = '#ffa700' 

    return 'background-color: {}'.format(color)





def sma_color(val):
    """Color code the SMA values."""


    if val > 0.3:
        color = '#00ff00'  
    elif val < -0.3:
        color = '#ff0000'  
    else:
        color = '#ffa700' 

    return 'background-color: {}'.format(color)





def bollinger_color(val):
    """Color code the Bollinger Band values."""


    if val > 0.8:
        color = '#00ff00'  
    elif val < 0.2:
        color = '#ff0000'  
    else:
        color = '#ffa700' 

    return 'background-color: {}'.format(color)
