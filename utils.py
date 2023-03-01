#!/usr/bin/env python

from datetime import datetime


def print_info(self, deal_direction: str, time: int):
    print('NEW position ' + deal_direction + ' (' + str(time) + 'm)', datetime.now(), 
        self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)


def round(quantity: float, symbol: str):
    if symbol == 'BTC':
        if quantity < 10:
            return float(str(quantity)[:7])
        elif quantity < 100:
            return float(str(quantity)[:8])
        elif quantity < 1000:
            return float(str(quantity)[:9])
    elif symbol == 'USDT':
        return (round(quantity, 2))