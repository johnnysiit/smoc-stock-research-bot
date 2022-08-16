from dataclasses import replace
from operator import index
from webbrowser import get
from yahoo_fin.options import *
import yfinance as yf
from datetime import datetime


class OptionPrice:
    def __init__(self, ticker,price):
        self.ticker = ticker
        self.yf = yf.Ticker(ticker)
        self.price = price
        dd = self.yf.options[0]
        dd = datetime.strptime(dd, '%Y-%m-%d')
        self.expiration = dd.strftime("%m/%d/%Y")
    
    def make_strike_dict(self):
        index_strike = dict()
        count = 0
        for i in self.full_list["Strike"]:
            index_strike[count] = i
            count += 1
        num_index, strike = min(index_strike.items(), key=lambda x: abs(self.price - x[1]))
        return num_index, strike
    
    def avg_cal(self):
        last_price = float(self.final_list["Last Price"])
        bid_price = float(self.final_list["Bid"])
        ask_price = float(self.final_list["Ask"])
        mid_price = float((bid_price + ask_price)/2)
        return (last_price + mid_price + ask_price)/3

    def get_call(self):
        self.full_list = get_calls(self.ticker,self.expiration)
        index = self.make_strike_dict()
        self.final_list = self.full_list.iloc[index[0]]
        avg_price = self.avg_cal()
        return avg_price
    
    def get_put(self):
        self.full_list = get_puts(self.ticker,self.expiration)
        index = self.make_strike_dict()
        self.final_list = self.full_list.iloc[index[0]]
        avg_price = self.avg_cal()
        return avg_price



