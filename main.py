from select import select
import yfinance as yf
import pandas as pandas
#Introduction
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
stock_ticker = str(input("请输入股票代码 Please type in the symbol of the stock: "))
yearindex = int(input("\n请输入年份 Please type in the year index you want to get \n0: Most recent year\n1: Last Year \n1: Two years ago\n2: Three years ago\nPlease type in a number: "))
print("\n请稍等，总时长可能会超过2分钟 Please wait... The whole process might take over 2 minutes....\n")
yf_ticker = yf.Ticker(stock_ticker)

def data_selecting(sheet,content):
    try:
        selector = sheet.loc[content]
        selector = selector.iat[yearindex]
        if selector == "Null" or selector == "NaN" or selector== "None" or selector == "null" or selector == "nan" or selector == "none":
            selector = 0
        selector = int(selector)
        return selector
    except:
        print ("\n!!!WARNING请注意！！！")
        print ("We could not locate the data of '%s', please type in mannually\n我们无法找到 '%s',请手动补充" %(content,content))
        print ("!!!Please be advise that data unit in Yahoo Finance is in THOUSAND. \n!!!请注意，YahooFinance的数据单位是千")
        selector = float(input(content+": "))
        return selector

#Cash flow
yf_cashflow = yf_ticker.cashflow
operatingflow = data_selecting(yf_cashflow, "Total Cash From Operating Activities")
capitalExpenditures = data_selecting(yf_cashflow, "Capital Expenditures")
depreciation = data_selecting(yf_cashflow, "Depreciation")
preferStockDividend = data_selecting(yf_cashflow, "Preferred Stock Dividends Paid")
print(yf_cashflow)

#Income Statement
yf_income_statement = yf_ticker.financials
operating_income = data_selecting(yf_income_statement, "Operating Income")
tax = data_selecting(yf_income_statement, "Income Tax Expense")
interest_expense = data_selecting(yf_income_statement, "Interest Expense")
net_income = data_selecting(yf_income_statement, "Net Income")
sales = data_selecting(yf_income_statement, "Total Revenue")
interest_income = data_selecting(yf_income_statement, "Interest Income")
print (yf_income_statement)

#Balance Sheet
yf_balance = yf_ticker.balance_sheet
print (yf_balance)
debt = data_selecting(yf_balance, "Total Debt")
starting_equity_balance = data_selecting(yf_balance, "Total Stockholder Equity")
yearindex +=1 
ending_equity_balance = data_selecting (yf_balance, "Total Stockholder Equity")
yearindex =1
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

#final variables
ebit = net_income + tax - interest_expense
ebitda = ebit + depreciation
equity = starting_equity_balance
freecashflow = operatingflow+capitalExpenditures

#======================Calculating Part=======================#


#Operating Margin before D&A
print("***Operating Margin before D&A***\nOperating Income: %s\nDepreciation: %s\nTax: %s\nInterest Income: %s\nSales: %s"%(operating_income,depreciation,tax,interest_income,sales))
OMBDA = (operating_income+depreciation+tax+interest_income)/sales
print("Operating Margin before D&A (in%): ",OMBDA,"\n")

#Return on Equity
print("***Return on Equity***\nNet Income: %s\nPrefer Stock Dividend: %s\nAverage Common Stockholder's Equity: %s\n"%(net_income,preferStockDividend,avg_stock_equity))
ROE = (net_income-preferStockDividend)/avg_stock_equity
print("Return on Equity: ",ROE,"\n")
# def ROE_Grading(ROE):
#     if ROE <= 0.162:
#         return 1
#     elif 0.162 < ROE <= 0.172:
#         return 2
#     elif 0.172 < ROE <= 0.198:
#         return 3
#     elif 0.198 < ROE <= 0.205:
#         return 4
#     elif 0.205 < ROE <= 0.222:
#         return 5
#     elif 0.222 < ROE :
#         return 6
# print("Grade of ROE: ",ROE_Grading(ROE))

#EBIT Interest Coverage
print("***EBIT Interest Coverage***\nEbit: %s\nInterest: %s" %(ebit,interest_expense))
EI = ebit/(interest_expense*-1)
print("EBIT Interest Coverage",EI)
#8.7% - 1，12.4% - 2，15.2% - 3，21.8% - 4，28.4% - 5，27% - 6
# def EI_Grading(EI):
#     if EI <= 0.087:
#         return 1
#     elif 0.087 < EI <= 0.124:
#         return 2
#     elif 0.124 < EI <= 0.152:
#         return 3
#     elif 0.152 < EI <= 0.218:
#         return 4
#     elif 0.218 < EI <= 0.284:
#         return 5
#     elif 0.284 < EI <= 0.27:
#         return 6


print("\n***EBITDA Interest Coverage***\nEbitda: %s\nInterest: %s" %(ebitda,interest_expense))
EIC = ebitda/(interest_expense*-1)
print("EBITDA Interest Coverage ",EIC)

print("\n***Free Cash Flow to Debt***\nFree Cash Flow: %s\nTotal Debt: %s" %(freecashflow,debt))
FCFTB = freecashflow/debt
print("Free Cash Flow to Debt",FCFTB)

print("\n***Debt to EBITDA***\nTotal Debt: %s\nEbitda: %s" %(debt,ebitda))
DTE = debt/ebitda
print("Debt to EBITDA",DTE)

print("\n***Debt to (Debt + Equity)***\nTotal Debt: %s\nTotal Stockholder Equity: %s" %(debt,equity))
DTDE=(debt)/(debt+equity)
print ("Debt to (Debt + Equity)",DTDE)

