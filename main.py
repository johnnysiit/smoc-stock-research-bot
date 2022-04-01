import yfinance as yf
import pandas as pandas
#Introduction
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
yearindex = int(input("\nPlease type in the year index you want to get \n0: Most recent year\n1: Last Year \n1: Two years ago\n2: Three years ago\nPlease type in a number: "))
print("\nPlease wait... The whole process might take over 2 minutes....\n")
yf_ticker = yf.Ticker(stock_ticker)

#Cashflow
yf_cashflow = yf_ticker.cashflow
operatingflow = int(yf_cashflow.iat[10,yearindex])
capitalExpenditure = int(yf_cashflow.iat[18,yearindex])
print (yf_cashflow)
# freecashflow = int(operatingflow)-int(capitalExpenditures)





#Get Balance and equity
yf_balance = yf_ticker.balance_sheet
print (yf_balance)
debt = int(yf_balance.iat[0,yearindex])
starting_equity_balance = int(yf_balance.iat[1,yearindex])
ending_equity_balance = int(yf_balance.iat[1,(yearindex+1)])
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

# #final variables
# ebitda = ebit - depreciation
# equity = starting_equity_balance

# #======================Calculating Part=======================#

# print("\n\nIndex starting here")

# #Operating Margin before D&A
# print("Operating Income: %s\nDepreciation: %s\nTax: %s\nInterest: %s\nSales: %s"%(operating_income,depreciation,tax,interest,sales))
# OMBDA = (operating_income+depreciation+tax+interest)/sales
# print("Operating Margin before D&A (in%): ",OMBDA,"\n")

# #Return on Equity
# print("Net Income: %s\nPreferred Stock Dividends: %s\nAverage Common Stockholder's Equity: %s\n"%(net_income,dividends,avg_stock_equity))
# ROE = (net_income-dividends)/avg_stock_equity
# print("Return on Equity: ",ROE,"\n")

# print("Ebit: %\nInterest: %"%(ebit,interest))
# EI = ebit/interest
# print("1C",EI)

# d1 = ebitda/interest
# print("1D",d1)

# e1 = freecashflow/debt
# print("1E",e1)

# f1 = debt/ebitda
# print("1F",f1)

# print("1g",(debt)/(debt+equity))

