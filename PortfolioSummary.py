from exchange.basics import connect, portfolio, calculate_btc_val
from functions.orders import get_orders
from functions.deposits import get_deposits
from functions.operations import operations
import pandas as pd

pd.options.display.float_format = '{:.8f}'.format

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)
    portfolio = calculate_btc_val(client, portfolio)
    # market_data = get_history(client, portfolio, days=180, save=False)
    orders = get_orders(client, portfolio, save=False)
    deposits = get_deposits(client)
    operations = operations(deposits, orders)
