#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from datetime import datetime, timezone
import time
from trade_analys import Analys
import numpy as np

def bot(client):
    analys = Analys()
    analys.set_history_data(client.klines("BTCUSDT", "1m", limit=60))
    amoumt = 0
    
    while True:
        new_kline = client.klines("BTCUSDT", "1m", limit=2)
        if (analys.get_last_time() < new_kline[0][0]):
            analys.set(new_kline[0])
        if (analys.falling_flat() or analys.upping_flat()):
            position = True
            if (analys.change_price(3) <= 0):

                """имитируем ПОКУПКУ и логируем данные (сейчас в консоль)"""
                opening_time = datetime.now()
                opening_price = float(new_kline[1][4])
                take_profit = opening_price + analys.get_tp()
                stop_loss = opening_price - analys.get_sl()

                print('NEW POSITION UP', opening_time, opening_price, "---", "take_profit =", take_profit, "stop_loss =", stop_loss)

                while position:
                    new_kline = client.klines("BTCUSDT", "1m", limit=2)
                    current_price = float(new_kline[1][4])
                    if (analys.get_last_time() < new_kline[0][0]):
                        analys.set(new_kline[0])
                    if (current_price <= stop_loss):
                        amoumt-=(opening_price - current_price)
                        print('CLOSE', opening_time, "  -", opening_price - current_price, "=", amoumt)
                        position = False
                        break
                    elif (current_price >= take_profit):
                        amoumt+=(current_price - opening_price)
                        print('CLOSE', opening_time, "  +", current_price - opening_price, "=", amoumt)
                        position = False
                        break
            
            else:
                """имитируем ПРОДАЖУ и логируем данные (сейчас в консоль)"""
                opening_time = datetime.now()
                opening_price = float(new_kline[1][4])
                take_profit = opening_price - analys.get_tp()
                stop_loss = opening_price + analys.get_sl()

                print('NEW POSITION DOWN', opening_time, opening_price, "---", "take_profit =", take_profit, "stop_loss =", stop_loss)
                
                while position:
                    new_kline = client.klines("BTCUSDT", "1m", limit=2)
                    current_price = float(new_kline[1][4])
                    if (analys.get_last_time() < new_kline[0][0]):
                        analys.set(new_kline[0])
                    if (current_price >= stop_loss):
                        amoumt-=(current_price - opening_price)
                        print('CLOSE', opening_time, "  -", current_price - opening_price, "=", amoumt)
                        position = False
                        break
                    elif (current_price <= take_profit):
                        amoumt+=(opening_price - current_price)
                        print('CLOSE', opening_time, "  +", opening_price - current_price, "=", amoumt)
                        position = False
                        break
      


def main():
    config = ConfigParser()
    config.read("./config.ini")

    #config_logging(logging, logging.DEBUG)

    api_key = config["keys"]["api_key"]
    api_secret = config["keys"]["api_secret"]

    client = Client(api_key, api_secret)

    bot(client)


if __name__ == "__main__":
    main()