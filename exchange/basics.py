import pandas as pd
import numpy as np
from binance.client import Client
from parameters import keys


pd.options.display.float_format = '{:.8f}'.format


def connect():
    print('Connecting...')
    client = Client(api_key=keys.Public, api_secret=keys.Secret)
    return client


def portfolio(client):
    print('Fetching portfolio')
    df = pd.DataFrame(client.get_account()['balances'])
    df['free'] = df['free'].astype(float)
    df['locked'] = df['locked'].astype(float)
    df['total'] = df['free'] + df['locked']
    df = df[df['total'] > 0]
    df['account'] = df.asset.str[:2] == 'LD'
    df['account'] = df['account'].map({True: 'Earn', False: 'Spot'})
    df['asset'] = np.where(df.account == 'Earn', df.asset.str[2:], df.asset)
    df.sort_values(by=['account', 'asset'], inplace=True)
    df = df[['account', 'asset', 'free', 'locked', 'total']].reset_index(drop=True)

    return df


def calculate_btc_val(client, portfolio):
    prices = []

    for coin in portfolio['asset']:
        if (coin[:3] == 'USD') | (coin[-3:] == 'USD'):
            price = float(client.get_ticker(symbol='BTC' + coin)['lastPrice'])
            price = portfolio[portfolio['asset'] == coin]['total'].values[0].astype(float) / price
        elif coin != 'BTC':
            price = float(client.get_ticker(symbol=coin + 'BTC')['lastPrice'])
            price *= portfolio[portfolio['asset'] == coin]['total'].values[0].astype(float)
        else:   # case if coin == 'BTC'
            price = portfolio[portfolio['asset'] == coin[-3:]]['total'].values[0].astype(float)
        prices.append(price)

    portfolio['BTC'] = [x.round(8) for x in prices]

    return portfolio
