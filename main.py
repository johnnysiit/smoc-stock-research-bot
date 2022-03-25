import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pandas


#Intro 
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
ticker = YahooFinancials(stock_ticker)
yf_ticker = yf.Ticker(stock_ticker)

#Scrap data
ebit = ticker.get_ebit()
operating_income = ticker.get_operating_income()
tax = ticker.get_income_tax_expense()
net_income = ticker.get_net_income()
interest = ticker.get_interest_expense()
dividends = yf_ticker.dividends

#Datacleaning
def datacleaning(cleaninglist):
    a = cleaninglist.get(stock_ticker)
    a = a[0]
    date = list(a.keys())[0]
    a = a.get(date)
    return a


#Find data in cash 
# all_list = ticker.get_financial_stmts('annual', ['cash'])
# all_list = all_list.get('cashflowStatementHistory')
# scraped_field = datacleaning(all_list)
# depreciation = scraped_field.get('depreciation')
# capitalExpenditures = scraped_field.get('capitalExpenditures')

yf_cashflow = yf_ticker.cashflow
print(yf_cashflow)
print(yf_cashflow.loc['Total Cash From Operating Activities']["2021-09-25"])