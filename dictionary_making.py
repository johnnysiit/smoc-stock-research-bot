from select import select
import pandas as pandas
import data_scraping as ds
import algri_config as ac

def data_selecting(sheet,content,yearindex):
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


def data_dictionary(year,ticker):
    #Creating Tables
    yf_cashflow = ds.cash_flow(ticker)
    yf_balance = ds.balance_sheet(ticker)
    yf_income_statement = ds.income_statement(ticker)
    financial_data = dict()

    #Cash flow
    cashflow_list = ["Operating Cash Flow","Capital Expenditure","Preferred Stock Dividends Paid"]
    for i in cashflow_list:
        financial_data[i] = data_selecting(yf_cashflow,i,year)

    #Income Statement
    income_statement_list = ["Reconciled Depreciation","Net Income Common Stockholders","Operating Income","Interest Expense","Tax Provision","Total Revenue","EBIT","Net Interest Income"]
    for i in income_statement_list:
        financial_data[i] = data_selecting(yf_income_statement,i,year)
    print (yf_income_statement)

    #Balance Sheet
    balance_sheet_list = ["Total Debt","Total Equity Gross Minority Interest"]
    for i in balance_sheet_list:
        financial_data[i] = data_selecting(yf_balance,i,year)
    financial_data["Previous Year Stockholders Equity Balance"] = data_selecting(yf_balance,"Total Equity Gross Minority Interest",(year+1))

    #final variables
    financial_data["EBITA"] = financial_data["EBIT"] + financial_data["Reconciled Depreciation"]
    financial_data["Avg Stock Equity"] = (financial_data["Total Equity Gross Minority Interest"] + financial_data["Previous Year Stockholders Equity Balance"])/2
    financial_data["Equity"] = financial_data["Total Equity Gross Minority Interest"]
    financial_data["Free Cashflow"] = financial_data["Operating Cash Flow"] + financial_data["Capital Expenditure"]
    return financial_data

#======================Calculating Part=======================#


#Operating Margin before D&A
# print("\n***Operating Margin before D&A***\nOperating Income: %s\nDepreciation: %s\nTax: %s\nInterest Income: %s\nSales: %s"%(operating_income,depreciation,tax,interest_income,sales))
# OMBDA = (operating_income+depreciation+tax+interest_income)/sales
# print("Operating Margin before D&A (in%): ",OMBDA)
# print("Grade of ROE: ",ac.OMBDA_Grading(OMBDA))

# #Return on Equity
# print("\n***Return on Equity***\nNet Income: %s\nPrefer Stock Dividend: %s\nAverage Common Stockholder's Equity: %s"%(net_income,preferStockDividend,avg_stock_equity))
# ROE = (net_income-preferStockDividend)/avg_stock_equity
# print("Return on Equity: ",ROE)
# print("Grade of ROE: ",ac.ROE_Grading(ROE))

# #EBIT Interest Coverage
# print("\n***EBIT Interest Coverage***\nEbit: %s\nInterest: %s" %(ebit,interest_expense))
# EI = ebit/(interest_expense)
# print("EBIT Interest Coverage:",EI)
# print("Grade of EI: ",ac.EI_Grading(EI))

# #EBITDA Interest Coverage
# print("\n***EBITDA Interest Coverage***\nEbitda: %s\nInterest: %s" %(ebitda,interest_expense))
# EIC = ebitda/(interest_expense)
# print("EBITDA Interest Coverage:",EIC)
# print("Grade of EIC: ",ac.EIC_Grading(EIC))

# #Free Cash Flow to Debt Ratio
# print("\n***Free Cash Flow to Debt***\nFree Cash Flow: %s\nTotal Debt: %s" %(freecashflow,debt))
# FCFTD = freecashflow/debt
# print("Free Cash Flow to Debt:",FCFTD)
# print("Grade of FCFTD: ",ac.FCFTD_Grading(FCFTD))

# #DEBT to EBITDA Ratio
# print("\n***Debt to EBITDA***\nTotal Debt: %s\nEbitda: %s" %(debt,ebitda))
# DTE = debt/ebitda
# print("Debt to EBITDA:",DTE)
# print("Grade of DTE:",ac.DTE_Grading(DTE))

# #DEBT to Debt Equity Ratio
# print("\n***Debt to (Debt + Equity)***\nTotal Debt: %s\nTotal Stockholder Equity: %s" %(debt,equity))
# DTDE=(debt)/(debt+equity)
# print ("Debt to (Debt + Equity):",DTDE)
# print ("Grade of DTDE: ",ac.DTDE_Grading(DTDE))
# print ("\nTotal Average Grade:%1.2f"%(float(ac.OMBDA_Grading(OMBDA)+ac.ROE_Grading(ROE)+ ac.EI_Grading(EI) + ac.EIC_Grading(EIC) + ac.FCFTD_Grading(FCFTD) + ac.DTE_Grading(DTE) + ac.DTDE_Grading(DTDE))/7))