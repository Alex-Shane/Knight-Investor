#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 16:29:13 2023

@author: Alex
"""

import yfinance as yf

conversion = {'address1': 'Address 1', 'city': 'city', 'state': 'state', 'zip': 'zip', 'country': 'country', 'phone': 'phone', 'fax': 'fax', 'website': 'website', 'industry': 'industry', 'industryDisp': 'Industry Disp', 'sector': 'sector', 'longBusinessSummary': 'Long Business Summary', 'fullTimeEmployees': 'Full-Time Employees', 'companyOfficers': 'Company Officers', 'auditRisk': 'Audit Risk', 'boardRisk': 'Board Risk', 'compensationRisk': 'Compensation Risk', 'shareHolderRightsRisk': 'Share Holder Rights Risk', 'overallRisk': 'Overall Risk', 'governanceEpochDate': 'Governance Epoch Date', 'compensationAsOfEpochDate': 'Compensation as of Epoch Date', 'maxAge': 'Max Age', 'priceHint': 'Price Hint', 'previousClose': 'Previous Close', 'open': 'open', 'dayLow': 'Daily Low', 'dayHigh': 'Daily High', 'regularMarketPreviousClose': 'Regular Market Previous Close', 'regularMarketOpen': 'Regular Market Open', 'regularMarketDayLow': 'Regular Market Day Low', 'regularMarketDayHigh': 'Regular Market Day High', 'dividendRate': 'Dividend Rate', 'dividendYield': 'Dividend Yield', 'exDividendDate': 'Ex-Dividend Date', 'payoutRatio': 'Payout Ratio', 'fiveYearAvgDividendYield': 'Five-Year Average Dividend Yield', 'beta': 'beta', 'trailingPE': 'Trailing PE', 'forwardPE': 'Forward PE', 'volume': 'volume', 'regularMarketVolume': 'Regular Market Volume', 'averageVolume': 'Average Volume', 'averageVolume10days': 'Average Volume (last 10 days)', 'averageDailyVolume10Day': 'Average Daily Volume (last 10 days)', 'bid': 'bid', 'ask': 'ask', 'bidSize': 'Bid Size', 'askSize': 'Ask Size', 'marketCap': 'Market Cap', 'fiftyTwoWeekLow': '52 Week Low', 'fiftyTwoWeekHigh': '52 Week High', 'priceToSalesTrailing12Months': 'Price to Sales Trailing (12 months)', 'fiftyDayAverage': '50 Day Average', 'twoHundredDayAverage': '200 Day Average', 'trailingAnnualDividendRate': 'Trailing Annual Dividend Rate', 'trailingAnnualDividendYield': 'Trailing Annual Dividend Yield', 'currency': 'currency', 'enterpriseValue': 'Enterprise Value', 'profitMargins': 'Profit Margins', 'floatShares': 'Float Shares', 'sharesOutstanding': 'Shares Outstanding', 'sharesShort': 'Shares Short', 'sharesShortPriorMonth': 'Shares Short (last month)', 'sharesShortPreviousMonthDate': 'Shares Short Date (last month)', 'dateShortInterest': 'Date Short Interest', 'sharesPercentSharesOut': 'Shares Percent Shares Out', 'heldPercentInsiders': 'Percent Held by Insiders', 'heldPercentInstitutions': 'Percent Held by Institutions', 'shortRatio': 'Short Ratio', 'shortPercentOfFloat': 'Short Percent of Float', 'impliedSharesOutstanding': 'Implied Shares Outstanding', 'bookValue': 'Book Value', 'priceToBook': 'Price to Book', 'lastFiscalYearEnd': 'Last Fiscal Year End', 'nextFiscalYearEnd': 'Next Fiscal year End', 'mostRecentQuarter': 'Most Recent Quarter', 'earningsQuarterlyGrowth': 'Quarterly Earnings Growth', 'netIncomeToCommon': 'Net Income to Common', 'trailingEps': 'EPS (last 12 months)', 'forwardEps': 'Forward EPS', 'pegRatio': 'PEG Ratio', 'lastSplitFactor': 'Last Split Factor', 'lastSplitDate': 'Last Split Date', 'enterpriseToRevenue': 'Enterprise to Revenue', 'enterpriseToEbitda': 'Enterprise to EBITDA', '52WeekChange': '52 Week Change', 'SandP52WeekChange': '52 Week Sand Change', 'lastDividendValue': 'Last Dividend Value', 'lastDividendDate': 'Last Dividend Date', 'exchange': 'exchange', 'quoteType': 'Quote Type', 'symbol': 'symbol', 'underlyingSymbol': 'Underlying Symbol', 'shortName': 'Short Name', 'longName': 'Long Name', 'firstTradeDateEpochUtc': 'First Trade Date Epoch UTC', 'timeZoneFullName': 'Time Zone Full Name', 'timeZoneShortName': 'Time Zone Short Name', 'uuid': 'uuid', 'messageBoardId': 'Message Board ID', 'gmtOffSetMilliseconds': 'GMT Offset (ms)', 'currentPrice': 'Current Price', 'targetHighPrice': 'Target High Price', 'targetLowPrice': 'Target Low Price', 'targetMeanPrice': 'Target Mean Price', 'targetMedianPrice': 'Target Median Price', 'recommendationMean': 'Recommendation Mean', 'recommendationKey': 'Recommendation Key', 'numberOfAnalystOpinions': '# of Analyst Opinions', 'totalCash': 'Total Cash', 'totalCashPerShare': 'Total Cash Per Share', 'ebitda': 'EBITDA', 'totalDebt': 'Total Debt', 'quickRatio': 'Quick Ratio', 'currentRatio': 'Current Ratio', 'totalRevenue': 'Total Revenue', 'debtToEquity': 'Debt to Equity', 'revenuePerShare': 'Revenue Per Share', 'returnOnAssets': 'Return on Assets', 'returnOnEquity': 'Return on Equity', 'grossProfits': 'Gross Profits', 'freeCashflow': 'Free Cash Flow', 'operatingCashflow': 'Operating Cash Flow', 'earningsGrowth': 'Earnings Growth', 'revenueGrowth': 'Revenue Growth', 'grossMargins': 'Gross Margins', 'ebitdaMargins': 'EBITDA Margins', 'operatingMargins': 'Operating Margins', 'financialCurrency': 'Financial Currency', 'trailingPegRatio': 'PEG Ratio (last 12 months)'}
def getInfo(ticker):

    try:
        if ('.HK' not in ticker):
            #adjust for errors in user input
            ticker = ticker.replace('.', '-')
            ticker = ticker.replace(" ", "")
            ticker = ticker.upper()
        print(ticker)
        stock = yf.Ticker(str(ticker))
        info = formatValues(stock.info)
        new_info = {}
        for key in info:
            if key in conversion:
                new_info[conversion[key]] = info[key]
            else:
                new_info[key] = info[key]
        if 'Company Officers' in new_info:
            new_info = formatCompanyOfficers(new_info)
        return new_info
        
    except Exception as e:
        print(e)
        return None

def formatValues(info):
    for key in info:
        value = info[key]
        if type(value) == float or type(value) == int:
            info[key] = ('{:,}'.format(value))
    return info

def formatCompanyOfficers(info):
    val = ""
    for officer in info["Company Officers"]:
        val += officer["name"] + " (" + officer["title"] + "), "
        val += "\n"
    info["Company Officers"] = val
    return info


def makeWordDict(info):
    for key in info:
        val = str(input(key + ": "))
        if len(val) > 1:
            info[key] = val
    print(info)
    
info = getInfo('TSLA')
