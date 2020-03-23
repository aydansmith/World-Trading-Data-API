import requests
import json
import pandas as pd


# sort dataframe based on largest percentage rises
def get_best(dataframe, num):
    sorted_by_best = dataframe.sort_values(by=['Percentage Rise'], ascending=False)
    reindexed2 = sorted_by_best.reset_index(drop=True)
    best = reindexed2[:num]
    return best


# sort dataframe based on largest percentage falls
def get_worst(dataframe, num):
    sorted_by_worst = dataframe.sort_values(by=['Percentage Rise'], ascending=False)
    reindexed2 = sorted_by_worst.reset_index(drop=True)
    worst = reindexed2[:num]
    return worst


# adds point drop, point rise, percentage drop, percentage rise, and next day change at open
def add_all(dataframe):
    add_point_drop(dataframe)
    add_point_rise(dataframe)
    add_percentage_drop(dataframe)
    add_percentage_rise(dataframe)
    add_change_to_next_day_open(dataframe)
    return dataframe


# adds difference between previous day close and current day low
def add_point_drop(dataframe):
    length = len(dataframe.index)
    point_drop_list = ['0'] * length
    for x in range(length - 1):
        previous_close = float(dataframe['close'][x + 1])
        current_low = float(dataframe['low'][x])
        point_drop_list[x] = str(round(previous_close - current_low, 2))
    dataframe['point drop'] = point_drop_list
    return dataframe


# adds difference between current day high and previous day close
def add_point_rise(dataframe):
    length = len(dataframe.index)
    point_rise_list = ['0'] * length
    for x in range(length - 1):
        previous_close = float(dataframe['close'][x + 1])
        current_high = float(dataframe['high'][x])
        point_rise_list[x] = str(round(current_high - previous_close, 2))
    dataframe['point rise'] = point_rise_list
    return dataframe


# adds percent fall of current day low in comparison to previous day close
def add_percentage_drop(dataframe):
    length = len(dataframe.index)
    percentage_drop_list = ['0'] * length
    for x in range(length - 1):
        previous_close = float(dataframe['close'][x + 1])
        point_drop = float(dataframe['point drop'][x])
        percentage_drop_list[x] = str(round(point_drop / previous_close, 8))
    dataframe['percentage drop'] = percentage_drop_list
    return dataframe


# adds percent rise of current day low in comparison to previous day close
def add_percentage_rise(dataframe):
    length = len(dataframe.index)
    percentage_rise_list = ['0'] * length
    for x in range(length - 1):
        previous_close = float(dataframe['close'][x + 1])
        point_rise = float(dataframe['point rise'][x])
        percentage_rise_list[x] = str(round(point_rise / previous_close, 8))
    dataframe['percentage rise'] = percentage_rise_list
    return dataframe


# adds the difference between the next day's open and the current date's close
def add_change_to_next_day_open(dataframe):
    length = len(dataframe.index)
    x = 1
    change_to_next_day_open_list = ['0'] * length
    while x < length:
        next_day_open = float(dataframe['open'][x - 1])
        current_close = float(dataframe['close'][x])
        change_to_next_day_open_list[x] = str(round(next_day_open - current_close, 2))
        x = x + 1
    dataframe['change to next day open'] = change_to_next_day_open_list
    return dataframe


class DataAPIClass:
    # takes ticker and api token as input
    def __init__(self, ticker, apiKey):
        self.historicalURL = 'https://api.worldtradingdata.com/api/v1/history'
        self.symbol = ticker
        self.apiToken = apiKey

    # returns dataframe of historical data  with date, open, close, high, and low
    def get_historical_dataframe(self):
        params = {
            'symbol': self.symbol,
            'api_token': self.apiToken
        }
        response = requests.request('GET', self.historicalURL, params=params)
        data = response.json()
        data = data['history']
        data = pd.DataFrame.from_dict(data, orient='index')
        data = data.rename_axis('date').reset_index()
        return data
