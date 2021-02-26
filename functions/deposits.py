import pandas as pd

pd.options.display.float_format = '{:.8f}'.format


def get_deposits(client):
    print('Fetching crypto deposits')
    df = client.get_deposit_history()
    df = pd.DataFrame(df['depositList'])
    df['insertTime'] = pd.to_datetime(df['insertTime'], unit='ms')
    df = df.sort_values(by=['insertTime'], ascending=True).reset_index(drop=True)

    return df
