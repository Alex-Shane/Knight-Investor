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

class Stock: 
    def __init__(self, ticker, month_open, month_close):
        self.ticker = ticker
        self.month_open = month_open
        self.month_close = month_close
        self.delta = month_close - month_open
        return
        
    def __str__(self):
        return f'ticker: {self.ticker}, open: {self.month_open}, close: {self.month_close}'
    
    def __repr__(self):
        return f'ticker: {self.ticker}, open: {self.month_open}, close: {self.month_close}'


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
    if stock.delta > currentTopStocks[0].delta:
        return currentTopStocks[0]
    elif stock.delta > currentTopStocks[1].delta:
        return currentTopStocks[1]
    elif stock.delta > currentTopStocks[2].delta:
        return currentTopStocks[2]
    else:
        return None

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
    top_stocks = [Stock(0,0,0) for x in range(3)]
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

def makePDF(top_stocks):
    context = {}
    context['s1'] = yf.Ticker(top_stocks[0].ticker).info['longName']
    context['s1.ticker'] = top_stocks[0].ticker
    context['d1'] = f'{top_stocks[0].delta / top_stocks[0].month_open * 100:.2f}'
    configNews(yf.Ticker(top_stocks[0].ticker).get_news(), context, 1)
    context['s2'] = yf.Ticker(top_stocks[1].ticker).info['longName']
    context['s2.ticker'] = top_stocks[1].ticker
    context['d2'] = f'{top_stocks[1].delta / top_stocks[1].month_open * 100:.2f}'
    configNews(yf.Ticker(top_stocks[1].ticker).get_news(), context, 4)
    context['s3'] = yf.Ticker(top_stocks[2].ticker).info['longName']
    context['s3.ticker'] = top_stocks[2].ticker
    context['d3'] = f'{top_stocks[2].delta / top_stocks[2].month_open * 100:.2f}'
    configNews(yf.Ticker(top_stocks[2].ticker).get_news(), context, 7)
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    print(context)
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output_text, 'stock_report.pdf', configuration=config)

def configNews(news, context, num):
    for x in range(0, 3):
        title = news[x]['title']
        link = news[x]['link']
        title_string = f'news{num}.title'
        link_string = f'news{num}.link'
        print(title_string)
        context[title_string] = title
        context[link_string] = link
        num = num + 1
    return context


top_stocks = scrape()
file = makePDF(top_stocks)

print("\n" + "The best peforming stocks over the past month by delta stock price: ")
print("\n")
for stock in top_stocks:
    percent_gained = f'{stock.delta / stock.month_open * 100:.2f}'
    delta = f'{stock.delta:.2f}'
    print(f'ticker: {stock.ticker}, delta: {delta}, percent gain = {percent_gained}%')
    print("\n")
    ticker = yf.Ticker(stock.ticker)
    news = ticker.get_news()
    print(f"Follow these links to read more about {stock.ticker}:" + "\n")
    for article in news:
        title = article['title']
        link = article['link']
        print(f'{title}: {link}' + "\n")
