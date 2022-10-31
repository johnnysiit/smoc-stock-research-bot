#Author: Juanxi Xue
from webbrowser import get
import yfinance as yf

def get_price(ticker):
    yfinance = yf.Ticker(ticker)
    hist = yfinance.history(period="5y")
    hist = hist.drop(columns=["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"])
    monthly_price = hist.resample("M").mean()
    price_list = []
    for i in monthly_price["Close"]:
        price_list.append(float(i))
    stock_return = []
    for i in range(len(price_list)-1):
        stock_return.append((price_list[i+1]-price_list[i])/price_list[i])
    return stock_return