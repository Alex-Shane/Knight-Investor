#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:15:27 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
from Stock import Stock
import datetime as DT


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
        elif exchange == 'Dow':
            Scraper.getDowInfo(context, duration)
        else:
            Scraper.getNASDAQInfo(context, duration)
    
    def getDowInfo(context, duration):
        context['exchange'] = "Dow Jones Industrial Average"
        if duration == 'day':
            hist = yf.Ticker('^DJI').history(period='1d')
        elif duration == 'month':
            hist = yf.Ticker('^DJI').history(period='1mo')
        elif duration == 'week':
            today = DT.date.today()
            week_ago = today - DT.timedelta(days=7)
            hist = yf.Ticker('^DJI').history(
                start=week_ago, end=today, actions=False)
        else:
            print("invalid duration")
            return
        Scraper.finishInfo(context, hist)
         
    def getNASDAQInfo(context, duration):
        context['exchange'] = "NASDAQ Composite"
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
        Scraper.finishInfo(context, hist)
    
    def getNYSEInfo(context, duration):
        context['exchange'] = "NYSE Composite"
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
        Scraper.finishInfo(context, hist)


    def getSPIndexInfo(context, duration):
        context['exchange'] = "S&P 500 Index"
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
        Scraper.finishInfo(context, hist)
        
    def finishInfo(context, hist):
        current_index = hist['Close'][-1]
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
    
    def scrapeDOW(report_type):
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
        table = pd.read_html(url)
        tickers = table[1]['Symbol']
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
    


