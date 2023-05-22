#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:22:58 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf

class Stock: 
    def __init__(self, ticker, max_monthly_price, min_monthly_price):
        self.ticker = ticker
        self.max_monthly_price = max_monthly_price
        self.min_monthly_price = min_monthly_price
        return
        
    def __str__(self):
        return f'ticker: {self.ticker}, max_price: {self.max_monthly_price}, min_price: {self.min_monthly_price}'
    
    def __repr__(self):
        return f'ticker: {self.ticker}, max_price: {self.max_monthly_price}, min_price: {self.min_monthly_price}'

    
sp500url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
table = pd.read_html(sp500url)
tickers = table[0]['Symbol'].tolist()
stocks = list()
for ticker in tickers: 
    tick = yf.Ticker(ticker)
    hist = tick.history(period='1mo')
    if hist.empty:
        #if stock delisted, remove
        tickers.remove(ticker)
        continue
    max_price = max(hist['High'])
    min_price = min(hist['Low'])
    stock = Stock(ticker, max_price, min_price)
    stocks.append(stock)

print (stocks)
