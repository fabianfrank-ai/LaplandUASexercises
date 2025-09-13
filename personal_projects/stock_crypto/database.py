import sqlite3


#create a new database (or connect to existing) and create a table###
conn = sqlite3.connect('stock_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stocks
             (date TEXT, open REAL, high REAL, low REAL, close REAL, volume INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS buys
             (date TEXT, close REAL)''')
conn.commit()
conn.close()


def insert_stock_data(data):
    """insert data into the database"""

    conn = sqlite3.connect('stock_data.db')
    c = conn.cursor()
    for index, row in data.iterrows():
        c.execute("INSERT INTO stocks (date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?)",
                  (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
    conn.commit()
    conn.close()


def insert_buy(data):
    """insert data into the database"""

    conn = sqlite3.connect('stock_data.db')
    c = conn.cursor()
    for index, row in data.iterrows():
        c.execute("INSERT INTO buys (date, close) VALUES (?, ?)",
                  (index.strftime('%Y-%m-%d'), row['Close']))
    conn.commit()
    conn.close()