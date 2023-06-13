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
        
        Args:
            report_type (str): string representing the type of report being made

        Returns:
            list: A list of S&P 500 stocks

        """
        tickers = Scraper.getSP500Tickers()
        stocks = list()
        for ticker in tickers:
            print(ticker)
            ticker = yf.Ticker(ticker)
            stock = Stock(ticker)
            if not report_type == 'daily':
                stock.info = ticker.info
            stocks.append(stock)
        return stocks
    
    def getSP500Tickers():
        """
        Scrape S&P 500 tickers from specified url and return them in a list.

        Returns:
            list: A list of strings representing the S&P 500 tickers.
        """
        sp500url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        table = pd.read_html(sp500url)
        tickers = table[0]['Symbol'].tolist()
        # manually update discrepancies from wikipedia tickers to yahoo tickers
        tickers[65] = "BRK-B"
        tickers[81] = "BF-B"
        return tickers
    
    def getExchangeInfo(self, exchange, context, duration):
        """
        Update information about the exchange being looked at for the final report.

        Args:
            context (dict): A dictionary containing the context information for the report.
            exchange (str): The name of the exchange being looked at.
            duration (str): the period over which the report looks at (day, week, month)
        """
        if exchange == 'NYSE':
            Scraper.getNYSEInfo(context, duration)
        elif exchange == 'SP500':
            Scraper.getSPIndexInfo(context, duration)
        elif exchange == 'Dow':
            Scraper.getDowInfo(context, duration)
        else:
            Scraper.getNASDAQInfo(context, duration)
    
    def getDowInfo(context, duration):
        """
        Update information about the Dow Jones Industrial Average over given duration

        Args:
            context (dict): A dictionary containing the context information for the report.
            duration (str): the period over which the report looks at (day, week, month)
        """
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
        """
        Update information about the NASDAQ Composite over the given duration

        Args:
            context (dict): A dictionary containing the context information for the report.
            duration (str): the period over which the report looks at (day, week, month)
        """
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
        """
        Update information about the New York Stock Exchange over the given period

        Args:
            context (dict): A dictionary containing the context information for the report.
            duration (str): the period over which the report looks at (day, week, month)
        """
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
        """
        Update information about the S&P 500 over the given period

        Args:
            context (dict): A dictionary containing the context information for the report.
            duration (str): the period over which the report looks at (day, week, month)
        """
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
        """
        Find the percent increase or decrease in the given exchange's index and update the context dictionary.

        Args:
            context (dict): A dictionary containing the context information for the report.
            hist (DataFrame): DataFrame containing the price information about the given exchange's price info over the given duration'
        """
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
        """
        Scrape a CSV file of all current stock tickers in NYSE and return a list of Stock objects.

        Args:
            report_type (str): represents the period over which the report looks at.
                                If looking at daily report, yfinance info not called due to time intensity

        Returns:
            list: A list of Stock objects representing the tickers scraped from the NYSE CSV file.
        """
        symbols = pd.read_csv('nyse_stocks.csv')['Symbol'].tolist()
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
        """
        Scrape NASDAQ 100 stocks from Wikipedia and gather the information into Stock objects.
        
        Args:
            report_type (str): represents the period over which the report looks at.
                                If looking at daily report, yfinance info not called due to time intensity

        Returns:
            list: A list of Stock objects representing the NASDAQ 100 stocks.
        """
        tickers = Scraper.getNASDAQTickers()
        stocks = list()
        for ticker in tickers:
            print(ticker)
            ticker = yf.Ticker(ticker)
            stock = Stock(ticker)
            if not report_type == 'daily':
                stock.info = ticker.info
            stocks.append(stock)
        return stocks
    
    def getNASDAQTickers():
        """
        Scrape NASDAQ 100 tickers from Wikipedia and return them in a list.

        Returns:
            list: A list of strings representing the NASDAQ 100 tickers.
        """
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
        table = pd.read_html(url)
        tickers = table[4]['Ticker'].tolist()
        return tickers
    
    def scrapeDOW(report_type):
        """
        Scrape Dow Jones Industrial Average (Dow) stocks from Wikipedia and gather the information into Stock objects.

        Returns:
           list: A list of Stock objects representing the Dow Jones Industrial Average stocks.
        """
        tickers = Scraper.getDOWTickers()
        stocks = list()
        for ticker in tickers:
            print(ticker)
            ticker = yf.Ticker(ticker)
            stock = Stock(ticker)
            if not report_type == 'daily':
                stock.info = ticker.info
            stocks.append(stock)
        return stocks
    
    def getDOWTickers():
        """
        Scrape Dow tickers from Wikipedia and return them in a list.

        Returns:
            list: A list of strings representing the Dow tickers.
        """
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
        table = pd.read_html(url)
        tickers = table[1]['Symbol']
        return tickers



