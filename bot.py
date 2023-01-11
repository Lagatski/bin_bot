#!/usr/bin/env python

from datetime import datetime
from binance.spot import Spot as Client
from trade_analys import Analys

def _control_position(self):
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
            
def _save_parameters(self, time, new_kline):
    self.opening_price = float(new_kline[1][4])
    self.stop_loss = float(new_kline[0][4]) - self.analys.get_sl() #SL выставляем от значения последней закрытой свечи
    if time == 5:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp() #TP выставляем от значения последней закрытой свечи
    elif time == 3:
        self.take_profit = float(new_kline[0][4]) + self.analys.get_tp()/2 #TP выставляем от значения последней закрытой свечи

class Bot:

    def __init__(self, client: Client):
        self.client = client
        self.position = False
        self.amount = 0
        self.opening_price = 0
        self.take_profit = 0
        self.stop_loss = 0
        self.analys = Analys()
        self.analys.set_history_data(self.client.klines("BTCUSDT", "1m", limit=60))

    def trade(self):
        while True:
            new_kline = self.client.klines("BTCUSDT", "1m", limit=2)
            if (self.analys.get_last_time() < new_kline[0][0]):
                self.analys.set(new_kline[0])
            
            if self.analys.is_flat() and self.analys.down_trend_5m() and self.analys.approved_price("UP", new_kline[1]):
                self.position = True # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                _save_parameters(self, 5, new_kline)

                print('NEW position UP (5m)', datetime.now(), self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)
                
                _control_position(self)

            elif self.analys.is_flat() and self.analys.up_trend_5m() and self.analys.approved_price("DOWN", new_kline[1]):
                self.position = True # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                _save_parameters(self, 5, new_kline)

                print('NEW position DOWN (5m)', datetime.now(), self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)
                
                _control_position(self)
            
            elif self.analys.is_flat() and self.analys.down_trend_3m() and self.analys.approved_price("UP", new_kline[1]):
                self.position = True # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                _save_parameters(self, 3, new_kline)

                print('NEW position UP (3m)', datetime.now(), self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)

                _control_position(self)
            
            elif self.analys.is_flat() and self.analys.up_trend_3m() and self.analys.approved_price("DOWN", new_kline[1]):
                self.position = True # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                _save_parameters(self, 3, new_kline)

                print('NEW position DOWN (3m)', datetime.now(), self.opening_price, "---", "take_profit =", self.take_profit, "stop_loss =", self.stop_loss)
                
                _control_position(self)
                
 