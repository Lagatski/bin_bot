#!/usr/bin/env python

class Analys:

    def __init__(self):
        self.kline_data = []
        self.vol_kline = []
        self.flat = None
        self.tp = None
        self.sl = None
        self.iteration = -1

    """Методы для сохранений параметров свечи"""    

    def set(self, new_kline):
        self.iteration += 1
        self.kline_data.append(new_kline)
        self.vol_kline.append(float(new_kline[5]))
        if len(self.vol_kline) > 5:
            self.vol_kline.pop(0)

        if sum(self.vol_kline)/5 < 200:
            self.flat = 1.1
            self.tp = 5
            self.sl = 2.5
        else:
            self.flat = 2
            self.tp = 5
            self.sl = 4

    def set_history_data(self, klines_data):
        i = 0
        while i < len(klines_data)-1:
            self.iteration += 1
            self.kline_data.append(klines_data[i])
            self.vol_kline.append(float(klines_data[i][5]))
            if len(self.vol_kline) > 5:
                self.vol_kline.pop(0)
            if sum(self.vol_kline)/5 < 200:
                self.flat = 1.1
                self.tp = 5
                self.sl = 2.5
            else:
                self.flat = 2
                self.tp = 8
                self.sl = 4
            i += 1

    
    def get_last_kline(self):
        return self.kline_data[self.iteration]

    def get_last_time(self):
        return self.kline_data[self.iteration][0]

    def get_flat(self):
        return self.flat
    
    def get_tp(self):
        return self.tp
    
    def get_sl(self):
        return self.sl

    """Методы для анализа рынка"""
    
    def falling_flat(self):
        kline_size = float(self.kline_data[self.iteration][1]) - float(self.kline_data[self.iteration][4])
        if -1*self.flat <= kline_size <= 0:
            return True
        else:
            return False
    
    def upping_flat(self):
        kline_size = float(self.kline_data[self.iteration][1]) - float(self.kline_data[self.iteration][4])
        if 0.01 <= kline_size <= self.flat:
            return True
        else:
            return False

    def is_flat(self):
        kline_size = float(self.kline_data[self.iteration][1]) - float(self.kline_data[self.iteration][4])
        if 0 <= abs(kline_size) <= self.flat:
            return True
        else:
            return False
    
    def down_trend_3m(self):
        size_change = float(self.kline_data[self.iteration][4]) - float(self.kline_data[self.iteration-3][1])
        if size_change >= 0 or abs(size_change) < self.tp:
            return False
        return True
    
    def down_trend_5m(self):
        size_change = float(self.kline_data[self.iteration][4]) - float(self.kline_data[self.iteration-5][1])
        if size_change >= 0 or abs(size_change) < self.tp*2:
            return False
        return True

    def up_trend_3m(self):
        size_change = float(self.kline_data[self.iteration][4]) - float(self.kline_data[self.iteration-3][1])
        if size_change < 0 or size_change < self.tp:
            return False 
        return True

    def up_trend_5m(self):
        size_change = float(self.kline_data[self.iteration][4]) - float(self.kline_data[self.iteration-5][1])
        if size_change < 0 or size_change < self.tp*2:
            return False
        return True

    def approved_price(self, deal_direction: str, new_kline):
        if deal_direction == 'UP' or deal_direction == 'DOWN':
            if float(new_kline[4]) >= float(self.kline_data[self.iteration][4]) + 0.33 * self.flat:
                return False
            elif float(new_kline[4]) <= float(self.kline_data[self.iteration][4]) - 0.33 * self.flat:
                return False
            return True
        return False
        

