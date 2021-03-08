from exchange.basics import connect, portfolio
from functions.orders import order_manager
from functions.misc import check_params

if __name__ == '__main__':
    client = connect()
    portfolio = portfolio(client)

    coin = 'XRP'
    pair = 'BTC'
    side = 'BUY'

    # Choose only one:  [Part: None|0-100, Amount: None|int]
    part = 100
    amount = None

    start = 0.00000500
    end = 0.00000600
    steps = 200

    # True = normal distribution, False = linear distribution, [default: False]
    norm_dist = False

    # Do you want to print all orders? [bool, default: True]
    show = True

    run = check_params(coin, pair)

    if run:
        order_manager(client, portfolio,
                      side, coin, pair, start, end, steps, part, amount,
                      norm_dist, show)
