# -*- coding: utf-8 -*-
from datetime import date
import os

import pandas as pd


class PortfolioCalculator:
    def __init__(self, prices_fname='prices.csv', weights_fname='weights.csv'):
        self.prices_fname = prices_fname
        self.weights_fname = weights_fname

    def calculate_asset_performance(self, start_date, end_date):
        assets = self._get_assets(start_date, end_date)
        assets_diff = self._get_assets_diff(assets)
        print(assets_diff)

    def _get_assets(self, start_date, end_date):
        prices_path = os.path.join('data', self.prices_fname)
        return (pd.read_csv(prices_path)
                  .fillna(method='ffill')
                  .set_index('date')
                  .loc[start_date:end_date])

    def _get_assets_diff(self, assets):
        return assets.diff().iloc[1:]

    def calculate_currency_performance(self, start_date, end_date):
        weights = self._get_weights(start_date, end_date)

    def _get_weights(self):
        weights_path = os.path.join('data', self.weights_fname)
        weights = pd.read_csv(weights_path)
        weights.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        weights.set_index('date')
        weights.sort_index(axis=1, inplace=True)
        return weights

# def calculate_asset_performance(start_date, end_date):
    # print(assets_return)
    # print(assets.iloc[:-1])
    # assets_return = assets_return.divide(assets.iloc[:-1])
    # assets_return = assets_return.dropna()
    # print(assets.iloc[:-1])
    # merged = (assets_return
    #     .merge(weights, how='outer', left_index=True, right_index=True)
    #     .dropna(subset=['AT0000A18XM4 SW', 'BE0974268972 BB', 'DE0007164600 GR', 'US0527691069 US', 'US6092071058 US'])
    #     .fillna(method='ffill'))
    # print(assets)


if __name__ == '__main__':
    pc = PortfolioCalculator()
    pc.calculate_asset_performance('2014-01-13', '2018-03-05')
