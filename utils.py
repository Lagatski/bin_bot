#!/usr/bin/env python

from datetime import datetime


def print_info(self):
    print('NEW position', datetime.now(), 
        self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)


def crypto_round(quantity: float, asset: str):
    if asset == 'BTC':
        if quantity < 10:
            return float(str(quantity)[:7])
        elif quantity < 100:
            return float(str(quantity)[:8])
        elif quantity < 1000:
            return float(str(quantity)[:9])
    elif asset == 'TUSD':
        return (round(quantity, 2))