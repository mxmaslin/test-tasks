# -*- coding: utf-8 -*-
from datetime import date
import os

import pandas as pd


def calculate_asset_performance(start_date, end_date):
    prices_path = os.path.join('data', 'prices.csv')
    weights_path = os.path.join('data', 'weights.csv')

    weights = pd.read_csv(weights_path)
    weights.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
    weights.set_index('date')
    weights.sort_index(axis=1, inplace=True)

    assets = (pd.read_csv(prices_path)
                .fillna(method='ffill')
                .set_index('date')
                .loc[start_date:end_date])
    assets_return = assets.diff().iloc[1:]
    # print(assets_return)
    # print(assets.iloc[:-1])
    assets_return = assets_return.divide(assets.iloc[:-1])
    # assets_return = assets_return.dropna()


    print(assets_return)
    # print(assets.iloc[:-1])


    # merged = (assets_return
    #     .merge(weights, how='outer', left_index=True, right_index=True)
    #     .dropna(subset=['AT0000A18XM4 SW', 'BE0974268972 BB', 'DE0007164600 GR', 'US0527691069 US', 'US6092071058 US'])
    #     .fillna(method='ffill'))



    # print(assets)

calculate_asset_performance('2014-01-13', '2018-03-05')
