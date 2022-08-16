from finvizfinance.quote import finvizfinance
import pandas as pd
import datetime
import os
import time
import Volatility_Strategy.option_price as op

def get_finviz_data(ticker):
    stock = finvizfinance(ticker)
    stock_fundament = stock.ticker_fundament()
    return stock_fundament

def percentage_process(number):
    number = number.replace("%", "")
    number = float(number)
    number = abs(number)
    return number/100

def clean_sheet(dic):
    new_dict = dict()
    new_dict["Price"] = dic["Price"]
    new_dict["Earnings"] = dic["Earnings"]
    new_dict["Total Volatility"] = str((dic["Total Volatility"]*100))+"%"
    new_dict["Option Total"] = dic["Option Total"]
    new_dict["Option to Price"] = str((dic["Option to Price"]*100))+"%"
    new_dict["JVOI"] = dic["JVOI"] = str((dic["JVOI"]*100))+"%"
    return new_dict

def main():
    file = open("./Volatility_Strategy/ticker.txt", "r")
    ticker = file.readlines()
    ticker_list = []
    for k in ticker:
        ticker_list.append(k.strip())
    final_data = dict()
    count = 0
    for i in ticker_list:
        count += 1
        if count%20 == 0:
            print ("8 secs cooldown")
            time.sleep(8)
        try:
            try:
                stock_data = get_finviz_data(i)
            except:
                print (i, "... Finviz Finance Fetching Failure")
            filter_data = dict()
            if stock_data["Optionable"] == "Yes":
                for j in stock_data:
                    if j == "Price":
                        filter_data["Price"] = float(stock_data[j])
                    elif j == "Earnings":
                        filter_data["Earnings"] = stock_data[j]
                    elif j == "Perf Week":
                        filter_data["Perf Week"] = percentage_process(stock_data[j])
                    elif j == "Perf Month":
                        filter_data["Perf Month"] = percentage_process(stock_data[j])
                    elif j == "52W Low":
                        filter_data["52W Low"] = percentage_process(stock_data[j])
                    elif j == "52W High":
                        filter_data["52W High"] = percentage_process(stock_data[j])
                    elif j == "Volatility W":
                        filter_data["Volatility W"] = percentage_process(stock_data[j])
                    elif j == "Volatility M":
                        filter_data["Volatility M"] = percentage_process(stock_data[j])
                    elif j == "Change":
                        filter_data["Change"] = percentage_process(stock_data[j])
                filter_data["Total Volatility"] = (filter_data["Perf Week"]*5*6 + filter_data["Perf Month"]*6 + filter_data["52W Low"] + filter_data["52W High"] + filter_data["Volatility W"]*5*6*2 + filter_data["Volatility M"]*6*2 + filter_data["Change"]*180)/(180*9)
                option = op.OptionPrice(i,filter_data["Price"])
                opc = option.get_call()
                opp = option.get_put()
                filter_data["Call"] = opc
                filter_data["Put"] = opp
                total = opc + opp
                filter_data["Option Total"] = total
                filter_data["Option to Price"] = total/filter_data["Price"]
                filter_data["JVOI"] = filter_data["Total Volatility"]/filter_data["Option to Price"]
                cleaner_sheet = clean_sheet(filter_data)
                final_data[i] = cleaner_sheet
                print (i,"... Fetched Successfully")
            else:
                print (i,"... Not Optionable")
        except:
            print (i,"... Yahoo Finance Fetching Failure")
            continue

    df = pd.DataFrame(final_data)
    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        df.to_excel("./Output/Volatility_Strategy"+current_time+".xlsx")
        print ("\n数据输出成功于Output文件夹\nData output successfully in Output folder\n")
    except:
        print ("\n数据输出失败 请检查输出权限\nFailed to output data, please check output permission")