from parameters.params import Pairs
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.8f}'.format


def operations(deposits, orders):  # deposits, orders
    df1 = pd.DataFrame()
    df1[['timeStamp', 'amount', 'asset']] = deposits[['insertTime', 'amount', 'asset']].copy()

    df2 = pd.DataFrame()
    cols = ['updateTime', 'symbol', 'side', 'price', 'executedQty', 'cummulativeQuoteQty', 'provision']
    df2[['timeStamp', 'symbol', 'side', 'price', 'executedQty', 'cummulativeQuoteQty', 'provision']] = orders[
        orders['executedQty'] > 0][cols].copy()

    df = pd.concat([df1, df2], ignore_index=True, sort=False)
    df['side'].fillna('DEPOSIT', inplace=True)
    df['symbol'].fillna(df['asset'], inplace=True)
    df['executedQty'].fillna(df['amount'], inplace=True)
    df = df.sort_values(by=['timeStamp'], ascending=True).reset_index(drop=True)

    df = givers_takers(df)

    return df


def givers_takers(df):
    df['taker'] = df['asset'].apply(lambda x: x if not x == '' else '')
    df['right'] = df['taker'].fillna(df['symbol'].apply(
        lambda x: str(x)[-4:] if str(x)[-4:] in Pairs[4] else (str(x)[-3:]) if str(x)[-3:] in Pairs[3] else ''))
    df['left'] = df['taker'].fillna(df['symbol'].apply(
        lambda x: str(x)[:-4] if str(x)[-4:] in Pairs[4] else (str(x)[:-3]) if str(x)[-3:] in Pairs[3] else ''))

    giver, taker, giver_qty, taker_qty = [], [], [], []
    for index, row in df.iterrows():
        if row.side == 'BUY':
            giver.append(row.right)
            giver_qty.append(-row.cummulativeQuoteQty)
            taker.append(row.left)
            taker_qty.append(row.executedQty - row.provision)
        elif row.side == 'SELL':
            giver.append(row.left)
            giver_qty.append(-row.executedQty)
            taker.append(row.right)
            taker_qty.append(row.cummulativeQuoteQty - row.provision)
        else:
            giver.append(np.NaN)
            giver_qty.append(np.NaN)
            taker.append(row.asset)
            taker_qty.append(row.amount)

    df['taker'] = taker
    df['giver'] = giver
    df['taker_Qty'] = taker_qty
    df['giver_Qty'] = giver_qty

    for col in ['left', 'right', 'amount', 'asset']:
        del df[col]

    return df