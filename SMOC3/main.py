##年线:=EMA(C,96);
# 多头:EMA(C,2),COLORRED;
# 空头:年线-(多头-年线),COLORGREEN;
# 压力:=MA(LLV(C,12)*1.126,8);
# 支撑:=MA(HHV(C,26)*0.866,6);
# 多空线:=(压力+支撑)/2;
# 多空分界线: (压力+支撑)/2,COLORWHITE;
# 买:=CROSS(多头,多空线);
# 卖:=CROSS(多空线,多头);
# DRAWICON(买,L*0.99,1),COLORRED;
# DRAWICON(卖,H*1.01,2),COLORGREEN;
# M1:=CROSS(多头,空头);
# M2:=CROSS(空头,多头);
# DRAWTEXT(M1,L*0.99,'牛'),COLORRED;
# DRAWTEXT(M2,H*1.01,'熊'),COLORGREEN;
from tkinter.filedialog import Open
import yfinance as yf

def get_price(ticker):
    yfinance = yf.Ticker(ticker)
    hist = yfinance.history(period="6mo")
    hist["Price"] = (hist["Open"] + hist["Close"] + hist["High"] + hist["Low"]) / 4
    hist = hist.drop(columns=['Volume', 'Dividends', 'Stock Splits', 'Open', 'Close', 'High', 'Low'])
    print (hist)
get_price("AAPL")