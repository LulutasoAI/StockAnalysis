import pandas as pd
import numpy as np
import pandas_datareader as dt
import datetime
from matplotlib import pyplot as plt
from Baseutils import Baseutils

class MA(Baseutils):
    def __init__(self):
        #for MA
        super().__init__()
        self.periods = [20,144,200]

    def MA(self, data, period):
        """This creates the MA data based on the set period like 14 100 144 200 and so on"""
        ma = []
        for i, dat in enumerate(data):
            if i > period:
                m = np.mean(data[i-period:i])
                ma.append(m)
            else:
                ma.append(0)
        #plt.plot(data)
        #plt.plot(ma)
        #plt.show()
        return ma

    def mashandler(self,mas, prices,rang):
        colors = ["green", "yellow", "red"]
        for i,a in enumerate(mas):
            plt.plot(a[-rang:],color = colors[i])
        plt.plot(prices[-rang:],color = "black")
        plt.title("green = MA20, yellow = 144, red = 200")
        plt.show()

    def MAmain(self, stkname):
        """It arranges MA prediction making process.
        This one is outdated, do not use it.
        """
        data = self.stksearch(stkname, self.start, self.end)
        prices = self.df2price(data)
        mas = []
        colors = ["green", "yellow", "red"]
        for i, period in enumerate(self.periods):
            ma = self.MA(prices, period)
            mas.append(ma)
            plt.plot(ma,color = colors[i])
        plt.plot(prices,color = "black")
        plt.title(stkname)
        plt.show()
        self.mashandler(mas,prices,20)
        return mas

    def MAprediction(self, data):
        prices = data[-400:]
        mas = []
        colors = ["green", "yellow", "red"]
        for i, period in enumerate(self.periods):
            ma = self.MA(prices, period)
            mas.append(ma)
        self.mashandler(mas,prices,199)
        p = 0
        for a in range(0,3):
            #print(mas[a], "this is _ {}".format(a))
            if mas[a][-1] - mas[a][-199] >= 0:
                if a == 0:
                    print("20 is positive")
                elif a == 1:
                    print("144 is positive")
                elif a == 2:
                    print("200 is positive")
                p += 1
        if p == 3:#The higher p is, the more MAs were upwards
            return 1
        elif p == 2:
            return 0
        else:
            return -1
