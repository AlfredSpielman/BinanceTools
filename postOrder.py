from exchange.basics import connect, portfolio
from functions.misc import check_params
from functions.orders import order_manager

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'BTC'
    pair = 'USDT'
    side = 'BUY'

    # Choose only one:  [Part: None|0-100, Amount: None|int]
    part = None
    amount = 1000

    start = 52000
    end = 54000
    steps = 30

    # True = normal distribution, False = linear distribution, [default: False]
    norm_dist = False

    # Do you want to print all orders? [bool, default: True]
    show = True

    run = check_params(coin, pair)

    if run:
        order_manager(client, portfolio,
                      side, coin, pair, start, end, steps, part, amount,
                      norm_dist, show)
