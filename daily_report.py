#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 17:16:54 2023

@author: Alex
"""

import yfinance as yf
import jinja2
import pdfkit
from Scraper import Scraper
from PDFHelper import PDFHelper as Helper
from Stock import Stock


def rankStocks(stocks):
    """
    Ranks the given list of stocks based on the percent increase in stock price over the past day.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated rank 

    """
    increase_values = dict()
    for stock in stocks:
        ticker = yf.Ticker(stock.ticker)
        try:
            hist = ticker.history(period = '1d')
            stock.open = hist['Open'][0]
            print(stock.open)
            stock.close = hist['Close'][-1]
            print(stock.close)
            stock.delta = stock.close - stock.open
            increase = stock.delta / stock.open * 100
            increase_values[stock] = increase
        except:
            stocks.remove(stock)
    while(len(increase_values) != 0):
        highest_increase_stock = max(increase_values, key = increase_values.get)
        highest_increase_stock.rank = len(increase_values)
        del increase_values[highest_increase_stock]
    return stocks

def findWinners(stocks):
    winners = list()
    for x in range(3):
        winner = max(stocks, key = lambda k: k.rank)
        while winner.info['averageVolume'] == 0:
            stocks.remove(winner)
            winner = max(stocks, key = lambda k: k.rank)
        winners.append(winner)
        stocks.remove(winner)
    return winners

def findLosers(stocks):
    losers = list()
    for x in range(3):
        loser = min(stocks, key = lambda k: k.rank)
        while loser.info['averageVolume'] == 0:
            stocks.remove(loser)
            loser = min(stocks, key = lambda k: k.rank)
        losers.append(loser)
        stocks.remove(loser)
    return losers

def makePDF(winners, losers):
    context = {}
    scraper = Scraper()
    scraper.getSPIndexInfo(context, 'day')
    configureWinners(context, winners)
    configureLosers(context, losers)
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('daily_report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(output_text, 'daily_stock_report.pdf', configuration=config)
    
def configureWinners(context, winners):
    winner1 = winners[0]
    context['s1'] = winner1.info['longName']
    context['inc1'] = f'{winner1.delta / winner1.open * 100:.2f}'
    context['s1ticker'] = winner1.ticker
    context['price1'] = ('{:,}'.format(round(winner1.info['currentPrice'], 2)))
    context['mcap1'] = ('{:,}'.format(winner1.info['marketCap']))
    context['i1'] = winner1.info['industry']
    helper = Helper()
    helper.handleDividend(winner1, context, 1)
    helper.handleRecommendation(winner1, context, 1)
    winner2 = winners[1]
    context['s2'] = winner2.info['longName']
    context['inc2'] = f'{winner2.delta / winner2.open * 100:.2f}'
    context['s2ticker'] = winner2.ticker
    context['price2'] = ('{:,}'.format(round(winner2.info['currentPrice'], 2)))
    context['mcap2'] = ('{:,}'.format(winner2.info['marketCap']))
    context['i2'] = winner2.info['industry']
    helper.handleDividend(winner2, context, 2)
    helper.handleRecommendation(winner2, context, 2)
    winner3 = winners[2]
    context['s3'] = winner3.info['longName']
    context['inc3'] = f'{winner3.delta / winner3.open * 100:.2f}'
    context['s3ticker'] = winner3.ticker
    context['price3'] = ('{:,}'.format(round(winner3.info['currentPrice'], 2)))
    context['mcap3'] = ('{:,}'.format(winner3.info['marketCap']))
    context['i3'] = winner3.info['industry']
    helper.handleDividend(winner3, context, 3)
    helper.handleRecommendation(winner3, context, 3)

def configureLosers(context, losers):
    loser1 = losers[0]
    context['s4'] = loser1.info['longName']
    print(loser1)
    context['inc4'] = f'{loser1.delta / loser1.open * -100:.2f}'
    context['s4ticker'] = loser1.ticker
    context['price4'] = ('{:,}'.format(round(loser1.info['currentPrice'], 2)))
    context['mcap4'] = ('{:,}'.format(loser1.info['marketCap']))
    context['i4'] = loser1.info['industry']
    helper = Helper()
    helper.handleDividend(loser1, context, 4)
    helper.handleRecommendation(loser1, context, 4)
    loser2 = losers[1]
    context['s5'] = loser2.info['longName']
    context['inc5'] = f'{loser2.delta / loser2.open * -100:.2f}'
    context['s5ticker'] = loser2.ticker
    context['price5'] = ('{:,}'.format(round(loser2.info['currentPrice'], 2)))
    context['mcap5'] = ('{:,}'.format(loser2.info['marketCap']))
    context['i5'] = loser2.info['industry']
    helper.handleDividend(loser2, context, 5)
    helper.handleRecommendation(loser2, context, 5)
    loser3 = losers[2]
    context['s6'] = loser3.info['longName']
    context['inc6'] = f'{loser3.delta / loser3.open * -100:.2f}'
    context['s6ticker'] = loser3.ticker
    context['price6'] = ('{:,}'.format(round(loser3.info['currentPrice'], 2)))
    context['mcap6'] = ('{:,}'.format(loser3.info['marketCap']))
    context['i6'] = loser3.info['industry']
    helper.handleDividend(loser3, context, 6)
    helper.handleRecommendation(loser3, context, 6)


test = Scraper.scrapeNYSE()

stocks = Scraper.scrapeNYSE()
ranked_stocks = rankStocks(stocks)
winners = findWinners(ranked_stocks)
losers = findLosers(ranked_stocks)
makePDF(winners, losers)

history = yf.Ticker('APAM').history(period='1d')






