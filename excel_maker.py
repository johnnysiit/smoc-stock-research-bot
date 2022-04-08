import dictionary_making as dm
import pandas as pd

def dict_get(ticker):
    year0_dict = dm.data_dictionary(0,ticker)
    year1_dict = dm.data_dictionary(1,ticker)
    year2_dict = dm.data_dictionary(2,ticker)
    return [year0_dict,year1_dict,year2_dict]

def table_generate(dict_select,ticker):
    
    data_list = (dict_get(ticker))

    def data_select(yearindex):
        data = []
        for j in dict_select:
            data.append(data_list[yearindex][j])
        return data

    df = pd.DataFrame(
        {
            data_list[0]["Date"]:data_select(0),
            data_list[1]["Date"]:data_select(1),
            data_list[2]["Date"]:data_select(2)
        }
    )
    df.index = dict_select
    print(df)

def main():
    OMBDA = ["Operating Income","Reconciled Depreciation","Tax Provision","Net Interest Income","Total Revenue","OMBDA","OMBDA_Grading"," "]
    ROE = ["Net Income Common Stockholders","Preferred Stock Dividends Paid","Avg Stock Equity","ROE","ROE_Grading"," "]
    EI = ["EBIT","Interest Expense","EI","EI_Grading"," "]
    EIC = ["EBITA","Interest Expense","EIC","EIC_Grading"," "]
    FCFTD = ["Free Cashflow","Total Debt","FCFTD","FCFTD_Grading"," "]
    DTE = ["Total Debt","EBITA","DTE","DTE_Grading"," "]
    DTDE = ["Total Debt","Equity","DTDE","DTDE_Grading"," "]
    TOTAL = ["Total_Avg_Grading"]
    dict_select = OMBDA+ROE+EI+EIC+FCFTD+DTE+DTDE+TOTAL
    table_generate(dict_select,"AAPL")

main()