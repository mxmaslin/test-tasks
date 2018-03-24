import os

import pandas as pd


def calculate_asset_performance(start_date, end_date):
    prices_path = os.path.join('data', 'prices.csv')

    assets = pd.read_csv(prices_path).\
        fillna(method='ffill').\
        set_index('date').\
        loc[start_date:end_date]

    assets_t = assets[1:].reset_index(drop=True)
    assets_t_minus = assets[:-1].reset_index(drop=True)
    assets_return = assets_t.subtract(assets_t_minus)

    print(assets_return)

calculate_asset_performance('2014-01-13', '2014-01-14')
