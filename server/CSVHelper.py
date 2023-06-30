#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:55:07 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
#from Scraper import Scraper 

def updateIndustriesInCSV(file_name):
    """
    Update the 'Industry' column of a CSV file to match the industries stored in stocks on Yahoo Finance.

    Args:
       csv_file (str): The path or file object of the CSV file to be updated.
                       The CSV file should have a column header named 'Symbol' representing the stock tickers.
   """
    df = pd.read_csv(file_name)
    tickers = df['Symbol'].tolist()
    index = 0
    for ticker in tickers:
        try:
            industry = yf.Ticker(ticker).info['industry']
            df.loc[index, 'Industry'] = industry
        except:
            print(ticker)
            pass
        index = index + 1
    df.to_csv(file_name, index = False)

def sortByIndustry(file_name, industry):
    df = pd.read_csv(file_name)
    #df = df[df.Industry == industry]
    filtered_df = df[df['Industry'].str.contains(industry, case=False, na=False)]
    return filtered_df['Symbol'].tolist()

def cleanCSV(file_name):
    """
    Clean a CSV file by deleting all stocks with '^' character in their ticker and updating discrepancies in tickers
    to match the tickers on Yahoo Finance.

    Args:
        csv_file (str): The path or file object of the CSV file to be cleaned.
                    The CSV file should have a column header named 'Symbol' representing the stock tickers.
    """
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
    df.to_csv(file_name, index = False)
    
def getIndustriesInCSV(file_name):
    df = pd.read_csv(file_name)['Industry'].tolist()
    industries = dict()
    for industry in df:
        if industry in industries:
            industries[industry] = industries[industry] + 1
        else:
            industries[industry] = 1
    eligible_industries = []
    keys = list(industries.keys())
    eligible_industries = []
    [eligible_industries.append(x) for x in keys if industries[x] > 5]
    #[industries.append(x) for x in df if x not in industries]
    return eligible_industries

def cleanNASDAQ():
    df = pd.read_csv('./static/NASDAQ_stocks.csv')
    filtered_df = df[df['Symbol'].str.len() < 5]
    filtered_df = filtered_df[filtered_df['Country'].str.contains('United States', na = False)]
    filtered_df.to_csv('./static/NASDAQ_stocks.csv', index = False)

cleanNASDAQ()
    
    


# =============================================================================
# def makeCSV(exchange):
#     """
#     Create a CSV file for storing stocks from a specific exchange.
# 
#     Args:
#         exchange (str): The name of the exchange for which the CSV file is being created.
#     """
#     df = pd.DataFrame()
#     if exchange == 'SP500':
#         tickers = Scraper.getSP500Tickers()
#         file_name = 'SP500_stocks.csv'
#     elif exchange == 'DOW':
#         tickers = Scraper.getDOWTickers()
#         file_name = 'Dow_Jones_stocks.csv'
#     else:
#         tickers = Scraper.getNASDAQ100Tickers()
#         file_name = 'NASDAQ_100_stocks.csv'
#     df['Symbol'] = tickers
#     industries = list()
#     for ticker in tickers:
#         try:
#             industries.append(yf.Ticker(ticker).info['industry'])
#         except:
#             industries.append('Miscellaneous')
#     df['Industry'] = industries
#     df.to_csv(file_name, index = False)
# =============================================================================

