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
        # Define the base URL without the page letter
        base_url = "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={}.htm"

        # Define the range of letters for the pages (e.g., A to Z)
        start_letter = ord('A')
        end_letter = ord('Z')

        # Create an empty list to store the tickers
        ticker_list = []

        # Iterate over each page letter
        for page_letter in range(start_letter, end_letter + 1):
            # Construct the URL for the current page
            url = base_url.format(chr(page_letter))
    
            # Send a GET request to the URL
            response = requests.get(url, verify = False)
    
            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
    
            # Find the table element that contains the ticker data
            table = soup.find("table")
    
            # Iterate over each row in the table
            for row in table.find_all("tr"):
                # Extract the ticker symbol from the first column
                ticker = row.find("td").text.strip()
                # Append the ticker to the ticker list
                ticker_list.append(ticker)
                print(ticker)
        return ticker_list

scraper = Scraper()
data = scraper.scrapeNYSE()
















