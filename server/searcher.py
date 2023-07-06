#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 16:29:13 2023

@author: Alex
"""

import yfinance as yf

def getInfo(ticker):

    try:
        if ('.HK' in ticker):
            #adjust for errors in user input
            ticker = ticker.replace('.', '-')
            ticker = ticker.replace(" ", "")
            ticker = ticker.upper()
        print(ticker)
        stock = yf.Ticker(str(ticker))
        return stock.info
        
    except Exception as e:
        print(e)
        return None



