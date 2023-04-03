#!/usr/bin/env python

from datetime import datetime
from binance.spot import Spot as Client

from trade_analys import Analys
import trade
from loan import Loan

class Bot:

    def __init__(self, client: Client):
        self.client = client
        self.deposit = float(client.isolated_margin_account()['assets'][0]['quoteAsset']['free'])
        print(type(self.deposit))
        print("Bot started with: " + str(round(self.deposit, 2)) + " TUSD")
        self.loan = Loan(client)
        self.position = False
        self.opening_price = 0
        self.closing_price = 0
        self.take_profit = 0
        self.stop_loss = 0
        self.analys = Analys()
        self.analys.set_history_data(self.client.klines("BTCTUSD", "1m", limit=60))
        

    def trade(self):
        while True:
            new_klines = self.client.klines("BTCTUSD", "1m", limit=2)
            if (self.analys.get_last_time() < new_klines[0][0]):
                self.analys.set(new_klines[0])
            
            if self.analys.is_flat() and self.analys.down_trend_5m() and self.analys.approved_price("UP", new_klines[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                trade.start_position(self, 1, new_klines)

            elif self.analys.is_flat() and self.analys.up_trend_5m() and self.analys.approved_price("DOWN", new_klines[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                trade.start_position(self, 3, new_klines)
            
            elif self.analys.is_flat() and self.analys.down_trend_3m() and self.analys.approved_price("UP", new_klines[1]):
                # имитируем ПОКУПКУ и логируем данные (сейчас в консоль)
                trade.start_position(self, 2, new_klines)
            
            elif self.analys.is_flat() and self.analys.up_trend_3m() and self.analys.approved_price("DOWN", new_klines[1]):
                # имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)
                trade.start_position(self, 4, new_klines)
    


 