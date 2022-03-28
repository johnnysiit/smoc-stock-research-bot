import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pandas


#Intro 
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
print("\nPlease wait... The whole process might take over 2 minutes....\n")
ticker = YahooFinancials(stock_ticker)
yf_ticker = yf.Ticker(stock_ticker)

#Scrap data
ebit = int(ticker.get_ebit())
operating_income = int(ticker.get_operating_income())
tax = int(ticker.get_income_tax_expense())
net_income = int(ticker.get_net_income())
interest = int(ticker.get_interest_expense())
sales = int(ticker.get_total_revenue())

#Datacleaning
def datacleaning(cleaninglist):
    a = cleaninglist.get(stock_ticker)
    a = a[0]
    date = list(a.keys())[0]
    a = a.get(date)
    return a

#Find data in cash 
all_list = ticker.get_financial_stmts('annual', ['cash'])
all_list = all_list.get('cashflowStatementHistory')
scraped_field = datacleaning(all_list)
depreciation = int(scraped_field.get('depreciation'))
capitalExpenditures = int(scraped_field.get('capitalExpenditures'))
dividends = int(scraped_field.get('dividendsPaid'))

#Get Operating Cash Flow
yf_cashflow = yf_ticker.cashflow
operatingflow = int(yf_cashflow.iat[10,0])
freecashflow = int(operatingflow)-int(capitalExpenditures)

#Get Balance and equity
yf_balance = yf_ticker.balance_sheet
debt = int(yf_balance.iat[0,0])
starting_equity_balance = int(yf_balance.iat[1,0])
ending_equity_balance = int(yf_balance.iat[1,1])
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

#final variables
ebitda = ebit - depreciation
equity = starting_equity_balance

#======================Calculating Part=======================#
#1a

print("\n\nIndex starting here")

#Operating Margin before D&A
print("Operating Income: %s\nDepreciation: %s\nTax: %s\nInterest: %s\nSales: %s"%(operating_income,depreciation,tax,interest,sales))
output = (operating_income+depreciation+tax+interest)/sales
print("Operating Margin before D&A (in%): ",output,"\n")

#Return on Equity
print("Net Income: %s\nPreferred Stock Dividends: %s\nAverage Common Stockholder's Equity: %s\n"%(net_income,dividends,avg_stock_equity))
output = (net_income-dividends)/avg_stock_equity
print("Return on Equity: ",output,"\n")

c1 = ebit/interest
print("1C",c1)

d1 = ebitda/interest
print("1D",d1)

e1 = freecashflow/debt
print("1E",e1)

f1 = debt/ebitda
print("1F",f1)

print("1g",(debt)/(debt+equity))

