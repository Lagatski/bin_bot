#!/usr/bin/env python

from binance.spot import Spot as Client
import time

import utils

class Loan:

    def __init__(self, client: Client):
        self.client = client
        self.deposit = client.isolated_margin_account()['assets'][0]['quoteAsset']['free']
        self.tusd = 0
        self.btc = 0
        self.loan_time = 0

    
    def get_loan(self, loan_asset: str, new_kline: list):
        if loan_asset == 'BTC':
            self.btc = utils.crypto_round((self.deposit*5) / float(new_kline[1][4]), loan_asset)
            self.client.margin_borrow(asset=loan_asset, amount=self.btc, symbol='BTCTUSD', isIsolated=True)
            self.loan_time = time.time()
            return utils.crypto_round(self.btc + (self.deposit)/float(new_kline[1][4]), 'BTC')
        
        elif loan_asset == 'TUSD':
            self.tusd = utils.crypto_round((self.deposit*4), loan_asset)
            self.client.margin_borrow(asset=loan_asset, amount=self.tusd, symbol='BTCTUSD', isIsolated=True)
            self.loan_time = time.time()
            return utils.crypto_round((self.tusd + self.deposit)/float(new_kline[1][4]), 'BTC') # ВОзвращаем сумму в биткоинах для совершения сделки

    def put_loan(self):
        if self.tusd > 0:
            info = self.client.margin_fee(vipLevel=0, coin="TUSD")
            commision_per_min = float(info[0]['dailyInterest'])/1440
            loan_amount = round(((int(time.time() - self.loan_time) * commision_per_min) + self.tusd), 1)
            print(self.client.margin_repay(asset='TUSD', amount=loan_amount, symbol='BTCTUSD', isIsolated=True))
            self.tusd = 0
        elif self.btc > 0:
            info = self.client.margin_fee(vipLevel=0, coin="BTC")
            commision_per_min = float(info[0]['dailyInterest'])/1440
            loan_amount = round(((int(time.time() - self.loan_time) * commision_per_min) + self.btc), 6)
            print(self.client.margin_repay(asset='BTC', amount=loan_amount, symbol='BTCTUSD', isIsolated=True))
            self.btc = 0


            