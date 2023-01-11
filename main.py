#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from configparser import ConfigParser
from bot import Bot


def main():
    config = ConfigParser()
    config.read("./config.ini")

    #config_logging(logging, logging.DEBUG)

    api_key = config["keys"]["api_key"]
    api_secret = config["keys"]["api_secret"]

    client = Client(api_key, api_secret)
    bot = Bot(client)

    #print(client.account())
    bot.trade()



if __name__ == "__main__":
    main()