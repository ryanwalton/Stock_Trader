# used for graphing
import plotly.graph_objects as go
from plotly.offline import plot
# used to get data and configure to usable format
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
# used for calculating dates
import datetime
from dateutil.relativedelta import relativedelta
# used to take graph and make it a div string for html
from flask import Markup

# def get_stocksyb():
#     return stock_symbol

def get_x_axis_dates(id, number):
    date_list = []
    i = 0
    if id == 'Day':
        end_date = datetime.datetime.today() + relativedelta(days = -number)
        date_index = datetime.datetime.today()
        date_list.append(date_index.strftime('%d:%I%p'))
        if number == 1:
            while date_index.strftime('%d:%I%p') != end_date.strftime('%d:%I%p'):
                i += 1
                date = datetime.datetime.today() + relativedelta(hours = -i)
                date_list.append(date.strftime('%d:%I%p'))
                date_index = date
        if number == 5:
            while date_index.strftime('%d:%I%p') != end_date.strftime('%d:%I%p'):
                i += 1
                date = datetime.datetime.today() + relativedelta(hours = -i)
                print(date)
                date_list.append(date.strftime('%d:%I%p'))
                date_index = date
        date_list.reverse()
        return date_list
    if id == 'Month':
        # get the end date to stop and return date_list
        end_date = datetime.datetime.today() + relativedelta(months = -number)
        # get starting date for indexing
        date_index = datetime.datetime.today()
        # append start date to date_list
        date_list.append(date_index.strftime('%Y-%m-%d'))
        if number == 1:
            # untill date_index get to end_date keep getting every day into date_list
            while date_index.strftime('%Y-%m-%d') != end_date.strftime('%Y-%m-%d'):
                i += 1
                date = datetime.datetime.today() + relativedelta(days = -i)
                date_list.append(date.strftime('%Y-%m-%d'))
                date_index = date
        if number == 6:
            while date_index.strftime('%Y-%m-%d') != end_date.strftime('%Y-%m-%d'):
                i += 1
                date = datetime.datetime.today() + relativedelta(days = -i)
                date_list.append(date.strftime('%Y-%m-%d'))
                date_index = date
        date_list.reverse()
        return date_list
    if id == 'Year':
        # get the end date to stop and return date_list
        end_date = datetime.datetime.today() + relativedelta(years = -number)
        # get starting date for indexing
        date_index = datetime.datetime.today()
        # append start date to date_list
        date_list.append(date_index.strftime('%Y-%m-%d'))
        if number == 1:
            # untill date_index get to end_date keep getting every day into date_list
            while date_index.strftime('%Y-%m-%d') != end_date.strftime('%Y-%m-%d'):
                i += 1
                date = datetime.datetime.today() + relativedelta(days = -i)
                date_list.append(date.strftime('%Y-%m-%d'))
                date_index = date
        if number == 5:
            while date_index.strftime('%Y-%m-%d') != end_date.strftime('%Y-%m-%d'):
                i += 1
                date = datetime.datetime.today() + relativedelta(days = -i)
                date_list.append(date.strftime('%Y-%m-%d'))
                date_index = date
        date_list.reverse()
        return date_list


def get_y_axis_data(stock_symbol, id, number):   # id will tell us if its days,months, years
                                    # and number will tell us how many days,months,..
    # get a all data from a given start date only
    if id == 'Day':
        ts = TimeSeries(key = 'H2AKUMZSFASPIHZH', output_format = 'pandas')
        data = ts.get_intraday(symbol = stock_symbol, interval='5min', outputsize = 'full')[0]
        start_date = datetime.datetime.today() + relativedelta(days = -number)
        clean_data = data[start_date:]['4. close']
        float_list = []
        index = 0
        for _ in clean_data:
            float_list.append(clean_data[:][index])
            index += 1
        return float_list
    if id == 'Month':
        ts = TimeSeries(key = 'H2AKUMZSFASPIHZH', output_format = 'pandas')
        data = ts.get_daily_adjusted(symbol = stock_symbol, outputsize = 'full')[0]
        start_date = datetime.datetime.today() + relativedelta(months = -number)
        clean_data = data[start_date:]['4. close']
        float_list = []
        index = 0
        for _ in clean_data:
            float_list.append(clean_data[:][index])
            index += 1
        return float_list
    if id == 'Year':
        ts = TimeSeries(key = 'H2AKUMZSFASPIHZH', output_format = 'pandas')
        data = ts.get_daily_adjusted(symbol = stock_symbol, outputsize = 'full')[0]
        start_date = datetime.datetime.today() + relativedelta(years = -number)
        clean_data = data[start_date:]['4. close']
        float_list = []
        index = 0
        for _ in clean_data:
            float_list.append(clean_data[:][index])
            index += 1
        return float_list

def get_stockcharts(stock_symbol, id, number):
    # get all stock data
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = get_x_axis_dates(id, number),
        y = get_y_axis_data(stock_symbol, id, number)
    ))

    fig.update_layout(
        title = f"{stock_symbol} {number} {id} Stock Chart",
        margin = dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="LightSteelBlue",
        autosize=True,
        width=650,
        height=550,
    )
    graph_to_div = Markup(plot(fig, output_type='div'))

    return graph_to_div

def get_freshGraph():
    # get all stock data
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = [],
        y = []
    ))

    fig.update_layout(
        margin = dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="LightSteelBlue",
        autosize=True,
        width=650,
        height=550,
    )
    graph_to_div = Markup(plot(fig, output_type='div'))

    return graph_to_div