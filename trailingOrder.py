from exchange.basics import connect
from functions.trailOrder import trailing_bot

if __name__ == '__main__':
    client = connect()

    params = {
        'coin': 'BTC',
        'pair': 'USDT',
        'side': 'BUY',
        'price': 52000,
        'val': 1000,
        'deviation': ('V', 275)  # 'P' (percentage 0.01-100.00) or 'V' (value >0)
    }

    trailing_bot(client, params, test=True)
