import yfinance as yf
import pandas as pandas
#Introduction
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
yearindex = int(input("\nPlease type in the year index you want to get \n0: Most recent year\n1: Last Year \n1: Two years ago\n2: Three years ago\nPlease type in a number: "))
print("\nPlease wait... The whole process might take over 2 minutes....\n")
yf_ticker = yf.Ticker(stock_ticker)

#Cash flow
yf_cashflow = yf_ticker.cashflow
operatingflow = int(yf_cashflow.iat[10,yearindex])
capitalExpenditures = int(yf_cashflow.iat[18,yearindex])
print (yf_cashflow)
freecashflow = int(operatingflow)-int(capitalExpenditures)
depreciation = int(yf_cashflow.iat[11,yearindex])

z = yf_cashflow.loc["Net Income"]
z = z.iat[yearindex]
print("\n",z,"\n")

#Income Statement
yf_income_statement = yf_ticker.financials
print (yf_income_statement)
operating_income = int(yf_income_statement.iat[8,yearindex])
tax = int(yf_income_statement.iat[14,yearindex])
interest_expense = int(yf_income_statement.iat[10,yearindex])
net_income = int(yf_income_statement.iat[4,yearindex])
sales = int(yf_income_statement.iat[15,yearindex])


#Balance Sheet
yf_balance = yf_ticker.balance_sheet
print (yf_balance)
shortterm_ebit = int(yf_income_statement.iat[0,yearindex])
longterm_debt = int(yf_income_statement.iat[20,yearindex])
starting_equity_balance = int(yf_balance.iat[1,yearindex])
ending_equity_balance = int(yf_balance.iat[1,(yearindex+1)])
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

#final variables
ebit = net_income + tax - interest_expense
ebitda = ebit + depreciation
equity = starting_equity_balance
debt = shortterm_ebit+longterm_debt

#======================Calculating Part=======================#

print("\n\nIndex starting here")

#Operating Margin before D&A
print("Operating Income: %s\nDepreciation: %s\nTax: %s\nSales: %s"%(operating_income,depreciation,tax,sales))
# OMBDA = (operating_income+depreciation+tax+interest)/sales
# print("Operating Margin before D&A (in%): ",OMBDA,"\n")

#Return on Equity
print("Net Income: %s\nPreferred Stock Dividends: %s\nAverage Common Stockholder's Equity: %s\n"%(net_income,avg_stock_equity))
ROE = (net_income)/avg_stock_equity
print("Return on Equity: ",ROE,"\n")

print("Ebit: %s\nInterest: %s" %(ebit,interest_expense))
EI = ebit/interest_expense
print("1C",EI)

d1 = ebitda/interest_expense
print("1D",d1)

e1 = freecashflow/debt
print("1E",e1)

f1 = debt/ebitda
print("1F",f1)

print("1g",(debt)/(debt+equity))
print ("Debt: %s\nEBIT: %s\nEBITDA: %s\n"%(debt,ebit,ebitda))

