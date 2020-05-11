import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

# api_key = 'H2AKUMZSFASPIHZH'
stock_symbol = 'MSFT'

def six_month_stockchart(stock_symbol, api_key = 'H2AKUMZSFASPIHZH'):
    # get all stock data
    ts = TimeSeries(key = api_key, output_format = 'pandas')
    data = ts.get_daily(symbol = stock_symbol, outputsize = 'full')[0]

    # get a all data from a given start date only
    start_date = datetime.datetime.today() + relativedelta(months = -6) 
    clean_data = data[start_date:]['4. close']

    # get x axis dates
    x_axis_labels = get_month_xticks(6)
    # configure graph
    clean_data.plot()
    plt.title(stock_symbol + ' 6 Month Stock chart')
    plt.xticks(x_axis_labels)
    plt.xlabel('Dates')
    plt.ylabel('Close Values')
    plt.savefig('6monthchart.png')
    plt.close()



def one_month_stockchart(stock_symbol, api_key = 'H2AKUMZSFASPIHZH'):
    # get all stock data
    ts = TimeSeries(key = api_key, output_format = 'pandas')
    data = ts.get_daily(symbol = stock_symbol, outputsize = 'full')[0]

    # get a all data from a given start date only
    start_date = datetime.datetime.today() + relativedelta(months = -1) 
    cleaned_data = data[start_date:]['4. close']

    # get x axis dates
    x_axis_labels = get_month_xticks(1)
    # configure graph
    cleaned_data.plot()
    plt.title(stock_symbol + ' 1 Month Stock chart')
    plt.xticks(x_axis_labels)
    plt.xlabel('Dates')
    plt.ylabel('Close Values')
    plt.savefig('1monthchart.png')
    plt.close()
    


def get_month_xticks(months):
    x_axis_labels = []
    for i in range(7):
        if(months == 1):
            if i == 5: break
            date = datetime.datetime.today() + relativedelta(weeks = -i)
            x_axis_labels.append(date.strftime('%Y-%m-%d'))
        if(months == 6):
            date = datetime.datetime.today() + relativedelta(months = -i)
            x_axis_labels.append(date.strftime('%Y-%m-%d'))
    return x_axis_labels


def get_year_xticks(years):
    x_axis_labels = []
    buffer = 1
    for i in range(6):
        if(years == 1):
            if i == 4: break
            date = datetime.datetime.today() + relativedelta(months = -i - buffer)
            x_axis_labels.append(date.strftime('%Y-%m-%d'))
            buffer += 2
        if(years == 5):
            date = datetime.datetime.today() + relativedelta(years = -i)
            x_axis_labels.append(date.strftime('%Y-%m-%d'))
    return x_axis_labels




def one_year_stockchart(stock_symbol, api_key = 'H2AKUMZSFASPIHZH'):
    # get all stock data
    ts = TimeSeries(key = api_key, output_format = 'pandas')
    data = ts.get_daily(symbol = stock_symbol, outputsize = 'full')[0]

    # get a all data from a given start date only
    start_date = datetime.datetime.today() + relativedelta(years = -1) 
    cleaned_data = data[start_date:]['4. close']

    # get x axis dates
    x_axis_labels = get_year_xticks(1)
    # configure graph
    cleaned_data.plot()
    plt.title(stock_symbol + ' 1 Year Stock chart')
    plt.xticks(x_axis_labels)
    plt.xlabel('Dates')
    plt.ylabel('Close Values')
    plt.savefig('1yearchart.png')
    plt.close()


def five_year_stockchart(stock_symbol, api_key = 'H2AKUMZSFASPIHZH'):
    # get all stock data
    ts = TimeSeries(key = api_key, output_format = 'pandas')
    data = ts.get_daily(symbol = stock_symbol, outputsize = 'full')[0]

    # get a all data from a given start date only
    start_date = datetime.datetime.today() + relativedelta(years = -5) 
    cleaned_data = data[start_date:]['4. close']

    # get x axis dates
    x_axis_labels = get_year_xticks(5)
    # configure graph
    cleaned_data.plot()
    plt.title(stock_symbol + ' 5 Year Stock chart')
    plt.xticks(x_axis_labels)
    plt.xlabel('Dates')
    plt.ylabel('Close Values')
    plt.savefig('5yearchart.png')
    plt.close()
            

six_month_stockchart(stock_symbol)
one_month_stockchart(stock_symbol)
one_year_stockchart(stock_symbol)
five_year_stockchart(stock_symbol)