from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

def data_scraping(ticker,sheet_name):
    url = ("https://finance.yahoo.com/quote/"+ticker+"/"+sheet_name+"?p="+ticker)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'DNT': '1', # Do Not Track Request Header 
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    assert len(table_rows) > 0
    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")
        none_count = 0
        
        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
                
            except ValueError:
                parsed_row.append("0")
                none_count += 1
        if (none_count < 4):
            parsed_rows.append(parsed_row)


    df = pd.DataFrame(parsed_rows)
    df = df.set_index(0)
    df.rename(index={df.index[0]: 'Date'}, inplace=True)
    return df

def income_statement(ticker):
    income_statement = data_scraping(ticker,"financials")
    income_statement = income_statement.iloc[:,1:]
    return income_statement

def balance_sheet(ticker):
    balance_sheet = data_scraping(ticker,"balance-sheet")
    return balance_sheet

def cash_flow(ticker):
    cash_flow = data_scraping(ticker,"cash-flow")
    cash_flow = cash_flow.iloc[:,1:]
    return cash_flow

def full_income_statement(ticker):
    income_statement = data_scraping(ticker,"financials")
    return income_statement
def full_cash_flow(ticker):
    cash_flow = data_scraping(ticker,"cash-flow")
    return cash_flow
def total_years(ticker):
    balance_sheet = data_scraping(ticker,"balance-sheet")
    return len(balance_sheet.columns)