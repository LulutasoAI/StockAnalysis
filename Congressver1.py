import pandas as pd
import numpy as np
import pandas_datareader as dt
import datetime
from matplotlib import pyplot as plt


class StockAnalysisCongress():
    def __init__(self):
        #for MA
        self.periods = [20,144,200]
        self.start = datetime.datetime(2001,1,1)
        self.end = datetime.datetime.today()
        self.colors = ["green", "yellow", "red"]

    def stksearch(self,stk_name,start, end):
        df = dt.DataReader(stk_name,"yahoo", start, end)
        return df

    def df2price(self, data):
        prices = data["Close"]
        return np.array(prices)

    def MA(self, data, period):
        ma = []
        for i, dat in enumerate(data):
            if i > period:
                m = np.mean(data[i-period:i])
                ma.append(m)
            else:
                ma.append(0)
        return ma

    def mashandler(self,mas, prices,rang):
        for i,a in enumerate(mas):
            plt.plot(a[-rang:],color = self.colors[i])
        plt.plot(prices[-rang:],color = "black")
        plt.title("green = MA20, yellow = 144, red = 200")
        plt.show()
    def MAmain(self,stkname):
        data = self.stksearch(stkname, self.start, self.end)
        prices = self.df2price(data)

        mas = []
        for i, period in enumerate(self.periods):
            ma = self.MA(prices, period)
            mas.append(ma)
            plt.plot(ma,color = self.colors[i])
        plt.plot(prices,color = "black")
        plt.title(stkname)
        plt.show()
        self.mashandler(mas,prices,20)
        return mas
if __name__ == "__main__":
    cong = StockAnalysisCongress()
    a = cong.MAmain("NEE")
