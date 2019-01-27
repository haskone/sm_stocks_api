from datetime import datetime
from iexfinance.stocks import (
    get_historical_data,
    Stock,
)
from iexfinance import get_available_symbols
from db import save

FIRST_N_STOCKS = 150
START = datetime(2018, 11, 1)
END = datetime(2019, 1, 1)

def get_company(stock_symbol):
    stock = Stock(stock_symbol)
    last_price = stock.get_price()
    company_data = stock.get_company()
    company_data.pop('symbol')
    company_data['last_price'] = last_price
    return company_data

def get_historical(stock_symbol, start, end):
    return get_historical_data(stock_symbol, start, end)


if __name__ == "__main__":
    for stock in get_available_symbols(output_format='pandas')[:FIRST_N_STOCKS]:
        symbol = stock['symbol']
        company = get_company(symbol)
        data = get_historical(symbol, START, END)
        obj = {
            'symbol': symbol,
            'company': company,
            'history': data,
        }
        save(obj)
        print(f'{symbol} saved...')
