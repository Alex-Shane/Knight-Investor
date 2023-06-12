#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:55:07 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf

def updateIndustries(file_name):
    df = pd.read_csv(file_name)
    tickers = df['Symbol'].tolist()
    index = 0
    for ticker in tickers:
        print(ticker)
        try:
            industry = yf.Ticker(ticker).info['industry']
            df.loc[index, 'Industry'] = industry
        except:
            continue
        index = index + 1
    df.to_csv(file_name)

def cleanCSV(file_name):
    df = pd.read_csv(file_name)
    df = df[~df.Symbol.str.contains('\^')]
    tickers = df['Symbol'].tolist()
    df = df.reset_index(drop = True)
    index = 0
    for ticker in tickers:
        if '/' in ticker:
            ticker = ticker.replace('/', '-')
            df.loc[index, 'Symbol'] = ticker
        index = index + 1
    df.to_csv(file_name)


cleanCSV('nyse_stocks.csv')
updateIndustries('nyse_stocks.csv')
