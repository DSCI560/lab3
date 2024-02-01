import yfinance as yf
import sqlite3
import mysql.connector

conn = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = 'Ldy990912!',
    database = 'stock_portfolio'
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM portfolio')
results = cursor.fetchall()
for row in results:
    print(row)


def fetch_stock_data(stock_symbol, start_date, end_date):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(start=start_date, end=end_date)
    return data

# 示例：获取苹果公司(AAPL)在指定日期范围内的股票数据
data = fetch_stock_data('AAPL', '2023-01-01', '2023-01-10')
print(data)



def check_stock_validity(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    # Check if the stock data exists
    #return stock.info['regularMarketPrice'] is not None
    return stock

# def add_stock_to_portfolio(portfolio_id, stock_symbol):
#     if check_stock_validity(stock_symbol):
#         try:
#             conn = sqlite3.connect('stock_portfolio.db')
#             cursor = conn.cursor()

#             # 在这里，我们默认股票名称为股票代码
#             cursor.execute("INSERT INTO stocks (portfolio_id, stock_symbol, stock_name) VALUES (?, ?, ?)",
#                            (portfolio_id, stock_symbol, stock_symbol))
#             conn.commit()
#             print("股票添加成功")
#         except sqlite3.Error as e:
#             print(f"数据库错误: {e}")
#         finally:
#             conn.close()
#     else:
#         print("无效的股票代码")

def add_portfolio(portfolio_name, creation_date):
    try:
        conn = mysql.connector.connect (
            host = 'localhost',
            user = 'root',
            password = 'Ldy990912!',
            database = 'stock_portfolio')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM portfolio WHERE name = %s",(portfolio_name,))
        if cursor.fetchone()[0]>0:
            print('the portfolio already exists')
            return 
        
        cursor.execute("INSERT INTO portfolio (name, creation_date) VALUES (%s, %s)", (portfolio_name, creation_date))
      
        #print(data)
        #cursor.execute(query, data)
        # ursor.execute("INSERT INTO 'portfolio' ('name', 'creation_date') VALUES (?, ?)", (portfolio_name, creation_date))
        conn.commit()
        print("Portfolio added successfully")
        conn.close()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        
def add_stock_to_portfolio(portfolio_name, stock_symbol):
    if check_stock_validity(stock_symbol):
        try:
            conn = mysql.connector.connect (
                host = 'localhost',
                user = 'root',
                password = 'Ldy990912!',
                database = 'stock_portfolio')
            cursor = conn.cursor()
            # Check if the portfolio exists
            cursor.execute("SELECT portfolio_id FROM portfolio WHERE name = %s", (portfolio_name,))
            portfolio = cursor.fetchone()
            if portfolio is None:
                print("Portfolio does not exist")
                return
            p_id = portfolio[0]
            

            # Assuming stock symbol is used as the stock name
            cursor.execute("INSERT INTO stocks (portfolio_id, symbol) VALUES (%s, %s)",
                           (p_id, stock_symbol))
            conn.commit()
            print("Stock added successfully")
            conn.close()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
    else:
        print("Invalid stock symbol")
        
        
def remove_stock_from_portfolio(portfolio_name, stock_symbol):
    if check_stock_validity(stock_symbol):
        try:
            conn = mysql.connector.connect (
                host = 'localhost',
                user = 'root',
                password = 'Ldy990912!',
                database = 'stock_portfolio')
            cursor = conn.cursor()
            # Check if the portfolio exists
            cursor.execute("SELECT portfolio_id FROM portfolio WHERE name = %s", (portfolio_name,))
            portfolio = cursor.fetchone()
            if portfolio is None:
                print("Portfolio does not exist")
                return
            p_id = portfolio[0]
    
    
  	    # if exist, perform deletion
            cursor.execute("DELETE FROM stocks WHERE portfolio_id = %s AND symbol = %s", (p_id, stock_symbol))
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                print("Stock removed successfully")
            else:
                print("Stock not found")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

def display_portfolios():
    try:
        conn = mysql.connector.connect (
            host = 'localhost',
            user = 'root',
            password = 'Ldy990912!',
            database = 'stock_portfolio')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio")
        portfolios = cursor.fetchall()

        for portfolio in portfolios:
            print(f"Portfolio ID: {portfolio[0]}, Creation Date: {portfolio[1]}")
            cursor.execute("SELECT symbol FROM stocks WHERE portfolio_id = %s", (portfolio[0],))
            stocks = cursor.fetchall()
            print("Stocks included: " + ", ".join([stock[0] for stock in stocks]))
            print()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

# test function
def test_portfolio_management():
    portfolio_name = 'new'
    creation_date = '2024-02-01'
    
    # assume we have a portfolio name and creation date, test the add portfolio function
    # add_portfolio(portfolio_name, creation_date)
    
    # a list of stock sumbols
    stock_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "JPM", "JNJ", "KO", "BA", "NVDA"]

    # add symbols to a portfolio
    for symbol in stock_symbols:
        add_stock_to_portfolio(portfolio_name, symbol)

    # show the current portfolios
    display_portfolios()
    
    # remove stock from portfolio
    remove_stock_from_portfolio('tech', "TSLA")

    # show the portfolio again to see if delete succesfully
    display_portfolios()




# run test function
test_portfolio_management()
conn.close()

