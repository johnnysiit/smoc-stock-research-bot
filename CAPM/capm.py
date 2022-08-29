#Author: Juanxi Xue
import calculator as calc

r_free = float(input("Enter the risk-free rate: "))
sp500_return = float(input("Enter the S&P 500 expect return: "))

capm_stock = r_free + calc.b*(sp500_return-r_free)
print (capm_stock)