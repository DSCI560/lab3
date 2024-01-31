import yfinance as yf
import pandas as pd

def fetch_stock_data(stock_symbol, start_date, end_date):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(start=start_date, end=end_date)
    data.reset_index(inplace=True)
    data.to_csv("stock_data.csv",index=False)
    return data

data = fetch_stock_data('AAPL', '2023-01-01', '2023-01-10')
print(data)

# Handle Missing Values
miss_val = input("Please choose a type among = (Forward Filling: ffill, Backward Filling: bfill, Interpolate: linear) ---> ")
if miss_val in ['ffill', 'bfill']:
    data.fillna(method = miss_val, inplace = True)
else:
    data.interpolate(method = miss_val, inplace = True)
print(data)

# Data Time format for Attribute:Date
if data['Date'].dtype == 'datetime64[ns]':
    print('The date attribute is already in datetime format')
else:
    print("The 'date' attribute is not in datetime format.")
    data['Date'] = pd.to_datetime(data['Date'])
    print("Converted to datetime format")

# Add Daily Returns as a new attributes
data['daily_returns'] = data['Close'].pct_change()
data["daily_returns"].fillna(0, inplace =True)
print(data.head())
data.to_csv("Preprocessed_stock_data.csv", index= False)


