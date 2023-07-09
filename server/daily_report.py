#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 17:16:54 2023

@author: Alex
"""

import jinja2
import pdfkit
from Scraper import Scraper
from PDFHelper import PDFHelper as Helper


def rankStocks(stocks):
    """
    Ranks the given list of stocks based on the percent increase in stock price over the past day.

    Args:
       stocks (list): A list of stocks to be ranked.

    Returns:
       list: A new list of stocks with updated rank 

    """
    increase_values = dict()
    for stock in stocks[:]:
        ticker = stock.ticker_obj
        try:
            hist = ticker.history(period = '1d')
            stock.open = hist['Open'][0]
            #if stock opens at zero, most likely delisted or something weird
            if stock.open == 0:
                continue
            stock.close = hist['Close'][-1]
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
    """
    Find the three highest-ranked stocks from the given list of stocks

    Args:
        stocks (list): A list of stocks, where each stock has many attributes
                       Each stock should have the following attributes:
                       - 'ticker' (str): The symbol of the stock.
                       - 'rank' (int): The ranking of the stock.

    Returns:
        list: A list containing the three highest-ranked stocks from the given list.
    """
    winners = list()
    for x in range(3):
        winner = max(stocks, key = lambda k: k.rank)
        #get needed info for stock in report
        winner.info = winner.ticker_obj.info
        while winner.info['averageVolume'] == 0 or winner.open == 0:
            stocks.remove(winner)
            winner = max(stocks, key = lambda k: k.rank)
        winners.append(winner)
        stocks.remove(winner)
    return winners

def findLosers(stocks):
    """
    Find the three lowest-ranked stocks from the given list of stocks

    Args:
        stocks (list): A list of stocks, where each stock has many attributes
                       Each stock should have the following attributes:
                       - 'ticker' (str): The symbol of the stock.
                       - 'rank' (int): The ranking of the stock.

    Returns:
        list: A list containing the three lowest-ranked stocks from the given list.
    """
    losers = list()
    for x in range(3):
        loser = min(stocks, key = lambda k: k.rank)
        #get needed info for stock in report
        loser.info = loser.ticker_obj.info 
        while loser.info['averageVolume'] == 0 or loser.open == 0:
            stocks.remove(loser)
            loser = min(stocks, key = lambda k: k.rank)
        losers.append(loser)
        stocks.remove(loser)
    return losers

def makePDF(winners, losers, exchange):
    """
    Generates a PDF file containing relevant information and current news about the highest ranked stocks for current month.

    Args:
        winners (list): A list of the highest ranked stocks for the day
        losers (list): A list of the lowest ranked stocks for the day
        exchange (str): name of the stock exchange being reported on

    """
    context = {}
    helper = Helper()
    helper.makeTitle(exchange, context) 
    scraper = Scraper()
    scraper.getExchangeInfo(exchange, context, 'day')
    configureWinners(context, winners)
    configureLosers(context, losers)
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('./templates/daily_report.html')
    output_text = template.render(context)
    config = pdfkit.configuration()
    file_name = helper.getFileName(exchange, 'day')
    pdfkit.from_string(output_text, file_name, configuration=config)
    return (context, file_name)
    
def configureWinners(context, winners):
    """
    Configure the context dictionary with information from the winning stocks for the final report.

    Args:
        context (dict): A dictionary containing the context information for the final report.

        winning_stocks (list): A list of stocks representing the winning stocks.

    Returns:
        nothing, just updates context dictionary
    """
    winner1 = winners[0]
    context['s1'] = winner1.info['longName']
    context['inc1'] = f'{winner1.delta / winner1.open * 100:.2f}'
    context['s1ticker'] = winner1.ticker
    context['price1'] = ('{:,}'.format(round(winner1.info['currentPrice'], 2)))
    context['mcap1'] = ('{:,}'.format(winner1.info['marketCap']))
    helper = Helper()
    context['i1'] = helper.getIndustry(winner1)
    helper.handleDividend(winner1, context, 1)
    helper.handleRecommendation(winner1, context, 1)
    winner2 = winners[1]
    context['s2'] = winner2.info['longName']
    context['inc2'] = f'{winner2.delta / winner2.open * 100:.2f}'
    context['s2ticker'] = winner2.ticker
    context['price2'] = ('{:,}'.format(round(winner2.info['currentPrice'], 2)))
    context['mcap2'] = ('{:,}'.format(winner2.info['marketCap']))
    context['i2'] = helper.getIndustry(winner2)
    helper.handleDividend(winner2, context, 2)
    helper.handleRecommendation(winner2, context, 2)
    winner3 = winners[2]
    context['s3'] = winner3.info['longName']
    context['inc3'] = f'{winner3.delta / winner3.open * 100:.2f}'
    context['s3ticker'] = winner3.ticker
    context['price3'] = ('{:,}'.format(round(winner3.info['currentPrice'], 2)))
    context['mcap3'] = ('{:,}'.format(winner3.info['marketCap']))
    context['i3'] = helper.getIndustry(winner3)
    helper.handleDividend(winner3, context, 3)
    helper.handleRecommendation(winner3, context, 3)

def configureLosers(context, losers):
    """
    Configure the context dictionary with information from the losing stocks for the final report.

    Args:
        context (dict): A dictionary containing the context information for the final report.

        winning_stocks (list): A list of stocks representing the losing stocks.

    Returns:
        nothing, just updates context dictionary
    """
    loser1 = losers[0]
    context['s4'] = loser1.info['longName']
    context['inc4'] = f'{loser1.delta / loser1.open * -100:.2f}'
    context['s4ticker'] = loser1.ticker
    context['price4'] = ('{:,}'.format(round(loser1.info['currentPrice'], 2)))
    context['mcap4'] = ('{:,}'.format(loser1.info['marketCap']))
    helper = Helper()
    context['i4'] = helper.getIndustry(loser1)
    helper.handleDividend(loser1, context, 4)
    helper.handleRecommendation(loser1, context, 4)
    loser2 = losers[1]
    context['s5'] = loser2.info['longName']
    context['inc5'] = f'{loser2.delta / loser2.open * -100:.2f}'
    context['s5ticker'] = loser2.ticker
    context['price5'] = ('{:,}'.format(round(loser2.info['currentPrice'], 2)))
    context['mcap5'] = ('{:,}'.format(loser2.info['marketCap']))
    context['i5'] = helper.getIndustry(loser2)
    helper.handleDividend(loser2, context, 5)
    helper.handleRecommendation(loser2, context, 5)
    loser3 = losers[2]
    context['s6'] = loser3.info['longName']
    context['inc6'] = f'{loser3.delta / loser3.open * -100:.2f}'
    context['s6ticker'] = loser3.ticker
    context['price6'] = ('{:,}'.format(round(loser3.info['currentPrice'], 2)))
    context['mcap6'] = ('{:,}'.format(loser3.info['marketCap']))
    context['i6'] = helper.getIndustry(loser3)
    helper.handleDividend(loser3, context, 6)
    helper.handleRecommendation(loser3, context, 6)

def run(exchange, industry = None):
    if exchange == 'NYSE':
        stocks = Scraper.scrapeNYSE('day', industry)
    elif exchange == 'NASDAQ100':
        stocks = Scraper.scrapeNASDAQ100('day', industry)
    elif exchange == 'DOW':
        stocks = Scraper.scrapeDOW('day', industry)
    elif exchange == 'NASDAQ':
        stocks = Scraper.scrapeNASDAQ('day', industry)
    elif exchange == 'HKSE':
        stocks = Scraper.scrapeHKSE('day', industry)
    else:
        stocks = Scraper.scrapeSP500('day', industry)
    ranked_stocks = rankStocks(stocks)
    winners = findWinners(ranked_stocks)
    losers = findLosers(ranked_stocks)
    return makePDF(winners, losers, exchange)













