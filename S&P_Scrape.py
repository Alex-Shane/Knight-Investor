#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:54:46 2023

@author: Alex
"""

import pandas as pd
from datetime import datetime, timedelta

# Calculate the start and end dates for the past month
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

# Format the dates in the required format (e.g., "05/22/2023")
start_date_str = start_date.strftime("%m/%d/%Y")
end_date_str = end_date.strftime("%m/%d/%Y")

# Define the URL for the S&P 500 historical data
url = f"https://www.slickcharts.com/sp500/history/{start_date_str}/{end_date_str}"

# Read the table from the website using pandas
tables = pd.read_html(url)

# Extract the desired table (assuming it's the first one)
table = tables[0]

table = table[:-1]

# Extract the relevant columns for stock name, high, and low prices
stock_data = table[['Symbol', 'High', 'Low']]

# Group the data by stock name and calculate the maximum high and minimum low prices
grouped_data = stock_data.groupby('Symbol').agg({'High': 'max', 'Low': 'min'})

# Print the high and low prices for each stock in the month
for stock_name, row in grouped_data.iterrows():
    high_price = row['High']
    low_price = row['Low']
    print(f"Stock: {stock_name}")
    print(f"High: {high_price}")
    print(f"Low: {low_price}")
    print()

