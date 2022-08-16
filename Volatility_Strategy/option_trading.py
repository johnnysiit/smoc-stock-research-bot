from finvizfinance.quote import finvizfinance
import pandas as pd
import datetime
import os
import time
import option_price as op

def get_finviz_data(ticker):
    stock = finvizfinance(ticker)
    stock_fundament = stock.ticker_fundament()
    return stock_fundament

def percentage_process(number):
    number = number.replace("%", "")
    number = float(number)
    number = abs(number)
    return number/100

def main():
    ticker_list = ["LOW","ADI","TJX","TGT","SNPS","NIO","KEYS","ZTO","EC","AMCR","EBR","ELP","WOLF","PFGC","BBWI","ZIM","BAK","WB","EVO","CIG","SID","SRAD","DNUT","YY","CINT","SFL","MCG","EXAI","TUYA","MAG","HYZN","NNDM","JBSS","TGS","CRMT","NESR","PLCE","TUFN","RADA","AURC","ORMP","GRIN","ZOM","KMDA","IREN","RAAS","SMED","MDXH","LUCD","BEST","OTMO","AIH","CRWS","CIH","VTVT","BDL","TPHS","DGLY","MXC","DGHI","AIKI","BSGM","NAVB","ALRN","ELTK","BTBD","HOTH","MOBQ","NEPT","RMED"]
    # ticker_list = ["LOW"]
    final_data = dict()
    count = 0
    for i in ticker_list:
        count += 1
        if count%20 == 0:
            print ("8 secs cooldown")
            time.sleep(8)
        try:
            stock_data = get_finviz_data(i)
            filter_data = dict()
            if stock_data["Optionable"] == "Yes":
                for j in stock_data:
                    if j == "Price":
                        filter_data["Price"] = float(stock_data[j])
                    elif j == "Perf Week":
                        filter_data["Perf Week"] = percentage_process(stock_data[j])
                    elif j == "Perf Quarter":
                        filter_data["Perf Quarter"] = percentage_process(stock_data[j])
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
                filter_data["Total Volatility"] = (filter_data["Perf Week"]*5 + filter_data["Perf Quarter"] + filter_data["52W Low"] + filter_data["52W High"] + filter_data["Volatility W"]*5 + filter_data["Volatility M"]*2 + filter_data["Change"]*10)/5
                option = op.OptionPrice(i,filter_data["Price"])
                opc = option.get_call()
                opp = option.get_put()
                filter_data["Call"] = opc
                filter_data["Put"] = opp
                total = opc + opp
                filter_data["Option Total"] = total
                final_data[i] = filter_data
                print (i,"...Fetched Successfully")
        except:
            print (i,"...Failed")
            continue

    df = pd.DataFrame(final_data)
    current_time = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        df.to_excel("./Output/Volatility_Strategy"+current_time+".xlsx")
        print ("\n数据输出成功于Output文件夹\nData output successfully in Output folder\n")
    except:
        print ("\n数据输出失败 请检查输出权限\nFailed to output data, please check output permission")

main()