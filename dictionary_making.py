from select import select
import pandas as pandas
import data_scraping as ds
import algri_config as ac

def data_selecting(sheet,content,yearindex,runmode):
    try:
        selector = sheet.loc[content]
        selector = selector.iat[yearindex]
        if selector == "Null" or selector == "-" or selector == "NaN" or selector== "None" or selector == "null" or selector == "nan" or selector == "none":
            selector = 0
        selector = selector.replace(',','')
        selector = int(selector)
        return selector
    except:
        #Getting Date
        if runmode == 2:
            selector = 0
        elif runmode == 1:
            date = sheet.loc["Date"]
            date = date.iat[yearindex]
            print ("\n!!!WARNING请注意!!!")
            print ("We could not locate the data of '%s' for the date of %s, please type in mannually\n我们无法找到%s的 '%s',请手动补充" %(content,date,date,content))
            print ("!!!Unit is in THOUSAND DOLLARS\n!!!单位是1000美元\n")
            selector = int(input(content+": "))
        return selector


def data_dictionary(year,ticker,runmode):
    #Creating Tables
    financial_data = dict()
    try:
        yf_cashflow = ds.cash_flow(ticker)
        yf_balance = ds.balance_sheet(ticker)
        yf_income_statement = ds.income_statement(ticker)
    except:
        print("\nData Scraping Failed!\n数据抓取失败,请检查股票代码%s是否正确\n"%ticker)
        exit()
    
    #Getting Date
    date = yf_balance.loc["Date"]
    financial_data["Date"] = date.iat[year]

    #Cash flow
    cashflow_list = ["Operating Cash Flow","Capital Expenditure"]
    for i in cashflow_list:
        financial_data[i] = data_selecting(yf_cashflow,i,year,runmode)

    #Income Statement
    if runmode == 1:
        income_statement_list = ["Preferred Stock Dividends","Reconciled Depreciation","Net Income Common Stockholders","Operating Income","Interest Expense","Tax Provision","Total Revenue","EBIT","Net Interest Income"]
    else:
        financial_data["Preferred Stock Dividends"] = 0
        income_statement_list = ["Reconciled Depreciation","Net Income Common Stockholders","Operating Income","Interest Expense","Tax Provision","Total Revenue","EBIT","Net Interest Income"]
    for i in income_statement_list:
        financial_data[i] = data_selecting(yf_income_statement,i,year,runmode)
    

    #Balance Sheet
    balance_sheet_list = ["Total Debt","Total Equity Gross Minority Interest"]
    for i in balance_sheet_list:
        financial_data[i] = data_selecting(yf_balance,i,year,runmode)
    try:
        financial_data["Previous Year Stockholders Equity Balance"] = data_selecting(yf_balance,"Total Equity Gross Minority Interest",(year+1),runmode)
    except:
        financial_data["Previous Year Stockholders Equity Balance"] = data_selecting(yf_balance,"Total Equity Gross Minority Interest",(year),runmode)
        if runmode == 1:
            print("\nCannot locate the Stockholders Equity of previous year, please ignore ROE result\n无法找到上一年的股东权益,ROE将不具备参考价值")

    #final variables
    financial_data["EBITA"] = financial_data["EBIT"] + financial_data["Reconciled Depreciation"]
    financial_data["Avg Stock Equity"] = (financial_data["Total Equity Gross Minority Interest"] + financial_data["Previous Year Stockholders Equity Balance"])/2
    financial_data["Equity"] = financial_data["Total Equity Gross Minority Interest"]
    financial_data["Free Cashflow"] = financial_data["Operating Cash Flow"] + financial_data["Capital Expenditure"]

    # OMBDA = (operating_income+depreciation+tax+interest_income)/sales
    financial_data["OMBDA"] = (financial_data["Operating Income"] + financial_data["Reconciled Depreciation"] + financial_data["Tax Provision"] + financial_data["Net Interest Income"])/financial_data["Total Revenue"]
    financial_data["OMBDA_Grading"] = ac.OMBDA_Grading(financial_data["OMBDA"])
    #ROE = (net_income-preferStockDividend)/avg_stock_equity
    financial_data["ROE"] = (financial_data["Net Income Common Stockholders"] - financial_data["Preferred Stock Dividends"])/financial_data["Avg Stock Equity"]
    financial_data["ROE_Grading"] = ac.ROE_Grading(financial_data["ROE"])
    # EI = ebit/(interest_expense)
    if financial_data["Interest Expense"] == 0:
        financial_data["Interest Expense"] = 0.0001
        if runmode == 1:
            print("Warning: Net Interest Expense is 0, please ignore EI datas\n警告:净利息支出为0,请忽略EI数据\n")
    financial_data["EI"] = financial_data["EBIT"]/financial_data["Interest Expense"]
    financial_data["EI_Grading"] = ac.EI_Grading(financial_data["EI"])
    # EIC = ebitda/(interest_expense)
    financial_data["EIC"] = financial_data["EBITA"]/financial_data["Interest Expense"]
    financial_data["EIC_Grading"] = ac.EIC_Grading(financial_data["EIC"])
    # FCFTD = freecashflow/debt
    financial_data["FCFTD"] = financial_data["Free Cashflow"]/financial_data["Total Debt"]
    financial_data["FCFTD_Grading"] = ac.FCFTD_Grading(financial_data["FCFTD"])
    # DTE = debt/ebitda
    financial_data["DTE"] = financial_data["Total Debt"]/financial_data["EBITA"]
    financial_data["DTE_Grading"] = ac.DTE_Grading(financial_data["DTE"])
    # DTDE=(debt)/(debt+equity)
    financial_data["DTDE"] = financial_data["Total Debt"]/(financial_data["Total Debt"]+financial_data["Total Equity Gross Minority Interest"])
    financial_data["DTDE_Grading"] = ac.DTDE_Grading(financial_data["DTDE"])

    financial_data["Total_Avg_Grading"] = ((financial_data["OMBDA_Grading"]+financial_data["ROE_Grading"]+financial_data["EI_Grading"]+financial_data["EIC_Grading"]+financial_data["FCFTD_Grading"]+financial_data["DTE_Grading"]+financial_data["DTDE_Grading"])/7)
    return financial_data

