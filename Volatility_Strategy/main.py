#Author: Juanxi Xue
from finvizfinance.quote import finvizfinance
import pandas as pd
import datetime
import os
import time
import Volatility_Strategy.option_price as op
import yfinance as yf

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
    new_dict["CV"] = str((dic["CV"]*100))+"%"
    new_dict["Option Total"] = dic["Option Total"]
    new_dict["Option to Price"] = str((dic["Option to Price"]*100))+"%"
    new_dict["JVOI"] = str((dic["JVOI"]*100))+"%"
    new_dict["JVOI2"] = str((dic["JVOI2"]*100))+"%"
    new_dict["JVOI3"] = str((dic["JVOI3"]*100))+"%"
    return new_dict

def get_cv(ticker):
    yfinance = yf.Ticker(ticker)
    hist = yfinance.history(period="6mo")
    price_list = []
    for t in hist["Open"]:
        price_list.append(float(t))
    for k in hist["Close"]:
        price_list.append(float(k))
    for j in hist["High"]:
        price_list.append(float(j))
    for l in hist["Low"]:
        price_list.append(float(l))
    #get mean on price list
    mean = sum(price_list)/len(price_list)
    # get standard deviation on price list
    std = sum([(i-mean)**2 for i in price_list])/len(price_list)
    std = std**0.5
    return std/mean

def main():
    file = open("./Volatility_Strategy/ticker.txt", "r")
    ticker = file.readlines()
    ticker_list = []
    for k in ticker:
        ticker_list.append(k.strip())
    ticker_list.append("VOO")
    ticker_list.append("TQQQ")
    ticker_list.append("SQQQ")
    ticker_list.append("UPRO")
    ticker_list.append("SDOW")
    ticker_list.append("UDOW")
    ticker_list.append("SPXL")
    ticker_list.append("SPXS")
    final_data = dict()
    count = 0
    for i in ticker_list:
        count += 1
        if count%20 == 0:
            print ("8 secs cooldown")
            time.sleep(8)
        #Get data from finviz
        try:
            stock_data = get_finviz_data(i)
        except:
            print (i, "... Finviz Finance Fetching Failure")
            continue
        #Data cleaning and processing start
        filter_data = dict()
        if stock_data["Optionable"] == "Yes":
            try: 
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
                    elif j == "SMA20":
                        filter_data["SMA20"] = percentage_process(stock_data[j])
                    elif j == "SMA50":
                        filter_data["SMA50"] = percentage_process(stock_data[j])
                    elif j == "SMA200":
                        filter_data["SMA200"] = percentage_process(stock_data[j])

                filter_data["Total Volatility"] = (filter_data["Perf Week"]*3*2 + filter_data["Perf Month"]*2 + filter_data["52W Low"] + filter_data["52W High"] + filter_data["Volatility W"]*3*2 + filter_data["Volatility M"]*2 + filter_data["Change"]*5*2 + filter_data["SMA20"]*2 + filter_data["SMA50"])/(15)
            except:
                print (i, "... Data Cleaning Failure")
                continue
            #=====Get Option Price Start=====
            try:
                option = op.OptionPrice(i,filter_data["Price"])
                opc = option.get_call()
                opp = option.get_put()
                filter_data["Call"] = opc
                filter_data["Put"] = opp
                total = opc + opp
                filter_data["Option Total"] = total

                filter_data["Option to Price"] = float(total/filter_data["Price"])
                filter_data["JVOI"] = filter_data["Total Volatility"]/filter_data["Option to Price"]
            except:
                print (i, "... Option Price Fetching Failure")
                continue
            #=====Get Option Price End=====
            try: 
                filter_data["CV"] = float(get_cv(i))
                filter_data["JVOI2"] = filter_data["CV"]/filter_data["Option to Price"]
                filter_data["JVOI3"] = (filter_data["JVOI"]+filter_data["JVOI2"])/2
                cleaner_sheet = clean_sheet(filter_data)
                final_data[i] = cleaner_sheet
            except:
                print (i, "... Historical Price Fetching Failure")
                continue
            print (i,"... Fetched Successfully")

        else:
            print (i,"... Not Optionable")
            continue

    df = pd.DataFrame(final_data)
    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        df.to_excel("./Output/Volatility_Strategy"+current_time+".xlsx")
        print ("\n数据输出成功于Output文件夹\nData output successfully in Output folder\n")
    except:
        print ("\n数据输出失败 请检查输出权限\nFailed to output data, please check output permission")