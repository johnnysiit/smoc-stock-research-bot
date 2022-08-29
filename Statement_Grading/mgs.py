#Author: Juanxi Xue
import pandas as pd
import Statement_Grading.data_scraping as ds
import Statement_Grading.algri_config as ac
import datetime
import os

def data_selecting(sheet,content,yearindex,runmode):
    try:
        selector = sheet.loc[content]
        selector = selector.iat[yearindex]
        if selector == "Null" or selector == "-" or selector == "NaN" or selector== "None" or selector == "null" or selector == "nan" or selector == "none":
            selector = 0
        selector = selector.replace(',','')
        selector = float(selector)
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
            selector = float(input(content+": "))
        return selector


def data_dictionary(ticker,runmode):
    #Creating Tables
    try:
        yf_cashflow = ds.cash_flow(ticker)
        yf_balance = ds.balance_sheet(ticker)
        yf_income_statement = ds.income_statement(ticker)
    except:
        print("\nData Scraping Failed!\n数据抓取失败,请检查股票代码%s是否正确\n"%ticker)
        exit()
    
    #Getting Date
    yearindex = ds.total_years(ticker)
    all_data_dict = dict()
    dict_select = select_dict()
    for year in range(yearindex):
        single_year_data = dict()
        date = yf_balance.loc["Date"]
        single_year_data["Date"] = date.iat[year]

        #Cash flow
        cashflow_list = ["Operating Cash Flow","Capital Expenditure"]
        for i in cashflow_list:
            single_year_data[i] = data_selecting(yf_cashflow,i,year,runmode)

        #Income Statement
        if runmode == 1:
            income_statement_list = ["Preferred Stock Dividends","Reconciled Depreciation","Net Income Common Stockholders","Operating Income","Interest Expense","Tax Provision","Total Revenue","EBIT","Net Interest Income"]
        else:
            single_year_data["Preferred Stock Dividends"] = 0
            income_statement_list = ["Reconciled Depreciation","Net Income Common Stockholders","Operating Income","Interest Expense","Tax Provision","Total Revenue","EBIT","Net Interest Income"]
        for i in income_statement_list:
            single_year_data[i] = data_selecting(yf_income_statement,i,year,runmode)
        

        #Balance Sheet
        balance_sheet_list = ["Total Debt","Total Equity Gross Minority Interest"]
        for i in balance_sheet_list:
            single_year_data[i] = data_selecting(yf_balance,i,year,runmode)
        try:
            single_year_data["Previous Year Stockholders Equity Balance"] = data_selecting(yf_balance,"Total Equity Gross Minority Interest",(year+1),runmode)
        except:
            single_year_data["Previous Year Stockholders Equity Balance"] = data_selecting(yf_balance,"Total Equity Gross Minority Interest",(year),runmode)
            if runmode == 1:
                print("\nCannot locate the Stockholders Equity of previous year, please ignore ROE result\n无法找到上一年的股东权益,ROE将不具备参考价值")

        #final variables
        single_year_data["EBITA"] = single_year_data["EBIT"] + single_year_data["Reconciled Depreciation"]
        single_year_data["Avg Stock Equity"] = (single_year_data["Total Equity Gross Minority Interest"] + single_year_data["Previous Year Stockholders Equity Balance"])/2
        single_year_data["Equity"] = single_year_data["Total Equity Gross Minority Interest"]
        single_year_data["Free Cashflow"] = single_year_data["Operating Cash Flow"] + single_year_data["Capital Expenditure"]

        # OMBDA = (operating_income+depreciation+tax+interest_income)/sales
        single_year_data["OMBDA"] = (single_year_data["Operating Income"] + single_year_data["Reconciled Depreciation"] + single_year_data["Tax Provision"] + single_year_data["Net Interest Income"])/single_year_data["Total Revenue"]
        single_year_data["OMBDA Grading"] = ac.OMBDA_Grading(single_year_data["OMBDA"])
        #ROE = (net_income-preferStockDividend)/avg_stock_equity
        single_year_data["ROE"] = (single_year_data["Net Income Common Stockholders"] - single_year_data["Preferred Stock Dividends"])/single_year_data["Avg Stock Equity"]
        single_year_data["ROE Grading"] = ac.ROE_Grading(single_year_data["ROE"])
        # EI = ebit/(interest_expense)
        if single_year_data["Interest Expense"] == 0:
            single_year_data["Interest Expense"] = 0.0001
            if runmode == 1:
                print("Warning: Net Interest Expense is 0, please ignore EI datas\n警告:净利息支出为0,请忽略EI数据\n")
        single_year_data["EI"] = single_year_data["EBIT"]/single_year_data["Interest Expense"]
        single_year_data["EI Grading"] = ac.EI_Grading(single_year_data["EI"])
        # EIC = ebitda/(interest_expense)
        single_year_data["EIC"] = single_year_data["EBITA"]/single_year_data["Interest Expense"]
        single_year_data["EIC Grading"] = ac.EIC_Grading(single_year_data["EIC"])
        # FCFTD = freecashflow/debt
        if single_year_data["Total Debt"] == 0:
            single_year_data["Total Debt"] = 0.0001
        single_year_data["FCFTD"] = single_year_data["Free Cashflow"]/single_year_data["Total Debt"]
        single_year_data["FCFTD Grading"] = ac.FCFTD_Grading(single_year_data["FCFTD"])
        # DTE = debt/ebitda
        single_year_data["DTE"] = single_year_data["Total Debt"]/single_year_data["EBITA"]
        single_year_data["DTE Grading"] = ac.DTE_Grading(single_year_data["DTE"])
        # DTDE=(debt)/(debt+equity)
        single_year_data["DTDE"] = single_year_data["Total Debt"]/(single_year_data["Total Debt"]+single_year_data["Total Equity Gross Minority Interest"])
        single_year_data["DTDE Grading"] = ac.DTDE_Grading(single_year_data["DTDE"])

        single_year_data["Total Avg Grading"] = ((single_year_data["OMBDA Grading"]+single_year_data["ROE Grading"]+single_year_data["EI Grading"]+single_year_data["EIC Grading"]+single_year_data["FCFTD Grading"]+single_year_data["DTE Grading"]+single_year_data["DTDE Grading"])/7)
        
        date_in_dict = single_year_data["Date"]
        temp_data = dict()
        for outterlist in dict_select:
            temp_data[outterlist] = ""
            for innerlist in dict_select[outterlist]:
                temp_data[innerlist] = single_year_data[innerlist]
        all_data_dict[date_in_dict] = temp_data
    return all_data_dict

def select_dict():
    dict_select= dict()
    dict_select["OMBDA List"] = ["Operating Income","Reconciled Depreciation","Tax Provision","Net Interest Income","Total Revenue","OMBDA","OMBDA Grading"]
    dict_select["ROE List"] = ["Net Income Common Stockholders","Preferred Stock Dividends","Avg Stock Equity","ROE","ROE Grading"]
    dict_select["EI List"] = ["EBIT","Interest Expense","EI","EI Grading"]
    dict_select["EIC List"] = ["EBITA","Interest Expense","EIC","EIC Grading"]
    dict_select["FCFTD List"] = ["Free Cashflow","Total Debt","FCFTD","FCFTD Grading"]
    dict_select["DTE List"] = ["Total Debt","EBITA","DTE","DTE Grading"]
    dict_select["DTDE List"] = ["Total Debt","Equity","DTDE","DTDE Grading"]
    dict_select["TOTAL List"] = ["Total Avg Grading"]
    return dict_select

def main(ticker,output_mode,runmode):
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_list = data_dictionary(ticker,runmode)
    print("\nData Generating... Please wait...\n 数据生成中，请稍等...\n")

    try: 
        df = pd.DataFrame(data_list)
        print("\n%s Data Generated Successfully!\n %s数据生成成功！\n"%(ticker,ticker))
    except:
        print("\n%s Data Generated Failed!\n %s数据生成失败，请联系管理员\n"%(ticker,ticker))

    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')

    if output_mode == 1:
        try:
            df.to_excel("./Output/%s_DataAnaly_%s.xlsx"%(ticker,current_time))
            print("\n%s Data Output Successfully! Please check Output folder\n %s数据输出成功,请检查Output文件夹\n"%(ticker,ticker))
        except:
            print("\n%s Data Output Failed! Please print in console\n %sExcel输出失败,请使用终端输出\n"%(ticker,ticker))
    elif output_mode == 2:
        print("%s Data Output %s数据:\n"%(ticker,ticker))
        print(df)