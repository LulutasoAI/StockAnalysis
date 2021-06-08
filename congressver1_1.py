class StockAnalysisCongress():
    # https://www.ig.com/jp/trading-strategies/10-trading-indicators-every-trader-should-know-201105
    #0 = up,1 = neutral ,2 = down
    #necessary range = 200
    def __init__(self):
        #for MA
        self.periods = [20,144,200]
        self.start = datetime.datetime(2001,1,1)
        self.end = datetime.datetime.today()

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
        prices = self.df2price(data)
        prices = prices[-400:]
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
            return 0
        elif p == 2:
            return 1
        else:
            return 2


if __name__ == "__main__":
    cong = StockAnalysisCongress()
    a = cong.MAmain("NEE")
