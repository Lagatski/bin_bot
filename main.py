#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from datetime import datetime
import time
import pandas as pd


from bot import Bot
from loan import Loan


def main():
    config = ConfigParser()
    config.read("./config.ini")

    #config_logging(logging, logging.DEBUG)

    api_key = config["keys"]["api_key"]
    api_secret = config["keys"]["api_secret"]
    client = Client(api_key, api_secret)
    bot = Bot(client)
    bot.trade()
    

    #print(int(time.time() * 1000) - client.time()['serverTime']) # binance->api.py 79 строчка, костыль со временем

    #print(client.isolated_margin_account()['assets'][0]['baseAsset']['free']) #БАЛАНС BTC
    #print(client.isolated_margin_account()['assets'][0]['quoteAsset']['free']) #БАЛАНС TUSD
    



if __name__ == "__main__":
    main()