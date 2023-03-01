#!/usr/bin/env python

from datetime import datetime
import utils


def control_test_position(self, deal_direction: str, deal_amount: float):
    while self.position:
        new_kline = self.client.klines("BTCUSDT", "1m", limit=2)
        if self.analys.get_last_time() < new_kline[0][0]:
            self.analys.set(new_kline[0])
        current_price = float(new_kline[1][4])
        if deal_direction == 'BUY' and current_price <= self.stop_loss:
            delta = _round(self.deposit - deal_amount*current_price, 'USDT')
            self.deposit-=delta
            print('BUY SL/CLOSE', datetime.now(), "  -", delta, "=", self.deposit)
            self.position = False
        elif deal_direction == 'BUY' and current_price >= self.take_profit:
            delta = _round(deal_amount*current_price - self.deposit, 'USDT')
            self.deposit+=delta
            print('BUY TP/CLOSE', datetime.now(), "  +", delta, "=", self.deposit)
            self.position = False
        elif deal_direction == 'SELL' and current_price >= self.stop_loss:
            delta = _round(deal_amount*current_price - self.deposit, 'USDT')
            self.deposit-=delta
            print('SELL SL/CLOSE', datetime.now(), "  -", delta, "=", self.deposit)
            self.position = False
        elif deal_direction == 'SELL' and current_price <= self.take_profit:
            delta = _round(self.deposit - deal_amount*current_price, 'USDT')
            self.deposit+=delta
            print('SELL TP/CLOSE', datetime.now(), "  +", delta, "=", self.deposit)
            self.position = False


def new_test_order(self, deal_direction: str, time: int, new_kline: list):
    self.opening_price = float(new_kline[1][4])
    if deal_direction == 'BUY':
        borrow_amount_USDT = utils.round(self.deposit / float(new_kline[1][4]), 'USDT')*9 # Заняли USDT для сделки
        deal_amount = self.deposit + borrow_amount_USDT # 
    elif deal_direction == 'SELL':
        borrow_amount_USDT = utils.round(self.deposit / float(new_kline[1][4]), 'USDT')*9 # Заняли USDT для сделки
        deal_amount = self.deposit + borrow_amount_USDT # 
        
    self.stop_loss = float(new_kline[0][4]) - self.analys.get_sl() #SL выставляем от значения последней закрытой свечи
    
    if time == 5:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp() #TP выставляем от значения последней закрытой свечи
    elif time == 3:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp()/2 #TP выставляем от значения последней закрытой свечи
    
    borrow_amount_BTC = utils.round(self.deposit / float(new_kline[1][4]), 'BTC')*9 # Заняли BTC для сделки


    self.position = True
    utils.print_info(self, deal_direction, deal_amount, time)
    return deal_amount