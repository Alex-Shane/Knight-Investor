#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:15:27 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
import requests
# from stocksymbol import StockSymbol
from bs4 import BeautifulSoup
from Stock import Stock
import datetime as DT
#import nasdaqdatalink as ndl


class Scraper:
    

    def scrapeSP500(report_type):
        """
        Scrapes the table of S&P 500 tickers from a specific source and creates a list of those stocks.

        Returns:
            list: A list of S&P 500 tickers.

        """
        sp500url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        table = pd.read_html(sp500url)
        tickers = table[0]['Symbol'].tolist()
        # manually update discrepancies from wikipedia tickers to yahoo tickers
        tickers[65] = "BRK-B"
        tickers[81] = "BF-B"
        stocks = list()
        for ticker in tickers:
            print(ticker)
            ticker = yf.Ticker(ticker)
            stock = Stock(ticker)
            if not report_type == 'daily':
                stock.info = ticker.info
            stocks.append(stock)
        return stocks
    
    def getExchangeInfo(self, exchange, context, duration):
        if exchange == 'NYSE':
            Scraper.getNYSEInfo(context, duration)
        elif exchange == 'SP500':
            Scraper.getSPIndexInfo(context, duration)
        else:
            Scraper.getNASDAQInfo(context, duration)
        
    def getNASDAQInfo(self, context, duration):
        context['exchange'] = "NASDAQ Composite"
        current_index = yf.Ticker('^IXIC').info['ask']
        if duration == 'day':
            hist = yf.Ticker('^IXIC').history(period='1d')
        elif duration == 'month':
            hist = yf.Ticker('^IXIC').history(period='1mo')
        elif duration == 'week':
            today = DT.date.today()
            week_ago = today - DT.timedelta(days=7)
            hist = yf.Ticker('^IXIC').history(
                start=week_ago, end=today, actions=False)
        else:
            print("invalid duration")
            return
        Scraper.finishInfo(context, hist, current_index)
    
    def getNYSEInfo(context, duration):
        context['exchange'] = "NYSE Composite"
        current_index = yf.Ticker('^NYA').info['ask']
        if duration == 'day':
            hist = yf.Ticker('^NYA').history(period='1d')
        elif duration == 'month':
            hist = yf.Ticker('^NYA').history(period='1mo')
        elif duration == 'week':
            today = DT.date.today()
            week_ago = today - DT.timedelta(days=7)
            hist = yf.Ticker('^NYA').history(
                start=week_ago, end=today, actions=False)
        else:
            print("invalid duration")
            return
        Scraper.finishInfo(context, hist, current_index)


    def getSPIndexInfo(self, context, duration):
        context['exchange'] = "S&P 500 Index"
        current_index = yf.Ticker('^GSPC').info['ask']
        if duration == 'day':
            hist = yf.Ticker('^GSPC').history(period='1d')
        elif duration == 'month':
            hist = yf.Ticker('^GSPC').history(period='1mo')
        elif duration == 'week':
            today = DT.date.today()
            week_ago = today - DT.timedelta(days=7)
            hist = yf.Ticker('^GSPC').history(
                start=week_ago, end=today, actions=False)
        else:
            print("invalid duration")
            return
        Scraper.finishInfo(context, hist, current_index)
        
    def finishInfo(context, hist, current_index):
        previous_index = hist['Open'][0]
        percent = round((current_index - previous_index) /
                        previous_index * 100, 2)
        change = ''
        if percent >= 0:
            change = 'increased'
        else:
            change = 'decreased'
            percent = percent * -1
        context['percent'] = percent
        context['change'] = change

    def scrapeNYSE(report_type):
# =============================================================================
#         # NYSE quotes post request api
#         url = 'https://www.nyse.com/api/quotes/filter'
# 
#         # Filter the paginated post request to get all NYSE tickers in ASC order, max 10,000 results
#         # There are only 7454 on NYSE, so this should be fine
#         response = requests.post(
#             url, json={"instrumentType": "EQUITY", "pageNumber": 1, "sortColumn": "NORMALIZED_TICKER", "sortOrder": "ASC", "maxResultsPerPage": 10000, "filterToken": ""})
# 
#         # Create a list of NYSE stocks
#         stocks = list()
#         tickers = list()
#         for ticker in response.json():
#             symbol = ticker['symbolTicker']
#             #yahoo finance doesn't recognize periods in tickers
#             if '.' in symbol or '-' in symbol:
#                 #if stock isn't class A stock, ignore it
#                 if not (symbol[-1] == '.' or symbol[-1] == '-' or '.A' in symbol or '-A' in symbol):
#                     continue
#                 elif '.' in symbol:
#                     symbol = symbol.replace('.', '-')
#             tickers.append(symbol)
# 
#         for ticker in tickers:
#             try:
#                 ticker = yf.Ticker(ticker)
#                 stock = Stock(ticker)
#                 if not report_type == 'daily':
#                     info = ticker.info
#                     stock.info = info
#                 stocks.append(stock)
#             #if issue getting stock info, either different class of stock which we ignore, or delisted and we want to skip it
#             except:
#                 print(ticker.ticker)
#                 continue
# =============================================================================
        symbols = pd.read_csv('nyse_stocks.csv')['Symbol'].tolist()
        symbols = Scraper.cleanSymbols(symbols)
        stocks = list()
        for symbol in symbols: 
            print(symbol)
            ticker = yf.Ticker(symbol)
            stock = Stock(ticker)
            if not report_type == 'daily':
                try:
                    stock.info = ticker.info
                except:
                    continue
            stocks.append(stock)
        return stocks
        
        

        
    
    def scrapeNASDAQ(report_type):
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
        table = pd.read_html(url)
        tickers = table[4]['Ticker'].tolist()
        stocks = list()
        for ticker in tickers:
            print(ticker)
            ticker = yf.Ticker(ticker)
            stock = Stock(ticker)
            if not report_type == 'daily':
                stock.info = ticker.info
            stocks.append(stock)
        return stocks
    
    def cleanSymbols(symbols):
        index = 0
        for symbol in symbols[:]:
            #don't care about different classes of stock
            if '^' in symbol:
                symbols.remove(symbol)
                index = index - 1
            elif '/' in symbol:
                symbol = symbol.replace('/', '-')
                symbols[index] = symbol
            index = index + 1
        return symbols
    

        






