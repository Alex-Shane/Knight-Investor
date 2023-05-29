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
        # URL of the website with the table
        base_url = 'https://www.nyse.com/listings_directory/stock'

        # Initialize an empty list to store the extracted data
        data = []

        # Make an initial request to get the first page
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from the current page
        table = soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                # Extract the relevant data from the cells and append it to the list
                cell_data = [cell.text.strip() for cell in cells]
                data.append(cell_data)
                print(cell_data)

        # Find the total number of pages
        pagination = soup.find('div', class_='pagination')
        num_pages = len(pagination.find_all('a'))

        # Iterate over the remaining pages
        for page in range(2, num_pages + 1):
            # Construct the URL for the next page
            page_url = base_url + '?page=' + str(page)

        # Send a request to the next page
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from the current page
        table = soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                # Extract the relevant data from the cells and append it to the list
                cell_data = [cell.text.strip() for cell in cells]
                data.append(cell_data)
                print(cell_data)
        return data

scraper = Scraper()
data = scraper.scrapeNYSE()
















