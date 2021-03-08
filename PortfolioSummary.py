from exchange.basics import connect, portfolio, calculate_btc_val
from functions.orders import get_orders
from functions.deposits import get_deposits
from functions.operations import operations
from MarketData import get_selected_history, get_market_periods
import pandas as pd

pd.options.display.float_format = '{:.8f}'.format

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)
    portfolio = calculate_btc_val(client, portfolio)
    orders = get_orders(client, portfolio, save=False)
    deposits = get_deposits(client)
    operations = operations(deposits, orders)
    market_periods = get_market_periods(operations)
    market_data = get_selected_history(client, market_periods)
