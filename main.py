#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from datetime import datetime, timezone
import time
from trade_analys import Parameters

def check_strategy_1m(client, symbol: str, limit: int):
    
    klines_data = client.klines(symbol, "1m", limit=limit)

    """Сделать проверку массива свечей"""
    iter = 0
    strategy_amoumt = 0
    params = Parameters()
    while iter < len(klines_data):
        params.set(klines_data[iter])

        if iter > 9:

            if (-1*params.get_flat() <= float(klines_data[iter][1]) - float(klines_data[iter][4]) <= params.get_flat()):
                """1)Определить тренд за последние N минут."""
                falling = klines_data[iter][4] < klines_data[iter-7][1]
                falling_3m = klines_data[iter][4] < klines_data[iter-3][1]
                falling_10m = klines_data[iter][4] < klines_data[iter-10][1]

                if (falling):
                    """на падении мы покупаем. Выставляем стопы"""
                    tmp_iter = iter
                    take_profit = float(klines_data[iter][4]) + params.get_tp()
                    stop_loss = float(klines_data[iter][4]) - params.get_sl()

                    while (iter < len(klines_data)-1):
                        iter+=1
                        if (float(klines_data[iter][3]) <= stop_loss):
                            strategy_amoumt-=params.get_sl()
                            print('UPPING ', datetime.fromtimestamp(klines_data[tmp_iter][0]/1000), "---",
                                datetime.fromtimestamp(klines_data[iter][0]/1000), "  -", params.get_sl(), "  =", strategy_amoumt)
                            break
                        elif (float(klines_data[iter][2]) >= take_profit):
                            strategy_amoumt+=params.get_tp()
                            print('UPPING ', datetime.fromtimestamp(klines_data[tmp_iter][0]/1000), "---",
                                datetime.fromtimestamp(klines_data[iter][0]/1000), "  +", params.get_tp(), "    =", strategy_amoumt)
                            break
                
                elif (not falling):
                    """При росте мы продаём. Выставляем стопы"""
                    tmp_iter = iter
                    take_profit = float(klines_data[iter][4]) - params.get_tp()
                    stop_loss = float(klines_data[iter][4]) + params.get_sl()

                    while (iter < len(klines_data)-1):
                        iter+=1
                        if (float(klines_data[iter][2]) >= stop_loss):
                            strategy_amoumt-=params.get_sl()
                            print('FALLING', datetime.fromtimestamp(klines_data[tmp_iter][0]/1000), "---",
                                datetime.fromtimestamp(klines_data[iter][0]/1000), "  -", params.get_sl(), "  =", strategy_amoumt)
                            break 
                        elif (float(klines_data[iter][3]) <= take_profit):
                            strategy_amoumt+=params.get_tp()
                            print('FALLING', datetime.fromtimestamp(klines_data[tmp_iter][0]/1000), "---",
                                datetime.fromtimestamp(klines_data[iter][0]/1000), "  +", params.get_tp(), "    =", strategy_amoumt)
                            break 
           
        iter+=1
    print("AMOUNT FOR DAY = ", strategy_amoumt)         


def main():
    config = ConfigParser()
    config.read("./config.ini")

    #config_logging(logging, logging.DEBUG)

    api_key = config["keys"]["api_key"]
    api_secret = config["keys"]["api_secret"]

    client = Client(api_key, api_secret)
    
    check_strategy_1m(client, "BTCUSDT", 1440)


if __name__ == "__main__":
    main()