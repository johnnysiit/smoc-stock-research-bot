#Author: Juanxi Xue
import CAPM.price_scraping as ps

def variance(data):
    mean = sum(data)/len(data)
    variance = sum([(i-mean)**2 for i in data])/len(data)
    return variance

def covariance(data1, data2):
    mean1 = sum(data1)/len(data1)
    mean2 = sum(data2)/len(data2)
    covariance = sum([(data1[i]-mean1)*(data2[i]-mean2) for i in range(len(data1))])/len(data1)
    return covariance

def beta(data1, data2):
    return covariance(data1, data2)/variance(data1)

def capm(b):
    r_free = 3.12
    sp500_return = 12.4
    capm = r_free + b*(sp500_return-r_free)
    return capm

def main(stock):
    sp500 = ps.get_price("VOO")
    stock = ps.get_price(stock)
    b = beta(stock, sp500)
    capm_stock = capm(b)
    print ("Beta: ", b)
    print ("CAPM: ", capm_stock)