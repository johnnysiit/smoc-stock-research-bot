#Author: Juanxi Xue
from finvizfinance.quote import finvizfinance
import pandas as pd
import datetime
import os
import time

def get_data(ticker):
    stock = finvizfinance(ticker)
    stock_fundament = stock.ticker_fundament()
    return stock_fundament

def main():
    input("Please enter the stock ticker in ticker,txt, press enter to continue: ")
    file = open("./Stock_Comparison/ticker.txt", "r")
    ticker = file.readlines()
    ticker_list = []
    for k in ticker:
        ticker_list.append(k.strip())

    final_data = dict()
    count = 0
    for i in ticker_list:
        if count%20 == 0:
            print("Cooling down...")
            time.sleep(7)
        try:
            count += 1
            stock_data = get_data(i)
            for j in stock_data:
                if stock_data[j].endswith ('B'):
                    stock_data[j] = stock_data[j].replace('B', '')
                    stock_data[j] = float(stock_data[j]) * 1000000000
                    stock_data[j] = int(stock_data[j])
                elif stock_data[j].endswith('M'):
                    stock_data[j] = stock_data[j].replace('M', '')
                    stock_data[j] = float(stock_data[j]) * 1000000
                    stock_data[j] = int(stock_data[j])
            final_data[i] = stock_data
            print (i, "fetching data successfully")
        except:
            print(i, "fetching data failed")
            continue
    df = pd.DataFrame(final_data)
    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    #make excel
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_name = "./Output/%s_SCT_%s.xlsx"%(ticker_list[0],current_time)
        df.to_excel(file_name)
        print ("\n数据输出成功于Output文件夹\nData output successfully in Output folder\n")
    except:
        print ("\n数据输出失败 请检查输出权限\nFailed to output data, please check output permission")
