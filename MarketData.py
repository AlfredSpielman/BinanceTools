import pandas as pd

pd.options.display.float_format = '{:.8f}'.format


def get_selected_history(client, market_periods):
    df = pd.DataFrame()

    for selection in market_periods:
        coin = selection.coin + 'BTC'
        start_date = selection.start
        end_date = selection.end

        klines = client.get_historical_klines(coin, client.KLINE_INTERVAL_5MINUTE, start_date, end_date)
        df_selection = pd.DataFrame(klines[['Open time', 'Open']], columns=['Open time', coin])
        df_selection = df_selection.set_index(['Open time'])
        df_selection.index = pd.to_datetime(df_selection.index, unit='ms')

        df.append(df_selection)

    return df


def get_market_periods(operations):
    # TODO work on get_market_periods
    periods = []

    for p in operations:
        periods.append(p)

    return periods
