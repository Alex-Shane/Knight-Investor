#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:14:15 2023

@author: Alex
"""

class Stock: 
    def __init__(self, ticker):
        self.ticker = ticker
        self.open = 0
        self.close = 0
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
        return f"Stock: {self.ticker}\n" \
               f"Open: {self.open}\n" \
               f"Close: {self.close}\n" \
               f"Rank: {self.rank}\n" \
               f"Delta: {self.delta}\n" \
               f"Trailing EPS Rating: {self.trailing_eps_rating}\n" \
               f"Forward EPS Rating: {self.forward_eps_rating}\n" \
               f"Industry: {self.industry}\n" \
               f"Trailing PE Rating: {self.trailing_pe_rating}\n" \
               f"Forward PE Rating: {self.forward_pe_rating}\n" \
               f"EVRev Rating: {self.EVRev_rating}\n" \
               f"Ebit Rating: {self.Ebit_rating}\n" \
               f"Increase Rating: {self.increase_rating}\n" \
               f"Info: {self.info}"f'ticker: {self.ticker}, open: {self.open}, close: {self.close}, ebit: {self.Ebit_rating}'
    
    def __repr__(self):
        return f"Stock: {self.ticker}\n" \
               f"Open: {self.open}\n" \
               f"Close: {self.close}\n" \
               f"Rank: {self.rank}\n" \
               f"Delta: {self.delta}\n" \
               f"Trailing EPS Rating: {self.trailing_eps_rating}\n" \
               f"Forward EPS Rating: {self.forward_eps_rating}\n" \
               f"Industry: {self.industry}\n" \
               f"Trailing PE Rating: {self.trailing_pe_rating}\n" \
               f"Forward PE Rating: {self.forward_pe_rating}\n" \
               f"EVRev Rating: {self.EVRev_rating}\n" \
               f"Ebit Rating: {self.Ebit_rating}\n" \
               f"Increase Rating: {self.increase_rating}\n" \
               f"Info: {self.info}"
               
               
