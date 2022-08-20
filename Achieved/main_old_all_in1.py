from select import select
# import yfinance as yf
import pandas as pandas
import Statement_Grading.data_scraping as ds
import Statement_Grading.algri_config as ac

#Introduction
print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
print("\nAttention: This system cannot apply on the data of financial industry.\n请注意：该系统不适用于金融行业的财报数据\n")
stock_ticker = str(input("请输入股票代码 Please type in the symbol of the stock: "))
yearindex = int(input("\n请输入年份 Please type in the year index you want to get \n0: Most recent year\n1: Last Year \n1: Two years ago\n2: Three years ago\nPlease type in a number: "))
print("\n请稍等，总时长可能会超过2分钟 Please wait... The whole process might take over 2 minutes....\n")

def data_selecting(sheet,content):
    try:
        selector = sheet.loc[content]
        selector = selector.iat[yearindex]
        if selector == "Null" or selector == "NaN" or selector== "None" or selector == "null" or selector == "nan" or selector == "none":
            selector = 0
        selector = selector.replace(',','')
        selector = int(selector)*1000
        return selector
    except:
        print ("\n!!!WARNING请注意！！！")
        print ("We could not locate the data of '%s', please type in mannually\n我们无法找到 '%s',请手动补充" %(content,content))
        print ("!!!Please be advise that data unit in Yahoo Finance is in THOUSAND. \n!!!请注意，YahooFinance的数据单位是千 输入时请换算成一")
        selector = int(input(content+": "))
        return selector

#Cash flow
yf_cashflow = ds.cash_flow(stock_ticker)
operatingflow = data_selecting(yf_cashflow, "Operating Cash Flow")
capitalExpenditures = data_selecting(yf_cashflow, "Capital Expenditure")
depreciation = data_selecting(yf_cashflow, "Depreciation")
preferStockDividend = data_selecting(yf_cashflow, "Preferred Stock Dividends Paid")
print(yf_cashflow)

#Income Statement
yf_income_statement = ds.income_statement(stock_ticker)
operating_income = data_selecting(yf_income_statement, "Operating Income")
tax = data_selecting(yf_income_statement, "Tax Provision")
interest_expense = data_selecting(yf_income_statement, "Interest Expense")
net_income = data_selecting(yf_income_statement, "Net Income Common Stockholders")
sales = data_selecting(yf_income_statement, "Total Revenue")
interest_income = data_selecting(yf_income_statement, "Net Interest Income")
ebit = data_selecting(yf_income_statement, "EBIT")
print (yf_income_statement)

#Balance Sheet
yf_balance = ds.balance_sheet(stock_ticker)
print (yf_balance)
debt = data_selecting(yf_balance, "Total Debt")
starting_equity_balance = data_selecting(yf_balance, "Total Equity Gross Minority Interest")
yearindex +=1 
ending_equity_balance = data_selecting (yf_balance, "Total Equity Gross Minority Interest")
yearindex =1
avg_stock_equity = (starting_equity_balance + ending_equity_balance)/2

#final variables
ebitda = ebit + depreciation
equity = starting_equity_balance
freecashflow = operatingflow+capitalExpenditures

#======================Calculating Part=======================#


#Operating Margin before D&A
print("\n***Operating Margin before D&A***\nOperating Income: %s\nDepreciation: %s\nTax: %s\nInterest Income: %s\nSales: %s"%(operating_income,depreciation,tax,interest_income,sales))
OMBDA = (operating_income+depreciation+tax+interest_income)/sales
print("Operating Margin before D&A (in%): ",OMBDA)
print("Grade of ROE: ",ac.OMBDA_Grading(OMBDA))

#Return on Equity
print("\n***Return on Equity***\nNet Income: %s\nPrefer Stock Dividend: %s\nAverage Common Stockholder's Equity: %s"%(net_income,preferStockDividend,avg_stock_equity))
ROE = (net_income-preferStockDividend)/avg_stock_equity
print("Return on Equity: ",ROE)
print("Grade of ROE: ",ac.ROE_Grading(ROE))

#EBIT Interest Coverage
print("\n***EBIT Interest Coverage***\nEbit: %s\nInterest: %s" %(ebit,interest_expense))
EI = ebit/(interest_expense)
print("EBIT Interest Coverage:",EI)
print("Grade of EI: ",ac.EI_Grading(EI))

#EBITDA Interest Coverage
print("\n***EBITDA Interest Coverage***\nEbitda: %s\nInterest: %s" %(ebitda,interest_expense))
EIC = ebitda/(interest_expense)
print("EBITDA Interest Coverage:",EIC)
print("Grade of EIC: ",ac.EIC_Grading(EIC))

#Free Cash Flow to Debt Ratio
print("\n***Free Cash Flow to Debt***\nFree Cash Flow: %s\nTotal Debt: %s" %(freecashflow,debt))
FCFTD = freecashflow/debt
print("Free Cash Flow to Debt:",FCFTD)
print("Grade of FCFTD: ",ac.FCFTD_Grading(FCFTD))

#DEBT to EBITDA Ratio
print("\n***Debt to EBITDA***\nTotal Debt: %s\nEbitda: %s" %(debt,ebitda))
DTE = debt/ebitda
print("Debt to EBITDA:",DTE)
print("Grade of DTE:",ac.DTE_Grading(DTE))

#DEBT to Debt Equity Ratio
print("\n***Debt to (Debt + Equity)***\nTotal Debt: %s\nTotal Stockholder Equity: %s" %(debt,equity))
DTDE=(debt)/(debt+equity)
print ("Debt to (Debt + Equity):",DTDE)
print ("Grade of DTDE: ",ac.DTDE_Grading(DTDE))
print ("\nTotal Average Grade:%1.2f"%(float(ac.OMBDA_Grading(OMBDA)+ac.ROE_Grading(ROE)+ ac.EI_Grading(EI) + ac.EIC_Grading(EIC) + ac.FCFTD_Grading(FCFTD) + ac.DTE_Grading(DTE) + ac.DTDE_Grading(DTDE))/7))