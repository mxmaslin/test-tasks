# -*- coding: utf-8 -*-
from datetime import date
import os

import pandas as pd


def calculate_stuff_return(stuff):
    stuff_diff = stuff.diff().iloc[1:]
    np_numer = stuff_diff.values
    np_denom = stuff[:-1].values
    return pd.DataFrame(np_numer / np_denom,
                        columns=stuff_diff.columns,
                        index=stuff_diff.index)


class AssetReturnCalculator:
    def __init__(self, prices_fname='prices.csv'):
        self.prices_fname = prices_fname

    def calculate_asset_return(self, start_date, end_date):
        assets = self._get_assets(start_date, end_date)
        return calculate_stuff_return(assets)

    def _get_assets(self, start_date, end_date):
        prices_path = os.path.join('data', self.prices_fname)
        return (pd.read_csv(prices_path)
                  .fillna(method='ffill')
                  .set_index('date')
                  .loc[start_date:end_date])


class CurrencyReturnCalculator:
    def __init__(self, exchanges_fname='exchanges.csv'):
        self.exchanges_fname = exchanges_fname

    def calculate_currency_return(self, start_date, end_date):
        currencies = self._get_currencies(start_date, end_date)
        return calculate_stuff_return(currencies)

    def _get_currencies(self, start_date, end_date):
        return 0




class PortfolioCalculator:
    def __init__(self, prices_fname='prices.csv', weights_fname='weights.csv'):
        self.prices_fname = prices_fname
        self.weights_fname = weights_fname

    def calculate_asset_performance(self, start_date, end_date):
        assets = self._get_assets(start_date, end_date)
        assets_diff = assets.diff().iloc[1:]
        np_numer = assets_diff.values
        np_denom = assets[:-1].values
        return pd.DataFrame(np_numer / np_denom,
                               columns=assets_diff.columns,
                               index=assets_diff.index)

    def _get_assets(self, start_date, end_date):
        prices_path = os.path.join('data', self.prices_fname)
        return (pd.read_csv(prices_path)
                  .fillna(method='ffill')
                  .set_index('date')
                  .loc[start_date:end_date])



    # def calculate_currency_performance(self, start_date, end_date):
    #     weights = self._get_weights(start_date, end_date)
    #     print(weights)

    def _get_weights(self, start_date, end_date):
        weights_path = os.path.join('data', self.weights_fname)
        weights = pd.read_csv(weights_path)
        weights.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        columns = weights.columns.values
        columns[3], columns[4] = columns[4], columns[3]
        weights = weights[columns]
        weights.set_index('date', inplace=True)
        weights.fillna(method='ffill')
        return weights






    # merged = (assets_return
    #     .merge(weights, how='outer', left_index=True, right_index=True)
    #     .dropna(subset=['AT0000A18XM4 SW', 'BE0974268972 BB', 'DE0007164600 GR', 'US0527691069 US', 'US6092071058 US'])
    #     .fillna(method='ffill'))
    # print(assets)


if __name__ == '__main__':
    pc = PortfolioCalculator()
    pc.calculate_currency_performance('2014-01-13', '2018-03-06')
