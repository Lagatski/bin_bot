#!/usr/bin/env python

from enum import Enum
from datetime import datetime
import utils

class Direction(Enum):
    BUY_LONG = 1
    BUY_SHORT = 2
    SELL_LONG = 3
    SELL_SHORT = 4

def _control_position(self, deal_direction: Direction, amount: float):
    while self.position:
        '''Get new info + save last kline'''
        new_kline = self.client.klines("BTCTUSD", "1m", limit=2)
        if self.analys.get_last_time() < new_kline[0][0]:
            self.analys.set(new_kline[0])
        current_price = float(new_kline[1][4])

        '''Checking the position'''
        if (deal_direction == Direction.BUY_LONG or deal_direction == Direction.BUY_SHORT) and \
            (current_price <= self.stop_loss or current_price >= self.take_profit):
            params = {
            "symbol": "BTCTUSD",
            "side": "SELL",
            "type": "MARKET",
            "quantity": amount,
            "isIsolated": True
            }
            order_info = self.client.new_margin_order(**params)
            self.closing_price = float(order_info['price']) 
            self.position = False
            self.loan.put_loan(self)

        elif (deal_direction == Direction.SELL_LONG or deal_direction == Direction.SELL_SHORT) and \
            (current_price >= self.stop_loss or current_price <= self.take_profit):
            params = {
            "symbol": "BTCTUSD",
            "side": "SELL",
            "type": "MARKET",
            "quantity": amount,
            "isIsolated": True
            }
            order_info = self.client.new_margin_order(**params)
            self.closing_price = float(order_info['price']) 
            self.position = False
            self.loan.put_loan(self)

        if self.position == False:
            print('CLOSE', datetime.now(), self.opening_price - self.closing_price, "=", self.amount)
            break


def _new_order(self, deal_direction: Direction, new_kline: list):

    if deal_direction == Direction.BUY_LONG or deal_direction == Direction.BUY_SHORT:
        print('BUY')
        self.stop_loss = float(new_kline[0][4]) - self.analys.get_sl() #SL выставляем от значения последней закрытой свечи
        if deal_direction == Direction.BUY_LONG:
            self.take_profit = float(new_kline[0][4]) + self.analys.get_tp() #TP выставляем от значения последней закрытой свечи
        else:
            self.take_profit = float(new_kline[0][4]) + self.analys.get_tp()/2 #TP выставляем от значения последней закрытой свечи
        amount = self.loan.get_loan('TUSD', new_kline)
        params = {
        "symbol": "BTCTUSD",
        "side": "BUY",
        "type": "MARKET",
        "quantity": amount,
        "isIsolated": True
        }
        self.opening_price = float(self.client.new_margin_order(**params)['price']) 
        self.position = True
        utils.print_info(self) # Next step will be logging
        return amount

    elif deal_direction == Direction.SELL_LONG or deal_direction == Direction.SELL_SHORT:
        print('SELL')
        self.stop_loss = float(new_kline[0][4]) + self.analys.get_sl() #SL выставляем от значения последней закрытой свечи
        if deal_direction == Direction.SELL_LONG:
            self.take_profit = float(new_kline[0][4]) - self.analys.get_tp() #TP выставляем от значения последней закрытой свечи
        else:
            self.take_profit = float(new_kline[0][4]) - self.analys.get_tp()/2 #TP выставляем от значения последней закрытой свечи
        amount = self.loan.get_loan('BTC', new_kline)
        params = {
        "symbol": "BTCTUSD",
        "side": "SELL",
        "type": "MARKET",
        "quantity": amount,
        "isIsolated": True
        }
        self.opening_price = float(self.client.new_margin_order(**params)['price']) 
        self.position = True
        utils.print_info(self) # Next step will be logging
        return amount

def start_position(self, deal_direction: Direction, new_kline: list):
    amount = _new_order(self, deal_direction, new_kline)
    _control_position(self, deal_direction, amount)