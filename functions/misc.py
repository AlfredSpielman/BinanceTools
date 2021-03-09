from parameters.params import Coins
import os


class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def gogogo(coin, pair, side, amount, start, end, steps):
    amount = round(amount, Coins[coin]['lot'])

    if start > 0.001:
        start_str = round(start, Coins[coin]['price'])
        end_str = round(end, Coins[coin]['price'])
        average = round((start + end) / 2, Coins[coin]['price'])
    else:
        start_str = str(int(round(start * 100000000, 0))) + ' satoshi'
        end_str = str(int(round(end * 100000000, 0))) + ' satoshi'
        average = str(int(round(((start + end) / 2) * 100000000, 0))) + ' satoshi'

    if side == 'SELL':
        question = input(f'{"-"*69}\n'
                         f'{Color.CYAN}Do you want to open {Color.RED}{steps} {side}{Color.CYAN}'
                         f' orders of {Color.RED}{amount}{Color.CYAN} {Color.RED}{coin}{Color.CYAN}'
                         f' for {Color.RED}{pair}{Color.CYAN}\n'
                         f'starting at : {Color.GREEN}{start_str}{Color.CYAN}\n'
                         f'ending at   : {Color.GREEN}{end_str}{Color.CYAN}\n'
                         f'average     : {Color.GREEN}{average}\n'
                         f'{Color.BOLD}Y/N{Color.END} ? --> ')
    else:
        question = input(f'{"-"*69}\n'
                         f'{Color.CYAN}Do you want to open {Color.RED}{steps} {side}{Color.CYAN}'
                         f' orders of {Color.RED}{coin}{Color.CYAN}'
                         f' for {Color.RED}{amount} {pair}{Color.CYAN}\n'
                         f'starting at : {Color.GREEN}{start_str}{Color.CYAN}\n'
                         f'ending at   : {Color.GREEN}{end_str}{Color.CYAN}\n'
                         f'average     : {Color.GREEN}{average}\n'
                         f'{Color.BOLD}Y/N{Color.END} ? --> ')

    question = question.upper()

    return question


def folder_check(folder):
    if folder not in os.listdir():
        os.mkdir(folder)


def check_params(coin, pair):
    run = True
    try:
        Coins[coin]
    except KeyError:
        print(f'{Color.RED}Missing coin {coin} in params.Coins{Color.END}')
        run = False

    try:
        Coins[pair]
    except KeyError:
        print(f'{Color.RED}Missing coin {pair} in params.Coins{Color.END}')
        run = False

    return run
