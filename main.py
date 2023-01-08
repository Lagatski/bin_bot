#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from datetime import datetime, timezone
import time
from trade_analys import Analys

def bot(client):
    analys = Analys()
    analys.set_history_data(client.klines("BTCUSDT", "1m", limit=60))
    strategy_amoumt = 0
    
    while True:
        new_kline = client.klines("BTCUSDT", "1m", limit=2)
        if (analys.get_last_time() < new_kline[0][0]):
            analys.set(new_kline[0])
        if (analys.falling_flat() or analys.upping_flat()): 
            """ВХОД В ПОЗИЦИЮ"""
            position = True
            if (analys.change_price(3) <= 0):
                """НА ПАДЕНИИ ПОКУПАЕМ И ВЫСТАВЛЯЕМ СТОПЫ"""
                start_position_time = datetime.fromtimestamp(new_kline[1][0]/1000)
                take_profit = float(new_kline[1][4]) + analys.get_tp()
                stop_loss = float(new_kline[1][4]) - analys.get_sl()
                print('NEW POSITION', start_position_time, "---", analys.change_price(3), "take_profit =", take_profit,
                    "stop_loss =", stop_loss)
                while position:
                    new_kline = client.klines("BTCUSDT", "1m", limit=2)
                    current_price = float(new_kline[1][4])
                    if (analys.get_last_time() < new_kline[0][0]):
                        analys.set(new_kline[0])
                    if (current_price <= stop_loss):
                        strategy_amoumt-=analys.get_sl()
                        print('UPPING ', start_position_time, "---",
                            datetime.fromtimestamp(new_kline[1][0]/1000), "  -", analys.get_sl(), "  =", strategy_amoumt)
                        position = False
                        break
                    elif (current_price >= take_profit):
                        strategy_amoumt+=analys.get_tp()
                        print('UPPING ', start_position_time, "---",
                            datetime.fromtimestamp(new_kline[1][0]/1000), "  +", analys.get_tp(), "    =", strategy_amoumt)
                        position = False
                        break
            
            else:
                """При росте мы продаём. Выставляем стопы"""
                start_position_time = datetime.fromtimestamp(new_kline[1][0]/1000)
                take_profit = float(new_kline[1][4]) - analys.get_tp()
                stop_loss = float(new_kline[1][4]) + analys.get_sl()
                print('NEW POSITION', start_position_time, "---", analys.change_price(3), "take_profit =", take_profit,
                    "stop_loss =", stop_loss)
                while position:
                    new_kline = client.klines("BTCUSDT", "1m", limit=2)
                    current_price = float(new_kline[1][4])
                    if (analys.get_last_time() < new_kline[0][0]):
                        analys.set(new_kline[0])
                    if (current_price >= stop_loss):
                        strategy_amoumt-=analys.get_sl()
                        print('FALLING', start_position_time, "---",
                            datetime.fromtimestamp(new_kline[1][0]/1000), "  -", analys.get_sl(), "  =", strategy_amoumt)
                        position = False
                        break 
                    elif (current_price <= take_profit):
                        strategy_amoumt+=analys.get_tp()
                        print('FALLING', start_position_time, "---",
                            datetime.fromtimestamp(new_kline[1][0]/1000), "  +", analys.get_tp(), "    =", strategy_amoumt)
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