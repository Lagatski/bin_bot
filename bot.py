#!/usr/bin/env python

from datetime import datetime
from binance.spot import Spot as Client
from trade_analys import Analys
import trade
#import test
import loan

class Bot:

    def __init__(self, client: Client, deposit: float):
        self.client = client
        self.deposit = deposit
        self.position = False
        self.opening_price = 0
        self.take_profit = 0
        self.stop_loss = 0
        self.analys = Analys()
        self.analys.set_history_data(self.client.klines("BTCUSDT", "1m", limit=60))

    def trade(self):
        while True:
            new_klines = self.client.klines("BTCUSDT", "1m", limit=2)
            if (self.analys.get_last_time() < new_klines[0][0]):
                self.analys.set(new_klines[0])
            
            if self.analys.is_flat() and self.analys.down_trend_5m() and self.analys.approved_price("UP", new_klines[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                deal_amount = trade.new_order(self, 1, new_klines)
                trade.control_position(self, 'UP')

            elif self.analys.is_flat() and self.analys.up_trend_5m() and self.analys.approved_price("DOWN", new_klines[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                deal_amount = trade.new_order(self, 'SELL', 5, new_klines)
                trade.control_position(self)
            
            elif self.analys.is_flat() and self.analys.down_trend_3m() and self.analys.approved_price("UP", new_klines[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                deal_amount = trade.new_order(self, 'BUY', 3, new_klines)
                trade.control_position(self)
            
            elif self.analys.is_flat() and self.analys.up_trend_3m() and self.analys.approved_price("DOWN", new_klines[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                deal_amount = trade.new_order(self, 'SELL', 3, new_klines)
                trade.control_position(self)
    
























    """def test_trade(self):
        while True:
            new_kline = self.client.klines("BTCUSDT", "1m", limit=2)
            if (self.analys.get_last_time() < new_kline[0][0]):
                self.analys.set(new_kline[0])
            
            if self.analys.is_flat() and self.analys.down_trend_5m() and self.analys.approved_price("UP", new_kline[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                deal_amount = test.new_test_order(self, 'BUY', 5, new_kline)
                test.control_test_position(self, 'BUY', deal_amount)

            elif self.analys.is_flat() and self.analys.up_trend_5m() and self.analys.approved_price("DOWN", new_kline[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                deal_amount = test.new_test_order(self, 'SELL', 5, new_kline)
                test.control_test_position(self, 'SELL', deal_amount)
            
            elif self.analys.is_flat() and self.analys.down_trend_3m() and self.analys.approved_price("UP", new_kline[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                deal_amount = test.new_test_order(self, 'BUY', 3, new_kline)
                test.control_test_position(self, 'BUY', deal_amount)
            
            elif self.analys.is_flat() and self.analys.up_trend_3m() and self.analys.approved_price("DOWN", new_kline[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                deal_amount = test.new_test_order(self, 'SELL', 3, new_kline)
                test.control_test_position(self, 'SELL', deal_amount)
    """
 