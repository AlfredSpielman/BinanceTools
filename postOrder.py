from exchange.basics import connect, portfolio
from functions.misc import check_params
from functions.orders import order_manager

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'RSR'
    pair = 'USDT'
    side = 'BUY'

    # Choose only one:  [Part: None|0-100, Amount: None|int]
    part = None
    amount = 1300

    start = 0.092
    end = 0.104
    steps = 120

    # True = normal distribution, False = linear distribution, [default: False]
    norm_dist = False

    run = check_params(coin, pair)
    if run:
        order_manager(client, portfolio, side, coin, pair, start, end, steps, part, amount, norm_dist)
