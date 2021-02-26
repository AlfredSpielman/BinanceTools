from exchange.basics import connect, portfolio
from functions.orders import order_manager

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'BTC'                # <-- INPUT !!!
    pair = 'USDT'               # <-- INPUT !!!
    side = 'BUY'                # <-- INPUT !!!
    start_margin = -0.5        # <-- INPUT !!!
    end_margin = -0.1          # <-- INPUT !!!
    part = 0.02                 # <-- How much of asset to be used?
    steps = 5                  # <-- INPUT !!!

    order_manager(client, portfolio, side, coin, pair, start_margin, end_margin, part, steps)
    # TODO BinanceAPIException: APIError(code=-1000): An unknown error occured while processing the request.
