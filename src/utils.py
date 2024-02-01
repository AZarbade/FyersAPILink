import os
import pandas as pd 

class GetHistorical:
    def __init__(self, client, stock_info: dict) -> None:
        self.client = client
        self.stock_info = stock_info

    def fetch_data(self):
        res = self.client.history(data = self.stock_info)

        if 'candles' in res:
            stock_data = pd.DataFrame(res['candles'])
            stock_data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            stock_data['timestamp'] = pd.to_datetime(stock_data['timestamp'], unit='s')
            stock_data['timestamp'] = stock_data['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
            stock_data['timestamp'] = stock_data['timestamp'].dt.tz_localize(None)
            stock_data = stock_data.set_index('timestamp')

            return stock_data
        else:
            raise ValueError("Invalid response from Fyers API.")
        