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
print("\n***Operating Margin before D&A***\nOperating Income: %s\nDepreciation: %s\nTax: %s\nInterest Income: %s\nSales: %s"%(operating_income,depreciation,tax,interest_income,sales))
OMBDA = (operating_income+depreciation+tax+interest_income)/sales
print("Operating Margin before D&A (in%): ",OMBDA)
#16.2% - 1, 17.2% - 2, 17% - 3，19.8% - 4，26.5% - 5，22.2% - 6
def OMBDA_Grading(OMBDA):
    if OMBDA <= 0.162:
        return 0
    elif 0.162 < OMBDA <= 0.172:
        return 1
    elif 0.172 < OMBDA <= 0.198:
        return 2
    elif 0.198 < OMBDA <= 0.205:
        return 3
    elif 0.205 < OMBDA <= 0.222:
        return 4
    elif 0.222 < OMBDA <= 0.265:
        return 6
    elif 0.265 < OMBDA :
        return 5
print("Grade of ROE: ",OMBDA_Grading(OMBDA))

#Return on Equity
print("\n***Return on Equity***\nNet Income: %s\nPrefer Stock Dividend: %s\nAverage Common Stockholder's Equity: %s"%(net_income,preferStockDividend,avg_stock_equity))
ROE = (net_income-preferStockDividend)/avg_stock_equity
print("Return on Equity: ",ROE)
ROE = ROE/100
#8.7% - 1，12.4% - 2，15.2% - 3，21.8% - 4，28.4% - 5，27% - 6
def ROE_Grading(ROE):
    if ROE <= 0.087:
        return 0
    elif 0.087 < ROE <= 0.124:
        return 1
    elif 0.124 < ROE <= 0.152:
        return 2
    elif 0.152 < ROE <= 0.218:
        return 3
    elif 0.218 < ROE <= 0.284:
        return 4
    elif 0.284 < ROE <= 0.27:
        return 5
    elif 0.27 < ROE :
        return 6
print("Grade of ROE: ",ROE_Grading(ROE))

#EBIT Interest Coverage
print("\n***EBIT Interest Coverage***\nEbit: %s\nInterest: %s" %(ebit,interest_expense))
EI = ebit/(interest_expense*-1)
print("EBIT Interest Coverage",EI)
#1.4 - 1，3.4 - 2，5.8 - 3，11.2 - 4，16.4 - 5，26.2 - 6
def EI_Grading(EI):
    if EI <= 1.4:
        return 0
    elif 1.4 < EI <= 3.4:
        return 1
    elif 3.4 < EI <= 5.8:
        return 2
    elif 5.8 < EI <= 11.2:
        return 3
    elif 11.2 < EI <= 16.4:
        return 4
    elif 16.4 < EI <= 26.2:
        return 5
    elif 26.2 < EI :
        return 6
print("Grade of EI: ",EI_Grading(EI))

#EBITDA Interest Coverage
print("\n***EBITDA Interest Coverage***\nEbitda: %s\nInterest: %s" %(ebitda,interest_expense))
EIC = ebitda/(interest_expense*-1)
print("EBITDA Interest Coverage ",EIC)
#2.3 - 1，4.8 - 2，7.8 - 3，13.5 - 4，19.5 - 5，32 - 6
def EIC_Grading(EIC):
    if EIC <= 2.3:
        return 0
    elif 2.3 < EIC <= 4.8:
        return 1
    elif 4.8 < EIC <= 7.8:
        return 2
    elif 7.8 < EIC <= 13.5:
        return 3
    elif 13.5 < EIC <= 19.5:
        return 4
    elif 19.5 < EIC <= 32:
        return 5
    elif 32 < EIC :
        return 6
print("Grade of EIC: ",EIC_Grading(EIC))

#Free Cash Flow to Debt Ratio
print("\n***Free Cash Flow to Debt***\nFree Cash Flow: %s\nTotal Debt: %s" %(freecashflow,debt))
FCFTB = freecashflow/debt
print("Free Cash Flow to Debt",FCFTB)
#11.5% - 1，25.7% - 2，35.5% - 3，54.5% - 4，79.2% - 5，155.5% - 6
def FCFTB_Grading(FCFTB):
    if FCFTB <= 0.115:
        return 0
    elif 0.115 < FCFTB <= 0.257:
        return 1
    elif 0.257 < FCFTB <= 0.355:
        return 2
    elif 0.355 < FCFTB <= 0.545:
        return 3
    elif 0.545 < FCFTB <= 0.792:
        return 4
    elif 0.792 < FCFTB <= 1.555:
        return 5
    elif 1.555 < FCFTB :
        return 6
print("Grade of FCFTB: ",FCFTB_Grading(FCFTB))

#DEBT to EBITDA Ratio
print("\n***Debt to EBITDA***\nTotal Debt: %s\nEbitda: %s" %(debt,ebitda))
DTE = debt/ebitda
print("Debt to EBITDA",DTE)
#5.5 - 1，3.1 - 2，2.2 - 3，1.5 - 4，0.9 - 5，0.4 - 6
def DTE_Grading(DTE):
    if DTE >= 5.5:
        return 0
    elif 5.5 > DTE >= 3.1:
        return 1
    elif 3.1 > DTE >= 2.2:
        return 2
    elif 2.2 > DTE >= 1.5:
        return 3
    elif 1.5 > DTE >= 0.9:
        return 4
    elif 0.9 > DTE >= 0.4:
        return 5
    elif 0.4 > DTE :
        return 6
print("Grade of DTE: ",DTE_Grading(DTE))

#DEBT to Debt Equity Ratio
print("\n***Debt to (Debt + Equity)***\nTotal Debt: %s\nTotal Stockholder Equity: %s" %(debt,equity))
DTDE=(debt)/(debt+equity)
print ("Debt to (Debt + Equity)",DTDE)
#73.2% - 1，52.5% - 2，44.5% - 3，36.8% - 4，35.2% - 5，12.3% - 6
def DTDE_Grading(DTDE):
    if DTDE >= 0.732:
        return 0
    elif 0.732 > DTDE >= 0.525:
        return 1
    elif 0.525 > DTDE >= 0.445:
        return 2
    elif 0.445 > DTDE >= 0.368:
        return 3
    elif 0.368 > DTDE >= 0.352:
        return 4
    elif 0.352 > DTDE >= 0.123:
        return 5
    elif 0.123 > DTDE :
        return 6
print ("Grade of DTDE: ",DTDE_Grading(DTDE))