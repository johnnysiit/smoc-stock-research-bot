from select import select
import yfinance as yf
import pandas as pandas
#Introduction
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("Please type in the symbol of the stock: "))
yearindex = int(input("\nPlease type in the year index you want to get \n0: Most recent year\n1: Last Year \n1: Two years ago\n2: Three years ago\nPlease type in a number: "))
print("\nPlease wait... The whole process might take over 2 minutes....\n")
yf_ticker = yf.Ticker(stock_ticker)

def data_selecting(sheet,content):
    # print (yf_cashflow)
    # print (content)
    try:
        selector = sheet.loc[content]
        selector = selector.iat[yearindex]
        if selector == "Null" or selector == "NaN" or selector== "None":
            selector = 0
        selector = int(selector)
        return selector
    except:
        selector =float(input("\nThe data (%s) is not available, please type in mannually\n"%content))
        return 0

#Cash flow
yf_cashflow = yf_ticker.cashflow
operatingflow = data_selecting(yf_cashflow, "Total Cash From Operating Activities")
capitalExpenditures = data_selecting(yf_cashflow, "Capital Expenditures")
depreciation = data_selecting(yf_cashflow, "Depreciation")



#Income Statement
yf_income_statement = yf_ticker.financials
print (yf_income_statement)
operating_income = data_selecting(yf_income_statement, "Operating Income")
tax = data_selecting(yf_income_statement, "Income Tax Expense")
interest_expense = data_selecting(yf_income_statement, "Interest Expense")
net_income = data_selecting(yf_income_statement, "Net Income")
sales = data_selecting(yf_income_statement, "Total Revenue")


#Balance Sheet
yf_balance = yf_ticker.balance_sheet
print (yf_balance)
shortterm_debt = data_selecting(yf_balance, "Short Long Term Debt")
longterm_debt = data_selecting(yf_balance, "Long Term Debt")
starting_equity_balance = data_selecting(yf_balance, "Total Stockholder Equity")
yearindex +=1 
ending_equity_balance = data_selecting (yf_balance, "Total Stockholder Equity")
yearindex =1
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

#final variables
ebit = net_income + tax - interest_expense
ebitda = ebit + depreciation
equity = starting_equity_balance
debt = shortterm_debt+longterm_debt
freecashflow = operatingflow-capitalExpenditures

#======================Calculating Part=======================#

print("\n\nIndex starting here")

#Operating Margin before D&A
print("Operating Income: %s\nDepreciation: %s\nTax: %s\nSales: %s"%(operating_income,depreciation,tax,sales))
# OMBDA = (operating_income+depreciation+tax+interest)/sales
# print("Operating Margin before D&A (in%): ",OMBDA,"\n")

#Return on Equity
print("Net Income: %s\nAverage Common Stockholder's Equity: %s\n"%(net_income,avg_stock_equity))
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

