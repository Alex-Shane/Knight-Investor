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
    

    def scrapeSP500():
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
            tick = yf.Ticker(ticker)
            stock = Stock(ticker)
            stock.info = tick.info
            stocks.append(stock)
        return stocks

# =============================================================================
#     def scrape2(self):
#         tickers = self.ss.get_symbol_list('US', 'SPX', True)
#         tickers[7] = "BRK-B"
#         tickers[271] = "BF-B"
#         tickers[6] = "META"
#         tickers[82] = "ELV"
#         tickers[165] = "SPGI"
#         stocks = list()
#         for ticker in tickers:
#             print(ticker)
#             tick = yf.Ticker(ticker)
#             stock = Stock(ticker)
#             stock.info = tick.info
#             stocks.append(stock)
#         return stocks
# =============================================================================

    def getSPIndexValue():
        url = 'https://www.marketwatch.com/investing/index/spx'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        index_element = soup.find('span', {'class': 'value'})
        index_value = str(index_element.text).replace(",", "")
        return float(index_value)

    def getSPIndexInfo(self, context, duration):
        current_index = Scraper.getSPIndexValue()
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

    def scrapeNYSE():
        # NYSE quotes post request api
        url = 'https://www.nyse.com/api/quotes/filter'

        # Filter the paginated post request to get all NYSE tickers in ASC order, max 10,000 results
        # There are only 7454 on NYSE, so this should be fine
        response = requests.post(
            url, json={"instrumentType": "EQUITY", "pageNumber": 1, "sortColumn": "NORMALIZED_TICKER", "sortOrder": "ASC", "maxResultsPerPage": 10000, "filterToken": ""})

        # Create a list of NYSE stocks
        stocks = list()
        tickers = list()
        for ticker in response.json():
            symbol = ticker['symbolTicker']
            #yahoo finance doesn't recognize periods in tickers
            if '.' in symbol:
                symbol = symbol.replace('.','-')
            tickers.append(symbol)
        
        clean_tickers = Scraper.cleanTickers(tickers)
            
        for ticker in clean_tickers:
            tick = yf.Ticker(ticker)
            info = list()
            try:
                info = tick.info
            except:
                ticker = ticker.replace('-', '-P')
                tick = yf.Ticker(ticker)
                info = tick.info
            finally:
                stock = Stock(ticker)
                stock.info = info
                stocks.append(stock)
                print(tick.ticker)
        return stocks
    
    def scrapeNASDAQ():
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
        table = pd.read_html(url)
        tickers = table[4]['Ticker'].tolist()
        stocks = list()
        for ticker in tickers:
            print(ticker)
            tick = yf.Ticker(ticker)
            stock = Stock(ticker)
            stock.info = tick.info
            stocks.append(stock)
        return stocks
    
    def cleanTickers(tickers):
        del tickers[3367]
        del tickers[3785]
        del tickers[4122]
        del tickers[4971]
        del tickers[6197]
        del tickers[6316]
        return tickers
    

    


