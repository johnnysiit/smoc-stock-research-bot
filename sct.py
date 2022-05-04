from finvizfinance.quote import finvizfinance
import pandas as pd

def get_data(ticker):
    stock = finvizfinance(ticker)
    stock_fundament = stock.ticker_fundament()
    return stock_fundament

def main():
    print ("请在每行输入一个股票代码，并留空回车以完成键入")
    print ("Please enter one ticker per line, and press enter to finish")
    ticker_list = []
    while True:
        tickers = input("Enter tickers: ")
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
    #make excel
    df.to_excel("./test.xlsx")
    print ("Done")
