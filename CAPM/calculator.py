#Author: Juanxi Xue
import price_scraping as ps

sp500 = ps.get_price("VOO")
stock = ps.get_price("WMT")

def variance(data):
    mean = sum(data)/len(data)
    variance = sum([(i-mean)**2 for i in data])/len(data)
    return variance

def covariance(data1, data2):
    mean1 = sum(data1)/len(data1)
    mean2 = sum(data2)/len(data2)
    covariance = sum([(data1[i]-mean1)*(data2[i]-mean2) for i in range(len(data1))])/len(data1)
    return covariance

sp500_variance = variance(sp500)
stock_variance = variance(stock)
sp500_stock_covariance = covariance(sp500, stock)

def beta(data1, data2):
    return covariance(data1, data2)/variance(data1)

b = beta(sp500, stock)
print (b)