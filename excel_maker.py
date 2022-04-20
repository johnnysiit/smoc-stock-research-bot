import dictionary_making as dm
import pandas as pd
import datetime
import data_scraping as ds
import os
def dict_get(ticker,dict_select,runmode):
    yearindex = ds.total_years(ticker)
    all_data_dict = dict()
    #获取所有年所需数据
    for i in range(yearindex):
        single_year_data = dm.data_dictionary(i,ticker,runmode)
        date_in_dict = single_year_data["Date"]
        temp_data = dict()
        for outterlist in dict_select:
            temp_data[outterlist] = ""
            for innerlist in dict_select[outterlist]:
                temp_data[innerlist] = single_year_data[innerlist]
        all_data_dict[date_in_dict] = temp_data
    note = dict()
    note["OMBDA_"]="ROE in the earliest year is not accurate \nROE在最早年份不准确 \nIf Interest Expense is 1, then EI and EIC could not be apply \n如果Interest Expense为1，则EI和EIC不能使用 \n"
    all_data_dict["Note"]=note
        #获取该年所需数据
    return all_data_dict

def table_generate(dict_select,ticker,output_mode,runmode):
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_list = (dict_get(ticker,dict_select,runmode))
    print("\nData Generating... Please wait...\n 数据生成中，请稍等...\n")

    try: 
        df = pd.DataFrame(data_list)
        print("\n%s Data Generated Successfully!\n %s数据生成成功！\n"%(ticker,ticker))
    except:
        print("\n%s Data Generated Failed!\n %s数据生成失败，请联系管理员\n"%(ticker,ticker))

    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')

    if output_mode == 1:
        try:
            df.to_excel(current_path+"/Output/%s_DataAnaly_%s.xlsx"%(ticker,current_time))
            print("\n%s Data Output Successfully! Please check Output folder\n %s数据输出成功,请检查Output文件夹\n"%(ticker,ticker))
        except:
            print("\n%s Data Output Failed! Please print in console\n %sExcel输出失败,请使用终端输出\n"%(ticker,ticker))
    elif output_mode == 2:
        print("%s Data Output %s数据:\n"%(ticker,ticker))
        print(df)

def main(ticker,output_mode,runmode):
    dict_select= dict()
    dict_select["OMBDA_"] = ["Operating Income","Reconciled Depreciation","Tax Provision","Net Interest Income","Total Revenue","OMBDA","OMBDA_Grading"]
    dict_select["ROE_"] = ["Net Income Common Stockholders","Preferred Stock Dividends","Avg Stock Equity","ROE","ROE_Grading"]
    dict_select["EI_"] = ["EBIT","Interest Expense","EI","EI_Grading"]
    dict_select["EIC_"] = ["EBITA","Interest Expense","EIC","EIC_Grading"]
    dict_select["FCFTD_"] = ["Free Cashflow","Total Debt","FCFTD","FCFTD_Grading"]
    dict_select["DTE_"] = ["Total Debt","EBITA","DTE","DTE_Grading"]
    dict_select["DTDE_"] = ["Total Debt","Equity","DTDE","DTDE_Grading"]
    dict_select["TOTAL_"] = ["Total_Avg_Grading"]
    table_generate(dict_select,ticker,output_mode,runmode)

