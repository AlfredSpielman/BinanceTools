import pandas as pd
import numpy as np
from datetime import date
from parameters.params import Coins
from functions.misc import folder_check, gogogo

pd.options.display.float_format = '{:.8f}'.format


def order_tailor(start, end, steps, coins):
    x = np.linspace(start, end, steps)
    mean = np.mean(x)
    sd = np.std(x)
    prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    df = pd.DataFrame(prob_density, columns=['distribution'])
    df = df.apply(lambda x: x / df['distribution'].sum())
    df['price'] = x
    df['coins'] = df['distribution'] * coins

    return df


def set_price(cost, margin):
    price = cost * (1 + margin)
    return price


def get_cost(coin):
    df = pd.read_excel('assets.xlsx')
    return df[df['coin'] == coin]['cost'][0]


def get_orders(client, portfolio, save):
    print('Fetching all orders')

    order_types = {
        'symbol': object,
        'orderId': object,
        'orderListId': object,
        'clientOrderId': object,
        'price': float,
        'origQty': float,
        'executedQty': float,
        'cummulativeQuoteQty': float,
        'status': object,
        'timeInForce': object,
        'type': object,
        'side': object,
        'stopPrice': float,
        'icebergQty': float,
        'time': 'datetime64[ns]',
        'updateTime': 'datetime64[ns]',
        'isWorking': bool,
        'origQuoteOrderQty': float}

    df = pd.DataFrame()

    for coin in portfolio['asset']:
        try:
            df_coin = pd.DataFrame(client.get_all_orders(symbol=coin + 'USDT'))
            for col in ['time', 'updateTime']:
                df_coin[col] = pd.to_datetime(df_coin[col], unit='ms')

            df_coin = df_coin.astype(order_types)
            df_coin['p%'] = Coins[coin]['provision']
            df_coin['provision'] = df_coin['p%'] * df_coin['cummulativeQuoteQty']
            del df_coin['p%']
            df = df.append(df_coin)

        except Exception as e:  # binance.exceptions.BinanceAPIException: APIError(code=-1121): Invalid symbol.
            if 'code=-1121' in str(e):
                pass

    if save is True:
        folder_check('orders')
        today = date.today().strftime('%Y-%m-%d')
        df.to_csv(f'orders/{today}_orders.csv', index=False)

    df.reset_index(drop=True, inplace=True)

    return df


def order_summary(df):
    summary = pd.DataFrame(
        df[df.status == 'FILLED'].groupby(['symbol', 'side'])['executedQty'].sum().reset_index()).pivot(
        index='symbol', columns='side', values='executedQty')

    return summary


def post_order(client, coin, pair, quantity, price, side):
    client.create_order(
        symbol=coin + pair,
        side=side,
        type='LIMIT',
        timeInForce='TIME_IN_FORCE_GTC',
        quantity=quantity,
        price=price)


def place_orders(client, orders, coin, pair, side):
    last = len(orders) - 1
    for i, r in orders.iterrows():

        price = round(r.price, Coins[coin]['price'])
        if side == 'SELL':
            quantity = round(r.coins, Coins[coin]['lot'])
        else:
            quantity = round(r.coins/r.price, Coins[coin]['lot'])

        if last < i:
            post_order(client, coin=coin, pair=pair, quantity=quantity, price=price, side=side)
        else:
            free = client.get_asset_balance(asset=coin)
            post_order(client, coin=coin, pair=pair, quantity=free, price=price, side=side)


def order_manager(client, portfolio, side, coin, pair, start_margin, end_margin, part, steps):
    if side == 'SELL':
        cost = get_cost(coin)
        amount = portfolio[portfolio['asset'] == coin]['total'].reset_index(drop=True)[0]
    elif side == 'BUY':
        cost = float(client.get_ticker(symbol='BTCUSDT')['lastPrice'])
        amount = portfolio[portfolio['asset'] == pair]['total'].reset_index(drop=True)[0]
    else:
        print(f'Wrong side: {side}\nShould be "BUY" or "SELL".')
        return

    start = set_price(cost, margin=start_margin)
    end = set_price(cost, margin=end_margin)
    amount *= part

    orders = order_tailor(start=start, end=end, steps=steps, coins=amount)
    if gogogo(coin, pair, side, amount, start, start_margin, end, end_margin) == 'Y':
        place_orders(client, orders, coin, pair, side)
