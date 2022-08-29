#Author: Juanxi Xue
import yfinance as yf

def get_cv(ticker):
    yfinance = yf.Ticker(ticker)
    hist = yfinance.history(period="6mo")
    price_list = []
    for i in hist["Open"]:
        price_list.append(float(i))
    for k in hist["Close"]:
        price_list.append(float(k))
    for j in hist["High"]:
        price_list.append(float(j))
    for l in hist["Low"]:
        price_list.append(float(l))
    print (price_list)
    #get mean on price list
    mean = sum(price_list)/len(price_list)
    # get standard deviation on price list
    std = sum([(i-mean)**2 for i in price_list])/len(price_list)
    std = std**0.5
    return std/mean
print (get_cv("CRMT"))

