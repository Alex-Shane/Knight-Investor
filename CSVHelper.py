#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:55:07 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
from Scraper import Scraper 

def updateIndustries(file_name):
    df = pd.read_csv(file_name, index_col = 0)
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
    df.to_csv(file_name, index = False)

def cleanCSV(file_name):
    df = pd.read_csv(file_name, index_col = 0)
    df = df[~df.Symbol.str.contains('\^')]
    tickers = df['Symbol'].tolist()
    df = df.reset_index(drop = True)
    index = 0
    for ticker in tickers:
        if '/' in ticker:
            ticker = ticker.replace('/', '-')
            df.loc[index, 'Symbol'] = ticker
        index = index + 1
    df.to_csv(file_name, index = False)
    
def makeCSV(exchange):
    df = pd.DataFrame()
    if exchange == 'SP500':
        tickers = Scraper.getSP500Tickers()
        file_name = 'SP500_stocks.csv'
    elif exchange == 'Dow':
        tickers = Scraper.getDOWTickers()
        file_name = 'Dow_Jones_stocks.csv'
    else:
        tickers = Scraper.getNASDAQTickers()
        file_name = 'NASDAQ_100_stocks.csv'
    df['Symbol'] = tickers
    industries = list()
    for ticker in tickers:
        try:
            industries.append(yf.Ticker(ticker).info['industry'])
        except:
            industries.append('Miscellaneous')
    df['Industry'] = industries
    df.to_csv(file_name, index = False)



