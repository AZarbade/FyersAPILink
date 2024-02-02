import datetime
import os
import pandas as pd
from pyparsing import col 

class GetHistorical:
    def __init__(self, client, stock_info: dict) -> None:
        self.client = client
        self.stock_info = stock_info

    def fetch_data(self):
        self.info = self.stock_info.copy()
        start_range = datetime.datetime.strptime(self.stock_info['range_from'], '%Y-%m-%d')
        stock_data = pd.DataFrame()

        while start_range <= datetime.datetime.strptime(self.stock_info['range_to'], '%Y-%m-%d'):
            end_range = min(start_range + datetime.timedelta(days=60), datetime.datetime.strptime(self.stock_info['range_to'], '%Y-%m-%d'))
            self.info['range_from'] = start_range.strftime('%Y-%m-%d')
            self.info['range_to'] = end_range.strftime('%Y-%m-%d')
            res = self.client.history(data=self.info)

            if 'candles' in res:
                data = pd.DataFrame(res['candles'])
                data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
                data['timestamp'] = data['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
                data['timestamp'] = data['timestamp'].dt.tz_localize(None)
                data = data.set_index('timestamp')

                stock_data = pd.concat([stock_data, data])

            start_range = end_range + datetime.timedelta(days=1)

        if stock_data.empty:
            raise ValueError("Invalid response from Fyers API.")

        return stock_data
        
    def save_data(self, path: str):
        stock_data = self.fetch_data()
        stock_data.to_csv(path)
        