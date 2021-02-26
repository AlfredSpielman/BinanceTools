import pandas as pd
from datetime import date, timedelta
from functions.misc import folder_check
import csv

pd.options.display.float_format = '{:.8f}'.format


def get_history(cli, pf, days, save):
    start_date = date.today() - timedelta(days=days)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    print(f'Fetching market data for {start_date} - {end_date} ({days} days):')

    df = pd.DataFrame()
    for coin in pf['asset']:
        print(f'--> {coin}')
        if coin != 'USDT':
            klines = cli.get_historical_klines(coin + 'USDT', cli.KLINE_INTERVAL_1HOUR, start_date, end_date)
            data = []
            for i in klines:        # keep only 'Open time' and 'Open'
                data.append(i[:2])

            if save is True:
                folder_check('market_data')
                with open(f'market_data/{coin}_{start_date}_{end_date}.csv', 'w') as f:
                    write = csv.writer(f, delimiter=',', lineterminator='\n')
                    write.writerow(['Open time', 'Open'])
                    write.writerows(data)
                    f.close()

            df_temp = pd.DataFrame(data, columns=['Open time', coin])
            df_temp.set_index(['Open time'], inplace=True)

            if len(df) == 0:
                df = df_temp.copy(deep=True)
            else:
                df = df.join(df_temp, on=['Open time'], how='outer')

    df.index = pd.to_datetime(df.index, unit='ms')

    return df


def get_selected_history(cli, ranges):
    pass
