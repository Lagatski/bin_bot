#!/usr/bin/env python

from enum import Enum
from datetime import datetime
import utils

class Direction(Enum):
    BUY_LONG = 1
    BUY_SHORT = 2
    SELL_LONG = 3
    SELL_SHORT = 4

def control_position(self):
    while self.position:
        new_kline = self.client.klines("BTCUSDT", "1m", limit=2)
        if self.analys.get_last_time() < new_kline[0][0]:
            self.analys.set(new_kline[0])
        current_price = float(new_kline[1][4])
        if current_price <= self.stop_loss:
            self.amount-=(self.opening_price - current_price)
            print('CLOSE', datetime.now(), "  -", self.opening_price - current_price, "=", self.amount)
            self.position = False
        elif current_price >= self.take_profit:
            self.amount+=(current_price - self.opening_price)
            print('CLOSE', datetime.now(), "  +", current_price - self.opening_price, "=", self.amount)
            self.position = False


def new_order(self, deal_direction: Direction, new_kline: list):
    """if deal_direction == Direction.BUY_LONG:

        if loan.get_loan(self.deposit*9):
          
        else:
            print()   
        self.client.margin_borrow(asset='USDT', amount=borrow_amount, symbol='BTCUSDT', isIsolated=True)
    
    elif deal_direction == Direction.BUY_SHORT:

    elif deal_direction == Direction.SELL_LONG:

    elif deal_direction == Direction.SELL_SHORT:
        borrow_amount = utils.round((self.deposit*9) / float(new_kline[1][4]),)
        self.client.margin_borrow(asset='BTC', amount='0.1', symbol='BTCUSDT', isIsolated=True)
    """
    params = {
        "symbol": "BTCUSDT",
        "side": deal_direction,
        "type": "MARKET",
        "quantity": quantity,
        "isIsolated": True
    }

    tmp = self.client.new_margin_order(**params)
    self.opening_price = float(tmp['price']) 

    self.stop_loss = float(new_kline[0][4]) - self.analys.get_sl() #SL выставляем от значения последней закрытой свечи

    if time == 5:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp() #TP выставляем от значения последней закрытой свечи
    elif time == 3:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp()/2 #TP выставляем от значения последней закрытой свечи
    
    self.position = True
    utils.print_info(self)