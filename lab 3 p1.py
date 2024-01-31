#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd


# In[2]:


def fetch_stock_data(stock_symbol, start_date, end_date):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(start=start_date, end=end_date)
    data.reset_index(inplace=True)
    data.to_csv("stock_data.csv",index=False)
    return data


# In[3]:


data = fetch_stock_data('AAPL', '2023-01-01', '2023-01-10')
print(data)


# In[6]:


miss_val = input("Please choose a type among = (Forward Filling: ffill, Backward Filling: bfill, Interpolate: linear) ---> ")
print(miss_val)
if miss_val in ['ffill', 'bfill']:
    data.fillna(method = miss_val, inplace = True)
else:
    data.interpolate(method = miss_val, inplace = True)
print(data)


# In[7]:


if data['Date'].dtype == 'datetime64[ns]':
    print('The date attribute is already in datetime format')
else:
    print("The 'date' attribute is not in datetime format.")
    data['Date'] = pd.to_datetime(data['Date'])
    print("Converted to datetime format")


# In[8]:


data['daily_returns'] = data['Close'].pct_change()
data["daily_returns"].fillna(0, inplace =True)
print(data.head())


# In[ ]:




