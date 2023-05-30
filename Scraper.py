#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:15:27 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from Stock import Stock


class Scraper:
    
    def scrape():
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
    
    def getSPIndexValue():
        url = 'https://www.marketwatch.com/investing/index/spx'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        index_element = soup.find('span', {'class': 'value'})
        index_value = str(index_element.text).replace(",", "")
        return float(index_value)
    
    def getSPIndexInfo(self, context):
        current_index = Scraper.getSPIndexValue()
        hist = yf.Ticker('^GSPC').history(period = '1d')
        previous_index = hist['Open'][0]
        percent = round((current_index - previous_index) / previous_index * 100, 2)
        context['percent'] = percent
        change = ''
        if percent >= 0:
            change = 'increased'
        else:
            change = 'decreased'
        context['change'] = change
    
    def scrapeNYSE(self):
        #Create empty lists for the company ticker
        tickers = list()
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for char in letters:
            tickers = Scraper.scrape_stock_symbols(char, tickers)
        return tickers

    def scrape_stock_symbols(Letter, tickers):
        Letter =  Letter.upper()
        URL =  'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=' + Letter
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        odd_rows = soup.find_all('tr', attrs= {'class':'ts0'})
        even_rows = soup.find_all('tr', attrs= {'class':'ts1'})
        for i in odd_rows:
            row = i.find_all('td')
            tickers.append(row[1].text.strip())
            print(row[1].text.strip())
        for i in even_rows:
            row = i.find_all('td')
            tickers.append(row[1].text.strip())
            print(row[1].text.strip())
        return tickers

scraper = Scraper()
data = scraper.scrapeNYSE()
















