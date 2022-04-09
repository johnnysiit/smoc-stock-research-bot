import dictionary_making as dm
import pandas as pd
import openpyxl
import datetime

def dict_get(ticker):
    year0_dict = dm.data_dictionary(0,ticker)
    year1_dict = dm.data_dictionary(1,ticker)
    year2_dict = dm.data_dictionary(2,ticker)
    return [year0_dict,year1_dict,year2_dict]

def table_generate(dict_select,ticker,output_mode):
    
    data_list = (dict_get(ticker))
    print("\nData Generating... Please wait...\n 数据生成中，请稍等...\n")
    def data_select(yearindex):
        data = []
        for j in dict_select:
            data.append(data_list[yearindex][j])
        return data
    try: 
        df = pd.DataFrame(
            {
                data_list[0]["Date"]:data_select(0),
                data_list[1]["Date"]:data_select(1),
                data_list[2]["Date"]:data_select(2)
            }
        )
        df.index = dict_select
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

def main(ticker,output_mode):
    OMBDA = ["Operating Income","Reconciled Depreciation","Tax Provision","Net Interest Income","Total Revenue","OMBDA","OMBDA_Grading"," "]
    ROE = ["Net Income Common Stockholders","Preferred Stock Dividends","Avg Stock Equity","ROE","ROE_Grading"," "]
    EI = ["EBIT","Interest Expense","EI","EI_Grading"," "]
    EIC = ["EBITA","Interest Expense","EIC","EIC_Grading"," "]
    FCFTD = ["Free Cashflow","Total Debt","FCFTD","FCFTD_Grading"," "]
    DTE = ["Total Debt","EBITA","DTE","DTE_Grading"," "]
    DTDE = ["Total Debt","Equity","DTDE","DTDE_Grading"," "]
    TOTAL = ["Total_Avg_Grading"]
    dict_select = OMBDA+ROE+EI+EIC+FCFTD+DTE+DTDE+TOTAL
    table_generate(dict_select,ticker,output_mode)