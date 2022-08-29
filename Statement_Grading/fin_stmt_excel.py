#Author: Juanxi Xue
import pandas as pd
import Statement_Grading.data_scraping as ds
import datetime
import os
def date_function(sheet):
        date_list = []
        date = sheet.loc["Date"]
        for i in date:
            date_list.append(i)
        sheet.columns = date_list
        sheet.drop(["Date"],axis=0,inplace=True)
        return sheet

def main(ticker,output_mode):
    current_path = os.path.dirname(os.path.abspath(__file__))
    print("\nNow generating financial statement\n正在生成财务报表\n")
    income = ds.full_income_statement(ticker)
    income = date_function(income)
    balance = ds.balance_sheet(ticker)
    balance = date_function(balance)
    cashflow = ds.full_cash_flow(ticker)
    cashflow = date_function(cashflow)
    if output_mode == 1:
        try:
            current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
            writer = pd.ExcelWriter("./Output/%s_FinStatmt_%s.xlsx"%(ticker,current_time))
            income.to_excel(writer, sheet_name="IncomeStatement")
            cashflow.to_excel(writer, sheet_name="CashFlow")
            balance.to_excel(writer, sheet_name="BalanceSheet")
            writer.save()
            writer.close()
            print("\n%s Financial Statement Output Successfully! Please check Output folder\n %s财报输出成功,请检查Output文件夹\n"%(ticker,ticker))
        except:
            print("\n%s Excel Output Failed! Please print in console\n %s财报输出失败,请使用终端输出\n"%(ticker,ticker))
    elif output_mode == 2:
        print("%s Financial Statement 财报:\n"%(ticker))
        print ("Income Statement:\n",income)
        print ("Cash Flow:\n",cashflow)
        print ("Balance Sheet:\n",balance)
