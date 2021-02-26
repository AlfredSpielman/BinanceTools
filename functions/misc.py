from parameters.params import Coins
import os


def gogogo(coin, pair, side, amount, start, start_margin, end, end_margin):
    amount = round(amount, Coins[coin]['lot'])
    start = round(start, Coins[coin]['price'])
    end = round(end, Coins[coin]['price'])
    start_margin = round(start_margin * 100, 2)
    end_margin = round(end_margin * 100, 2)

    class Color:
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'

    if side == 'SELL':
        question = input(f'{Color.CYAN}Do you want to open {Color.RED}{side}{Color.CYAN}'
                         f' orders of {Color.RED}{amount}{Color.CYAN} {Color.RED}{coin}{Color.CYAN}'
                         f' for {Color.RED}{pair}{Color.CYAN}\n'
                         f'starting at : {Color.GREEN}{start} ({start_margin}%){Color.CYAN}\n'
                         f'ending at   : {Color.GREEN}{end} ({end_margin}%){Color.CYAN}\n'
                         f'average     : {Color.GREEN}{(start+end)/2}\n'
                         f'{Color.BOLD}Y/N{Color.END} ? --> ')
    else:
        question = input(f'{Color.CYAN}Do you want to open {Color.RED}{side}{Color.CYAN}'
                         f' orders of {Color.RED}{coin}{Color.CYAN}'
                         f' for {Color.RED}{amount} {pair}{Color.CYAN}\n'
                         f'starting at : {Color.GREEN}{start} ({start_margin}%){Color.CYAN}\n'
                         f'ending at   : {Color.GREEN}{end} ({end_margin}%){Color.CYAN}\n'
                         f'average     : {Color.GREEN}{(start+end)/2}\n'
                         f'{Color.BOLD}Y/N{Color.END} ? --> ')

    question = question.upper()

    return question


def folder_check(folder):
    if folder not in os.listdir():
        os.mkdir(folder)
