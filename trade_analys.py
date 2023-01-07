#!/usr/bin/env python

class Parameters:

    def __init__(self):
        self.vol_kline=[]
        self.flat=None
        self.tp=None
        self.sl=None

    def set(self, kline_info):

        self.vol_kline.append(float(kline_info[5]))
        if (len(self.vol_kline) > 5):
            self.vol_kline.pop(0)

        if (sum(self.vol_kline)/5 < 200):
            self.flat = 1.1
            self.tp = 5
            self.sl = 2.5
        else:
            self.flat = 2
            self.tp = 5
            self.sl = 4

    def get_flat(self):
        return self.flat
    
    def get_tp(self):
        return self.tp
    
    def get_sl(self):
        return self.sl
    