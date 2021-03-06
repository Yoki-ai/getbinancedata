import requests
import json
import pandas as pd
import datetime as dt


def get_binance_bars(symbol, interval, startTime, endTime):

    url = "https://api.binance.com/api/v3/klines" #where are you getting the data from (read docs)

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'

    req_params = {"symbol": symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))

    if (len(df.index) == 0):
        return None

    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.open = df.open.astype("float")
    df.high = df.high.astype("float")
    df.low = df.low.astype("float")
    df.close = df.close.astype("float")
    df.volume = df.volume.astype("float")

    df['adj_close'] = df['close']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]

    return df


months = [dt.datetime(2020, i, 1) for i in range(1, 13)]
months.append(dt.datetime(2021, 1, 1))
# Change ticker(BTCUSDT) and interval(1m) to whichever you want
df_list = [get_binance_bars('BTCUSDT', '1m', months[i], months[i+1] - dt.timedelta(0, 1)) for i in range(0, len(months) - 1)]
# Concatenate list of dfs in 1 df
df = pd.concat(df_list)

df_list = []
last_datetime = dt.datetime(2017, 9, 1)
while True:
    print(last_datetime)
    # Change ticker(BTCUSDT) and interval(1m) to whatever you want
    new_df = get_binance_bars('BTCUSDT', '1m', last_datetime, dt.datetime.now())
    if new_df is None:
        break
    df_list.append(new_df)
    last_datetime = max(new_df.index) + dt.timedelta(0, 1)

df = pd.concat(df_list)
#rename the file.
df.to_csv('1minbtcbinance.csv', index=False)
