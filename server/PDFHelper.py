#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:16:36 2023

@author: Alex
"""

from datetime import date as dt
from datetime import timedelta 
import pandas as pd

class PDFHelper:
        
    def handleDividend(self, stock, context, number):
        """
        Checks if the current stock has a dividend rate or not, and updates the context dictionary as appropriate.

        Args:
           stock (Stock): The current stock object.
           context (dict): The context dictionary to store all the variable information in report.html
           number (int): The rank of the stock in the final list of best stocks.

        """
        string = f'a{number}'
        string2 = f'des{number}'
        if not 'dividendRate' in stock.info: 
            context[string] = "No"
            context[string2] = "this stock doesn't currently provide a dividend"
        else:
            context[string] = "Yes"
            dividend = stock.info['dividendRate']
            context[string2] = f'the current dividend rate is {dividend}%' 

    def handleRecommendation(self, stock, context, number):
        """
        Checks the recommendation for the current stock by Yahoo Finance analysts and updates it in the context dictionary.

        Args:
            stock (Stock): The current stock object.
            context (dict): The context dictionary to store the recommendation information.
            number (int): The rank of the stock in the final list of best stocks.

        """
        string = f'rec{number}'
        try:
            rec = stock.info['recommendationKey']
            if rec == 'buy':
                context[string] = "Buy this stock if not already in portfolio"
            elif rec == 'hold':
                context[string] = "Hold this stock if in portfolio"
            else: 
                context[string] = "Sell this stock"
        except:
            context[string] = "No reccomendation available"

    def configNews(self, news, context, num):
        """
        Cuts down the given data table of news information to three articles and adds their titles and links to the context dictionary.

        Args:
            news (list): The data table of news information.
            context (dict): The context dictionary to store the article titles and links.
            number (int): The position of the article we are looking at.
            
        """
        size = len(news)
        articles = 0
        if size < 3:
            articles = size
        else:
            articles = 3
        for x in range(articles):
            title = news[x]['title']
            link = news[x]['link']
            title_string = f'news{num}title'
            link_string = f'news{num}link'
            context[title_string] = title
            context[link_string] = link
            num = num + 1
    
    def makeTitle(self, exchange, context):
        """
        Create a title based on the information from the context dictionary and the given exchange.

        Args:
           context (dict): A dictionary containing the context information for the report.
           exchange (str): The name of the exchange from which the stocks are taken.

        Returns:
           nothing, updates generated title into context dictionary
        """
        if exchange == 'NYSE':
            context['market'] = 'New York Stock Exchange'
        elif exchange == 'SP500':
            context['market'] = 'S&P 500'
        elif exchange == 'NASDAQ100':
            context['market'] = 'NASDAQ 100'
        elif exchange == 'NASDAQ':
            context['market'] = 'NASDAQ Composite (US)'
        elif exchange == 'HKSE':
            context['market'] = 'Hong Kong Stock Exchange'
        else:
            context['market'] = 'Dow Jones'
            
    def getFileName(self, exchange, industry, duration):
        """
        Create a unique filename based on the exchange, industry, and duration of the report.

        Args:
            exchange (str): The name of the exchange from which the stocks of the report are taken 
            duration (str): The duration of the report, such as 'daily', 'weekly', or 'monthly'.

        Returns:
            str: The generated filename string.
    """
        today = dt.today()
        if duration == 'day':
            return (today.strftime("%b-%d-%Y") + "_" + exchange + "_" + industry + "_stock_report.pdf")
        elif duration == 'week': 
            week_ago = today - timedelta(days=7)
            return ("week_of_" + week_ago.strftime("%b-%d-%Y") + "_" + exchange + "_" + industry + "_stock_report.pdf")
        else:
            month_ago = today - timedelta(days=30)
            if today.month == month_ago.month:
                month_year = today.strftime("%B_%Y_")
            else:
                month_year = month_ago.strftime("%B_%Y-") + today.strftime("%B_%Y_")
            return (month_year + exchange + "_" + industry + "_stock_report.pdf")
    
    def getIndustry(self, stock, exchange):
        if exchange == 'NYSE':
            df = pd.read_csv('./static/nyse_stocks.csv')
        elif exchange == 'NASDAQ100':
            df = pd.read_csv('./static/NASDAQ_100_stocks.csv')
        elif exchange == 'NASDAQ':
            df = pd.read_csv('./static/NASDAQ_stocks.csv')
        elif exchange == 'HKSE':
            df = pd.read_csv('./static/HKSE_stocks.csv')
        else:
            df = pd.read_csv('./static/SP500_stocks.csv')
        
        df_indexed = df.set_index("Symbol")
        industry = df_indexed.at[stock.ticker, "Industry"]
        if '—' in industry:
            industry = industry.replace('—', ': ')
        return industry
    

    
            
            
        
