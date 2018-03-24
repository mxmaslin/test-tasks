import os

import pandas as pd


prices_path = os.path.join('data', 'prices.csv')

assets_initial = pd.read_csv(prices_path, header=0)
assets = assets_initial.fillna(method='ffill')

assets_t = assets.iloc[1:, 1:].reset_index(drop=True)
assets_t_minus = assets.iloc[:-1, 1:].reset_index(drop=True)

assets_return = assets_t.subtract(assets_t_minus)


print(assets_return)
