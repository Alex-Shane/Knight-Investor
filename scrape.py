#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:22:58 2023

@author: Alex
"""

import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si
import jinja2
import pdfkit
import requests
from bs4 import BeautifulSoup

class Stock: 
    def __init__(self, ticker):
        self.ticker = ticker
        self.month_open = 0
        self.month_close = 0
        self.rank = 0
        self.delta = 0
        self.trailing_eps_rating = 0 
        self.forward_eps_rating = 0
        self.industry = ""
        self.trailing_pe_rating = 0
        self.forward_pe_rating = 0
        self.EVRev_rating = 0
        self.Ebit_rating = 0
        self.increase_rating = 0
        self.info = ""
        return
        
    def __str__(self):
        return f'ticker: {self.ticker}, open: {self.month_open}, close: {self.month_close}, ebit: {self.Ebit_rating}'
    
    def __repr__(self):
        return f'ticker: {self.ticker}, open: {self.month_open}, close: {self.month_close}, ebit: {self.Ebit_rating}'


def isTopStockByDelta(currentTopStocks, stock):
    """
    
    Parameters
    ----------
    currentTopStocks : list of Stocks
        list of stocks with highest current deltas
    stock : Stock
        stock's delta is checked against current top deltas to see if it should be added

    Returns
    -------
    Stock
        returns the stock to be removed, None if stock delta isn't greater than current deltas

    """
    for x in range (len(currentTopStocks)):
        if stock.delta > currentTopStocks[x].delta:
            return currentTopStocks[x]
        else:
            return None
# =============================================================================
#     if stock.delta > currentTopStocks[0].delta:
#         return currentTopStocks[0]
#     elif stock.delta > currentTopStocks[1].delta:
#         return currentTopStocks[1]
#     elif stock.delta > currentTopStocks[2].delta:
#         return currentTopStocks[2]
#     else:
#         return None
# =============================================================================

def scrape():
    """
    
    Returns
    -------
    top_stocks : List of Stocks
        returns list of stocks that have greatest stock price delta over past month

    """
    sp500url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(sp500url)
    tickers = table[0]['Symbol'].tolist()
    # manually update discrepancies from wikipedia tickers to yahoo tickers
    tickers[65] = "BRK-B"
    tickers[81] = "BF-B"
    stocks = list()
    top_stocks = [Stock(0,0,0) for x in range(20)]
    for ticker in tickers: 
        tick = yf.Ticker(ticker)
        print(ticker)
        hist = tick.history(period='1mo')
        if not hist.empty:
            month_open = hist['Open'][0]
            month_close = hist['Close'][-1]
            stock = Stock(ticker, month_open, month_close)
            stocks.append(stock)
            check = isTopStockByDelta(top_stocks, stock)
            if check != None: 
                top_stocks.remove(check)
                top_stocks.append(stock)
        else:   
            #if stock delisted, remove
            tickers.remove(ticker)
    return top_stocks

def scrape2():
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

def makePDF(final_three):
    context = {}
    context['s1'] = final_three[0].info['longName']
    context['s1ticker'] = final_three[0].ticker
    context['d1'] = f'{final_three[0].delta / final_three[0].month_open * 100:.2f}'
    cur1 = round(final_three[0].info['currentPrice'], 2)
    cur1 = ('{:,}'.format(cur1))
    context['price1'] = cur1
    mcap1 = ('{:,}'.format(final_three[0].info['marketCap']))
    context['mcap1'] = mcap1
    context['i1'] = final_three[0].info['industry']
    handleDividend(final_three[0], context, 1)
    handleRecommendation(final_three[0], context, 1)
    configNews(yf.Ticker(final_three[0].ticker).get_news(), context, 1)
    context['s2'] = final_three[1].info['longName']
    context['s2ticker'] = final_three[1].ticker
    context['d2'] = f'{final_three[1].delta / final_three[1].month_open * 100:.2f}'
    cur2 = round(final_three[1].info['currentPrice'], 2)
    cur2 = ('{:,}'.format(cur2))
    context['price2'] = cur2
    mcap2 = ('{:,}'.format(final_three[1].info['marketCap']))
    context['mcap2'] = mcap2
    context['i2'] = final_three[1].info['industry']
    handleDividend(final_three[1], context, 2)
    handleRecommendation(final_three[1], context, 2)
    configNews(yf.Ticker(final_three[1].ticker).get_news(), context, 4)
    context['s3'] = final_three[2].info['longName']
    context['s3ticker'] = final_three[2].ticker
    context['d3'] = f'{final_three[2].delta / final_three[2].month_open * 100:.2f}'
    cur3 = round(final_three[2].info['currentPrice'], 2)
    cur3 = ('{:,}'.format(cur3))
    context['price3'] = cur3
    mcap3 = ('{:,}'.format(final_three[2].info['marketCap']))
    context['mcap3'] = mcap3
    context['i3'] = final_three[2].info['industry']
    handleDividend(final_three[2], context, 3)
    handleRecommendation(final_three[2], context, 3)
    configNews(yf.Ticker(final_three[2].ticker).get_news(), context, 7)
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output_text, 'stock_report.pdf', configuration=config)

def handleDividend(stock, context, number):
    string = f'a{number}'
    string2 = f'des{number}'
    if not 'dividendRate' in stock.info: 
        context[string] = "No"
        context[string2] = "this stock doesn't currently provide a dividend"
    else:
        context[string] = "Yes"
        dividend = stock.info['dividendRate']
        context[string2] = f'the current dividend rate is {dividend}%' 

def handleRecommendation(stock, context, number):
    string = f'rec{number}'
    rec = stock.info['recommendationKey']
    if rec == 'buy':
        context[string] = "Buy this stock if not already in portfolio"
    elif rec == 'hold':
        context[string] = "Hold this stock if in portfolio"
    else: 
        context[string] = "Sell this stock"

def configNews(news, context, num):
    for x in range(0, 3):
        title = news[x]['title']
        link = news[x]['link']
        title_string = f'news{num}title'
        link_string = f'news{num}link'
        context[title_string] = title
        context[link_string] = link
        num = num + 1

def rankStocks(topStocks):
    topStocks = rankPercentIncrease(topStocks)
    topStocks = rankTrailingEPS(topStocks)
    topStocks = rankForwardEPS(topStocks)
    topStocks = rankTrailingPE(topStocks)
    topStocks = rankForwardPE(topStocks)
    topStocks = rankEVRev(topStocks)
    topStocks = rankEBITDA(topStocks)
    return topStocks

def rankPercentIncrease(stocks): 
    increase_values = dict()
    counter = 0
    for stock in stocks:
        ticker = yf.Ticker(stock.ticker)
        hist = ticker.history(period = '1mo')
        if not hist.empty:
            stock.month_open = hist['Open'][0]
            stock.month_close = hist['Close'][-1]
            stock.delta = stock.month_close - stock.month_open
            increase = stock.delta / stock.month_open * 100
            increase_values[stock] = increase
            print(counter)
            counter = counter + 1
        else:
            stocks.remove(stock)
    counter = 0
    while(len(increase_values) != 0):
        highest_increase_stock = max(increase_values, key = increase_values.get)
        highest_increase_stock.increase_rating = len(increase_values)
        del increase_values[highest_increase_stock]
        print(counter)
        counter = counter + 1
    return stocks

def rankTrailingEPS(topStocks):
    eps_values = dict()
    counter = 0
    for stock in topStocks:
        #ticker = yf.Ticker(stock.ticker)
        #stock.info = ticker.info
        if 'trailingEps' in stock.info:
            if not isinstance(stock.info['trailingEps'], str):
                eps_values[stock] = stock.info['trailingEps']
                print(counter)
                counter = counter + 1
    counter = 0
    while(len(eps_values) != 0): 
        highest_EPS_Stock = max(eps_values, key = eps_values.get)
        highest_EPS_Stock.trailing_eps_rating = len(eps_values)
        del eps_values[highest_EPS_Stock]
        print(counter)
        counter = counter + 1
    return topStocks

def rankForwardEPS(topStocks):
    feps_values = dict()
    counter = 0
    for stock in topStocks:
        if 'forwardEps' in stock.info:
            if not isinstance(stock.info['forwardEps'], str):
                feps_values[stock] = stock.info['forwardEps']
                print(counter)
                counter = counter + 1
    counter = 0
    while(len(feps_values) != 0): 
        highest_fEPS_Stock = max(feps_values, key = feps_values.get)
        highest_fEPS_Stock.forward_eps_rating = len(feps_values)
        del feps_values[highest_fEPS_Stock]
        print(counter)
        counter = counter + 1
    return topStocks

def rankTrailingPE(topStocks):
    pe_values = dict()
    counter = 0
    for stock in topStocks:
        if 'trailingPE' in stock.info:
            if not isinstance(stock.info['trailingPE'], str):
                pe_values[stock] = stock.info['trailingPE']
                print(counter)
                counter = counter + 1
    counter = 0
    while(len(pe_values) != 0):
        best_pe_stock = min(pe_values, key = pe_values.get)
        best_pe_stock.trailing_pe_rating = len(pe_values)
        del pe_values[best_pe_stock]
        print(counter)
        counter = counter + 1
    return topStocks

def rankForwardPE(topStocks):
    fpe_values = dict()
    counter = 0
    for stock in topStocks:
        if 'forwardPE' in stock.info:
            if not isinstance(stock.info['forwardPE'], str):
                fpe_values[stock] = stock.info['forwardPE']
                print(counter)
                counter = counter + 1
    counter = 0
    while (len(fpe_values) != 0):
        best_fpe_stock = min(fpe_values, key = fpe_values.get)
        best_fpe_stock.forward_pe_rating = len(fpe_values)
        del fpe_values[best_fpe_stock]
        print(counter)
        counter = counter + 1
    return topStocks

def rankEVRev(topStocks):
    evRev_values = dict()
    counter = 0
    for stock in topStocks:
        if 'enterpriseToRevenue' in stock.info:
            if not isinstance(stock.info['enterpriseToRevenue'], str):
                evRev_values[stock] = stock.info['enterpriseToRevenue']
                print(counter)
                counter = counter + 1
    counter = 0
    while (len(evRev_values) != 0): 
        best_evRev_stock = min(evRev_values, key = evRev_values.get)
        best_evRev_stock.EVRev_rating = len(evRev_values)
        del evRev_values[best_evRev_stock]
        print(counter)
        counter = counter + 1
    return topStocks

def rankEBITDA(topStocks):
    ebit_values = dict()
    counter = 0
    for stock in topStocks:
        if 'enterpriseToEbitda' in stock.info:
            if not isinstance(stock.info['enterpriseToEbitda'], str):
                ebit_values[stock] = stock.info['enterpriseToEbitda']
                print(counter)
                counter = counter + 1
    counter = 0
    while (len(ebit_values) != 0): 
        best_ebit_stock = min(ebit_values, key = ebit_values.get)
        best_ebit_stock.Ebit_rating = len(ebit_values)
        del ebit_values[best_ebit_stock]
        print(counter)
        counter = counter + 1
    return topStocks


def getFinalStocks(topStocks, final_three): 
    stock_ranks = dict()
    for stock in topStocks:
        stock.rank = 0.4*(stock.increase_rating) + 0.2*(stock.trailing_pe_rating) + 0.15*(stock.Ebit_rating) + 0.1*(stock.trailing_eps_rating) + 0.1*(stock.EVRev_rating) + 0.025*(stock.forward_eps_rating) + 0.025*(stock.forward_pe_rating)
        stock_ranks[stock] = stock.rank
    for x in range (3):
        best_stock = max(stock_ranks, key = stock_ranks.get)
        final_three[x] = best_stock
        del stock_ranks[best_stock]
    return final_three

# =============================================================================
#     for stock in topStocks:
#         ticker = yf.Ticker(stock.ticker)
#         info = ticker.info
#         eps = info['trailingEps']
#         if eps >= 10:
#             stock.rank = 1 + 0.1*eps 
#         check = compareByRank(final_three, stock)
#         if check != None:
#             final_three.remove(check)
#             final_three.append(stock)
#     return final_three
# =============================================================================

def compareByRank(final_three, stock):
    for x in range(3):
        if stock.rank > final_three[x].rank:
            return final_three[x]
        else: 
            return None

def scrape_industryPE(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table on the page
    table = soup.find('table')

    # Extract the table headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract the table rows
    rows = []
    for row in table.find_all('tr'):
        data = [cell.text.strip() for cell in row.find_all('td')]
        if data:
            rows.append(data)

    # Create a Pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df

#url = 'https://eqvista.com/price-to-earnings-pe-ratios-by-industry/'
#industry_PE = scrape_industryPE(url)
            
top_stocks = scrape2()
top_stocks = rankStocks(top_stocks)
final_three = [Stock(0) for x in range(3)]
final_three = getFinalStocks(top_stocks, final_three)
for stock in final_three:
    print(stock.ticker)
makePDF(final_three)

# =============================================================================
# for x in range (3):
#     best_rank = max(top_stocks, key = lambda k: k.rank)
#     final_three.append(best_rank)
#     top_stocks.remove(best_rank)
# =============================================================================


