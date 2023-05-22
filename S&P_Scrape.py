#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:54:46 2023

@author: Alex
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Calculate the start and end dates for the past month
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

# Format the dates in the required format (e.g., "05/22/2023")
start_date_str = start_date.strftime("%m/%d/%Y")
end_date_str = end_date.strftime("%m/%d/%Y")

# Define the URL for the S&P 500 historical data
url = f"https://www.slickcharts.com/sp500/history/{start_date_str}/{end_date_str}"

# Send a GET request to the website and parse the HTML response
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table that contains the data
table = soup.find("table", {"class": "table-hover"})

# Initialize an empty dictionary to store the high and low prices for each stock
stock_prices = {}

# Iterate over each row in the table (excluding the header row)
for row in table.find_all("tr")[1:]:
    columns = row.find_all("td")
    stock_name = columns[1].text.strip()
    high = float(columns[2].text.strip().replace(",", ""))
    low = float(columns[3].text.strip().replace(",", ""))

    # Update the high and low prices for the stock in the dictionary
    if stock_name in stock_prices:
        stock_prices[stock_name]["high"] = max(stock_prices[stock_name]["high"], high)
        stock_prices[stock_name]["low"] = min(stock_prices[stock_name]["low"], low)
    else:
        stock_prices[stock_name] = {"high": high, "low": low}

# Print the high and low prices for each stock in the month
for stock_name, prices in stock_prices.items():
    print(f"Stock: {stock_name}")
    print(f"High: {prices['high']}")
    print(f"Low: {prices['low']}")
    print()
