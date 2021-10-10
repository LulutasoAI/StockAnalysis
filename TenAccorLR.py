import os
from matplotlib import pyplot as plt
import pandas_datareader.data as data
#os.chdir(r"D:\githubby\StockAnalysis")
from Baseutils import Baseutils
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import math
import numpy as np
from datetime import datetime, date, timedelta

Util = Baseutils()
prices = Util.stksearch2p("TSLA",Util.start,Util.end)
df = Util.stksearch("TSLA",Util.start, Util.end)

class LRshift_N():
    def __init__(self, name): #perfect I guess except for self.scalar2, what is that.
        self.name = name
        self.utility = Baseutils()
        self.prices = Util.stksearch2p(self.name,self.utility.start,self.utility.end)
        self.df = Util.stksearch(self.name,self.utility.start,self.utility.end)
        print("latest data", self.df.iloc[-1:,0:0])
        self.n = 10
        self.scalar_ = StandardScaler()
        self.scalar2 = StandardScaler()
        self.lags = 75 #200 for NIkkei, 75 for tesla. Notsure.

    def acorr_Close(self): 
        df = self.df
        newone = self.shifting(df,self.lags)
        newone = newone.drop(["High","Low","Open","Close","Volume"],axis = 1)
        today = newone.iloc[-1:,:].drop(["next day"],axis=1).values #Today's price. Generally useful.
        print(today,"today after generated")
        newone = newone.dropna()
        X_train, X_test, Y_train, Y_test, today = self.dataprocessing2(newone,today)
        model = self.learning2(X_train, X_test, Y_train, Y_test)
        predicted = model.predict(today)
        return model, today, predicted

    def shifting(self,df,n):
        """
        input data and lag to make a shifted data.
        """
        for t in range(1,n):
            if t == 1:
                a = df["Adj Close"].shift(+t).to_frame()
                a.columns = ["t_{}".format(t)]
                newone = pd.concat([df,a],axis = 1)
            else:
                a = df["Adj Close"].shift(+t).to_frame()
                a.columns = ["t_{}".format(t)]
                newone = pd.concat([newone,a],axis = 1)
        a = df["Adj Close"].shift(-1).to_frame()
        a.columns = ["next day"]
        newone = pd.concat([newone,a],axis = 1)
        print(newone, "shifting result")
        return newone

    def learning2(self,X_train, X_test, Y_train, Y_test):
        model= LinearRegression()
        model.fit(X_train,Y_train)
        r2_train = model.score(X_train,Y_train)
        print(r2_train,"trainscore")
        r2_test = model.score(X_test,Y_test)
        print(r2_test,"testscore")
        return model

    def dataprocessing2(self,newone,today): #what is the difference between Dataprocessing _ and 2?
        X = newone.drop(["next day"], axis=1)
        Y = newone[["next day"]]
        tr_size = int(0.7*len(X))
        X_train = X[0:tr_size]
        X_test= X[tr_size:len(X)]
        Y_train = Y.values[0:tr_size]
        Y_test= Y.values[tr_size:len(X)]
        return X_train, X_test, Y_train, Y_test, today

    def dataprocessing_(self):
        #used in the estimating process.
        newone = self.shifting(self.df,self.n)
        today = newone.iloc[-1:,:].drop(["next day"],axis=1).values
        newone = newone.dropna()
        X = newone.drop(["next day"], axis=1)
        Y = newone[["next day"]]
        X = self.scalar_.fit_transform(X)
        self.today = self.scalar_.transform(today)
        tr_size = int(0.7*len(X))
        X_train = X[0:tr_size]
        X_test= X[tr_size:len(X)]
        Y_train = Y.values[0:tr_size]
        Y_test= Y.values[tr_size:len(X)]
        std_reg = LinearRegression()
        return X_train, X_test, Y_train, Y_test

    def learning(self):
        #used in the estimating process.
        #This process has nothing to do with the self correlation analysis.
        X_train, X_test, Y_train, Y_test = self.dataprocessing_()
        model= LinearRegression()
        model.fit(X_train,Y_train)
        r2_train = model.score(X_train,Y_train)
        print(r2_train,"trainscore")
        r2_test = model.score(X_test,Y_test)
        print(r2_test,"testscore")
        return model
        #Y_predict = std_reg.predict(X_test)
    
    def estimation_dataprocessing_tomorrow(self):
        #This process has nothing to do with the self correlation analysis except for sharing the same data? I guess.
        #Therefore, This includes the learning process.
        model = self.learning()
        result = (round(float(model.predict(self.today)),2))
        print(result)
        return result

    def dataupdate(self,today,predicted):
        temp_list = list(today[0])
        temp_list = temp_list[1:]
        temp_list.insert(0,predicted)
        output = np.array(temp_list).reshape(1,len(temp_list))
        return output

    def visual_future_prediction(self):
        model, today, predicted = self.acorr_Close()
        outputplot = list(self.prices)[-100:]
        outputplot = list(reversed(outputplot))
        date_today = datetime.today()
        Y = []
        daysback = 1
        for i, a in enumerate(outputplot):
            daysback -= 1
            fixedday = date_today - timedelta(days=-daysback)
            A = fixedday.strftime("%A")
            while A == "Sunday" or A == "Saturday":
                daysback -= 1
                fixedday = date_today - timedelta(days=-daysback)
                A = fixedday.strftime("%A")
            Y.append(fixedday)
        outputplot = list(reversed(outputplot))
        Y = list(reversed(Y))
        daysback = 0
        for i in range(0,self.lags):
            daysback += 1
            if i == 0:
                new = self.dataupdate(today,predicted)
                predicted = model.predict(new)
            else:
                new = self.dataupdate(new,predicted)
                predicted = model.predict(new)
            outputplot.append(predicted)
            fixedday = date_today + timedelta(days=daysback)
            A = fixedday.strftime("%A")
            while A == "Sunday" or A == "Saturday":
                daysback += 1
                fixedday = date_today + timedelta(days=daysback)
                A = fixedday.strftime("%A")
            Y.append(fixedday)
        plt.plot(Y[:-self.lags],outputplot[:-self.lags],color="b")
        plt.plot(Y[-self.lags:],np.array(outputplot[-self.lags:]).reshape(-1,),color="r")
        plt.title("Future {} stock prices ".format(self.name))
        plt.tight_layout()
        plt.show()


    def main(self):
        result = self.estimation_dataprocessing_tomorrow()
        print("tomorrow's predicted price value of {}".format(self.name),result)
        self.visual_future_prediction()

if __name__ == "__main__":
    LR = LRshift_N("TSLA")
    result = LR.estimation_dataprocessing_tomorrow()
    print("tomorrow's predicted price value of {}".format(LR.name),result)
    LR.visual_future_prediction()
