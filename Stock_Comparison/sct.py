#Author: Juanxi Xue
from finvizfinance.quote import finvizfinance
import pandas as pd
import datetime
import os

def get_data(ticker):
    stock = finvizfinance(ticker)
    stock_fundament = stock.ticker_fundament()
    return stock_fundament

def main():
    print ("\n请在每行输入一个股票代码，并留空回车以完成键入")
    print ("Please enter one ticker per line, and press enter to finish\n")
    ticker_list = []
    count = 0
    while True:
        count += 1
        tickers = input("Enter stock ticker %s: "%count)
        if tickers == '':
            break
        else:
            ticker_list.append(tickers)

    final_data = dict()

    for i in ticker_list:
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

    df = pd.DataFrame(final_data)
    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    #make excel
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_name = current_path+"/Output/%s_SCT_%s.xlsx"%(ticker_list[0],current_time)
        df.to_excel(file_name)
        print ("\n数据输出成功于Output文件夹\nData output successfully in Output folder\n")
    except:
        print ("\n数据输出失败 请检查输出权限\nFailed to output data, please check output permission")
