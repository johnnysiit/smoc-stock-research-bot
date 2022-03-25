import yfinance as yf
from yahoofinancials import YahooFinancials

#Intro 
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
ticker = YahooFinancials(stock_ticker)

#Scrap data
ebit = ticker.get_ebit()
print (ebit)