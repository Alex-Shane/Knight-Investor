#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:22:58 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
import jinja2
import pdfkit
import requests
from bs4 import BeautifulSoup
from Scraper import Scraper
from PDFHelper import PDFHelper

    
def makePDF(stocks, exchange, industry):
    """
    Generates a PDF file containing relevant information and current news about the highest ranked stocks for current month.

    Args:
        final_three (list): A list of the highest ranked stocks for the month
        exchange (str): name of the stock exchange being reported on

    """
    context = {}
    helper = PDFHelper()
    helper.makeTitle(exchange, context)
    scraper = Scraper()
    scraper.getExchangeInfo(exchange, context, 'month')
    context['s1'] = stocks[0].info['longName']
    context['s1ticker'] = stocks[0].ticker
    context['d1'] = f'{stocks[0].delta / stocks[0].open * 100:.2f}'
    cur1 = round(stocks[0].info['currentPrice'], 2)
    cur1 = ('{:,}'.format(cur1))
    context['price1'] = cur1
    mcap1 = ('{:,}'.format(stocks[0].info['marketCap']))
    context['mcap1'] = mcap1
    context['i1'] = industry
    helper.handleDividend(stocks[0], context, 1)
    helper.handleRecommendation(stocks[0], context, 1)
    context['link1'] = f"https://finance.yahoo.com/quote/{stocks[0].ticker}/news?p={stocks[0].ticker}"
    if len(stocks) > 1:
        context['s2'] = stocks[1].info['longName']
        context['s2ticker'] = stocks[1].ticker
        context['d2'] = f'{stocks[1].delta / stocks[1].open * 100:.2f}'
        cur2 = round(stocks[1].info['currentPrice'], 2)
        cur2 = ('{:,}'.format(cur2))
        context['price2'] = cur2
        mcap2 = ('{:,}'.format(stocks[1].info['marketCap']))
        context['mcap2'] = mcap2
        context['i2'] = industry
        helper.handleDividend(stocks[1], context, 2)
        helper.handleRecommendation(stocks[1], context, 2)
        context['link2'] = f"https://finance.yahoo.com/quote/{stocks[1].ticker}/news?p={stocks[1].ticker}"
    if len(stocks) > 2:
        context['s3'] = stocks[2].info['longName']
        context['s3ticker'] = stocks[2].ticker
        context['d3'] = f'{stocks[2].delta / stocks[2].open * 100:.2f}'
        cur3 = round(stocks[2].info['currentPrice'], 2)
        cur3 = ('{:,}'.format(cur3))
        context['price3'] = cur3
        mcap3 = ('{:,}'.format(stocks[2].info['marketCap']))
        context['mcap3'] = mcap3
        context['i3'] = industry
        helper.handleDividend(stocks[2], context, 3)
        helper.handleRecommendation(stocks[2], context, 3)
        context['link3'] = f"https://finance.yahoo.com/quote/{stocks[2].ticker}/news?p={stocks[2].ticker}"
    file_name = helper.getFileName(exchange, industry, 'month')
    return (context, file_name, stocks, None)


def rankStocks(stocks):
    """
    Ranks the given list of stocks based on a multitude of financial information and factors.

    Args:
        stocks (list): A list of stocks to be ranked.

    Returns:
        list: the same list of stocks but with updated rank attributes

    """
    stocks = rankPercentIncrease(stocks)
    stocks = rankTrailingEPS(stocks)
    stocks = rankForwardEPS(stocks)
    stocks = rankTrailingPE(stocks)
    stocks = rankForwardPE(stocks)
    stocks = rankEVRev(stocks)
    stocks = rankEBITDA(stocks)
    return stocks

def rankPercentIncrease(stocks): 
    """
    Ranks the given list of stocks based on the percent increase in stock price over the past month.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated percentIncreaseRatings

    """
    increase_values = dict()
    index = 0
    for stock in stocks[:]:
        ticker = stock.ticker_obj
        try: 
            hist = ticker.history(period = '1mo')
            if not hist.empty:
                stock.open = hist['Open'][0]
                stock.close = hist['Close'][-1]
                stock.delta = stock.close - stock.open
                increase = stock.delta / stock.open * 100
                increase_values[stock] = increase
        #if stock doesn't have history, remove it
        except:
            stocks.remove(stock)
            index = index - 1
        index = index + 1
    while(len(increase_values) != 0):
        highest_increase_stock = max(increase_values, key = increase_values.get)
        highest_increase_stock.increase_rating = len(increase_values)
        highest_increase_stock.rank += 0.4*highest_increase_stock.increase_rating
        del increase_values[highest_increase_stock]
    return stocks

def rankTrailingEPS(stocks):
    """
    Ranks the given list of stocks based on the previous 12 months' EPS.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated trailingEPSRatings

    """
    eps_values = dict()
    for stock in stocks:
        if 'trailingEps' in stock.info:
            if not isinstance(stock.info['trailingEps'], str):
                eps_values[stock] = stock.info['trailingEps']
    while(len(eps_values) != 0): 
        highest_EPS_Stock = max(eps_values, key = eps_values.get)
        highest_EPS_Stock.trailing_eps_rating = len(eps_values)
        highest_EPS_Stock.rank += 0.1*highest_EPS_Stock.trailing_eps_rating
        del eps_values[highest_EPS_Stock]
    return stocks

def rankForwardEPS(stocks):
    """
    Ranks the given list of stocks based on future projected EPS.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated forwardEPSRatings

    """
    feps_values = dict()
    for stock in stocks:
        if 'forwardEps' in stock.info:
            if not isinstance(stock.info['forwardEps'], str):
                feps_values[stock] = stock.info['forwardEps']
    while(len(feps_values) != 0): 
        highest_fEPS_Stock = max(feps_values, key = feps_values.get)
        highest_fEPS_Stock.forward_eps_rating = len(feps_values)
        highest_fEPS_Stock.rank += 0.025*highest_fEPS_Stock.forward_eps_rating
        del feps_values[highest_fEPS_Stock]
    return stocks

def rankTrailingPE(stocks):
    """
    Ranks the given list of stocks based on the previous 12 months' PE ratios.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated trailingPERatings

    """
    pe_values = dict()
    for stock in stocks:
        if 'trailingPE' in stock.info:
            if not isinstance(stock.info['trailingPE'], str):
                pe_values[stock] = stock.info['trailingPE']
    while(len(pe_values) != 0):
        best_pe_stock = min(pe_values, key = pe_values.get)
        best_pe_stock.trailing_pe_rating = len(pe_values)
        best_pe_stock.rank += 0.2*best_pe_stock.trailing_pe_rating
        del pe_values[best_pe_stock]
    return stocks

def rankForwardPE(stocks):
    """
    Ranks the given list of stocks based on future projected PE.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated forwardPERatings

    """
    fpe_values = dict()
    for stock in stocks:
        if 'forwardPE' in stock.info:
            if not isinstance(stock.info['forwardPE'], str):
                fpe_values[stock] = stock.info['forwardPE']
    while (len(fpe_values) != 0):
        best_fpe_stock = min(fpe_values, key = fpe_values.get)
        best_fpe_stock.forward_pe_rating = len(fpe_values)
        best_fpe_stock.rank += 0.025*best_fpe_stock.forward_pe_rating
        del fpe_values[best_fpe_stock]
    return stocks

def rankEVRev(stocks):
    """
    Ranks the given list of stocks based on the previous 12 months' EV/Revenue.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated EV/Revenue Ratings

    """
    evRev_values = dict()
    for stock in stocks:
        if 'enterpriseToRevenue' in stock.info:
            if not isinstance(stock.info['enterpriseToRevenue'], str):
                evRev_values[stock] = stock.info['enterpriseToRevenue']
    while (len(evRev_values) != 0): 
        best_evRev_stock = min(evRev_values, key = evRev_values.get)
        best_evRev_stock.EVRev_rating = len(evRev_values)
        best_evRev_stock.rank += 0.1*best_evRev_stock.EVRev_rating
        del evRev_values[best_evRev_stock]
    return stocks

def rankEBITDA(stocks):
    """
    Ranks the given list of stocks based on the previous 12 months' EV/EBITDA.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated EV/EBITDA Ratings

    """
    ebit_values = dict()
    for stock in stocks:
        if 'enterpriseToEbitda' in stock.info:
            if not isinstance(stock.info['enterpriseToEbitda'], str):
                ebit_values[stock] = stock.info['enterpriseToEbitda']
    while (len(ebit_values) != 0): 
        best_ebit_stock = min(ebit_values, key = ebit_values.get)
        best_ebit_stock.Ebit_rating = len(ebit_values)
        best_ebit_stock.rank += 0.15*best_ebit_stock.Ebit_rating
        del ebit_values[best_ebit_stock]
    return stocks


def getFinalStocks(stocks): 
    """
    Calculates the final rankings for each stock in the given list of stocks by updating the rank attribute based on a weighted calculation.

    Args:
        stocks (list): A list of stocks to be ranked.

    Returns:
        list: A new list of stocks sorted in descending order of their rankings.

    """
    best_stocks = list()
    for x in range(0, len(stocks)):
        best = stocks[x]
        if best.info['averageVolume'] == 0 or best.open == 0:
            continue
        else:
            best_stocks.append(best)
            if len(best_stocks) == 3:
                break
    return best_stocks

def run(exchange, industry):
    if exchange == 'NYSE':
        stocks = Scraper.scrapeNYSE('month', industry)
    elif exchange == 'NASDAQ100':
        stocks = Scraper.scrapeNASDAQ100('month', industry)
    elif exchange == 'DOW':
        stocks = Scraper.scrapeDOW('month', industry)
    elif exchange == 'NASDAQ':
        stocks = Scraper.scrapeNASDAQ('month', industry)
    elif exchange == 'HKSE':
        stocks = Scraper.scrapeHKSE('month', industry)
    else:
        stocks = Scraper.scrapeSP500('month', industry)
    rankedStocks = rankStocks(stocks)
    rankedStocks.sort(key = lambda k: k.rank, reverse = True)
    best_stocks = getFinalStocks(rankedStocks)
    return makePDF(best_stocks, exchange, industry)
    







