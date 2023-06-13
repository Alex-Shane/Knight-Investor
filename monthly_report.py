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

    
def makePDF(final_three, exchange):
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
    context['s1'] = final_three[0].info['longName']
    context['s1ticker'] = final_three[0].ticker
    context['d1'] = f'{final_three[0].delta / final_three[0].open * 100:.2f}'
    cur1 = round(final_three[0].info['currentPrice'], 2)
    cur1 = ('{:,}'.format(cur1))
    context['price1'] = cur1
    mcap1 = ('{:,}'.format(final_three[0].info['marketCap']))
    context['mcap1'] = mcap1
    context['i1'] = final_three[0].info['industry'] 
    helper.handleDividend(final_three[0], context, 1)
    helper.handleRecommendation(final_three[0], context, 1)
    context['link1'] = f"https://finance.yahoo.com/quote/{final_three[0].ticker}/news?p={final_three[0].ticker}"
    #helper.configNews(yf.Ticker(final_three[0].ticker).get_news(), context, 1)
    context['s2'] = final_three[1].info['longName']
    context['s2ticker'] = final_three[1].ticker
    context['d2'] = f'{final_three[1].delta / final_three[1].open * 100:.2f}'
    cur2 = round(final_three[1].info['currentPrice'], 2)
    cur2 = ('{:,}'.format(cur2))
    context['price2'] = cur2
    mcap2 = ('{:,}'.format(final_three[1].info['marketCap']))
    context['mcap2'] = mcap2
    context['i2'] = final_three[1].info['industry']
    helper.handleDividend(final_three[1], context, 2)
    helper.handleRecommendation(final_three[1], context, 2)
    #helper.configNews(yf.Ticker(final_three[1].ticker).get_news(), context, 4)
    context['link2'] = f"https://finance.yahoo.com/quote/{final_three[1].ticker}/news?p={final_three[1].ticker}"
    context['s3'] = final_three[2].info['longName']
    context['s3ticker'] = final_three[2].ticker
    context['d3'] = f'{final_three[2].delta / final_three[2].open * 100:.2f}'
    cur3 = round(final_three[2].info['currentPrice'], 2)
    cur3 = ('{:,}'.format(cur3))
    context['price3'] = cur3
    mcap3 = ('{:,}'.format(final_three[2].info['marketCap']))
    context['mcap3'] = mcap3
    context['i3'] = final_three[2].info['industry']
    helper.handleDividend(final_three[2], context, 3)
    helper.handleRecommendation(final_three[2], context, 3)
    #helper.configNews(yf.Ticker(final_three[2].ticker).get_news(), context, 7)
    context['link3'] = f"https://finance.yahoo.com/quote/{final_three[2].ticker}/news?p={final_three[2].ticker}"
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    file_name = helper.getFileName(exchange, 'month')
    pdfkit.from_string(output_text, file_name, configuration=config)


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
    stock_ranks = dict()
    for stock in stocks:
        stock.rank = 0.4*(stock.increase_rating) + 0.2*(stock.trailing_pe_rating) + 0.15*(stock.Ebit_rating) + 0.1*(stock.trailing_eps_rating) + 0.1*(stock.EVRev_rating) + 0.025*(stock.forward_eps_rating) + 0.025*(stock.forward_pe_rating)
        stock_ranks[stock] = stock.rank
    best_stocks = list()
    if len(stock_ranks) < 3:
        size = len(stock_ranks)
    else:
        size = 3
    for x in range (size):
        best_stock = max(stock_ranks, key = stock_ranks.get)
        best_stocks.append(best_stock)
        del stock_ranks[best_stock]
    return best_stocks

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
    
stocks = Scraper.scrapeNYSE('month', 'Semiconductors')
rankedStocks = rankStocks(stocks)
best_stocks = getFinalStocks(rankedStocks)
makePDF(best_stocks, 'NYSE')






