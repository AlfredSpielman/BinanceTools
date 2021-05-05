import datetime


def trailing_bot(client, params, test=True):
    print(params)
    boundaries = set_boundaries(params['price'], params['deviation'])
    monitor, trailing = True, False

    while monitor:
        current_price = get_ticker(client, params)
        print_status(current_price, boundaries, trailing, params)

        if not trailing:
            trailing = start_trailing(params, current_price)

        if trailing:
            fire, boundaries = analyze_price(params, boundaries, current_price)
            if fire:
                if not test:
                    market_order(client, params, current_price)
                else:
                    print_result(params, current_price)
                monitor = False


def set_boundaries(price, deviation):
    if deviation[0] == 'V':
        boundaries = (price - deviation[1],
                      price + deviation[1])
    else:
        boundaries = (price - price * (deviation[1] / 100),
                      price + price * (deviation[1] / 100))
    return boundaries


def get_ticker(client, params):
    symbol = params['coin'] + params['pair']
    last_order = client.get_recent_trades(symbol=symbol)[-1]
    return float(last_order['price'])


def start_trailing(params, current_price):
    trail = False

    if params['side'] == 'BUY':
        if current_price <= params['price']:
            trail = True
    else:  # SELL
        if current_price >= params['price']:
            trail = True

    return trail


def analyze_price(params, boundaries, current_price):
    fire = False

    if params['side'] == 'BUY':
        if current_price > boundaries[1]:
            fire = True
        elif current_price < boundaries[0]:
            boundaries = adjust_boundaries(current_price, params)
        else:
            pass
    else:  # SELL
        if current_price < boundaries[0]:
            fire = True
        elif current_price > boundaries[1]:
            boundaries = adjust_boundaries(current_price, params)
        else:
            pass

    return fire, boundaries


def adjust_boundaries(current_price, params):
    deviation = params['deviation']
    if params['side'] == 'BUY':
        if deviation[0] == 'V':
            boundaries = (current_price,
                          current_price + deviation[1] * 2)
        else:
            boundaries = (current_price,
                          current_price + (current_price * (deviation[1] / 100)) * 2)
        print('boundaries down')
    else:  # SELL
        if deviation[0] == 'V':
            boundaries = (current_price - deviation[1] * 2,
                          current_price)
        else:
            boundaries = (current_price - (current_price * (deviation[1] / 100)) * 2,
                          current_price)
        print('boundaries up')

    return boundaries


def market_order(client, params, current_price):
    if params['side'] == 'BUY':
        client.order_market_buy(
            symbol=params['coin'] + params['pair'],
            quantity=params['val'])
    else:  # SELL
        client.order_market_sell(
            symbol=params['coin'] + params['pair'],
            quantity=params['val'])

    print_result(params, current_price)


def print_status(current_price, boundaries, trailing, params):
    now = datetime.datetime.now()
    if trailing:
        print(now.strftime('%Y-%m-%d %H:%M:%S'), '|', 'Trailing', '|',
              boundaries[0], '|', current_price, '|', boundaries[1])
    else:
        print(now.strftime('%Y-%m-%d %H:%M:%S'), '|', 'Monitoring', '|',
              params['side'] + ' at ' + str(params['price']), '|', current_price)


def print_result(params, current_price):
    diff_val = round(current_price - params['price'], 8)
    diff_prc = round((current_price / params['price'] - 1) * 100, 2)

    print(f"side:       {params['side']}\n"
          f"pair:       {params['coin'] + params['pair']}\n"
          f"quantity:   {params['val']}\n"
          f"price:      {current_price} (original {params['price']})\n"
          f"difference: {diff_val} ({diff_prc}%)")
