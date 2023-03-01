#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from datetime import datetime
import time
from bot import Bot


def main():
    config = ConfigParser()
    config.read("./config.ini")

    #config_logging(logging, logging.DEBUG)

    api_key = config["keys"]["api_key"]
    api_secret = config["keys"]["api_secret"]

    deposit = 500 # Пока что депозит захардкодим
    client = Client(api_key, api_secret)
    #base_url="https://testnet.binance.vision"
    #bot = Bot(client, deposit)
    #bot.trade()
    
    print(client.margin_borrow(asset='BTC', amount='0.01', symbol='BTCUSDT', isIsolated=True))
    #print(client.margin_fee(vipLevel=0, coin="USDT"))
    #print(client.margin_repay(asset='BTC', amount='0.10000040', symbol='BTCUSDT', isIsolated=True))
    
    #print(client.loan_borrow(loanCoin='USDT', collateralCoin='USDT', loanTerm=7))

    
    """params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "MARKET",
        "quantity": 0.225
    }
    print(client.new_order(**params))"""

    #print(int(time.time() * 1000) - client.time()['serverTime']) # binance->api.py 79 строчка, костыль со временем

    #print(client.account_snapshot('MARGIN'))

    #['snapshotVos'][6]['data']



if __name__ == "__main__":
    main()