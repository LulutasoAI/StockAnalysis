import os
from matplotlib import pyplot as plt
import pandas_datareader.data as data
from Baseutils import Baseutils
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import math

Util = Baseutils()
prices = Util.stksearch2p("TSLA",Util.start,Util.end)
df = Util.stksearch("TSLA",Util.start, Util.end)

class LRshift10():
    def __init__(self):
        self.utility = Baseutils()
        self.prices = Util.stksearch2p("TSLA",self.utility.start,self.utility.end)
        self.df = Util.stksearch("TSLA",self.utility.start,self.utility.end)
        print("latest data", self.df.iloc[-1:,0:0])
        self.n = 10
        self.scalar_ = StandardScaler()

    def shifting(self):
        df = self.df.copy()
        n = self.n
        for t in range(1,n):
            if t == 1:
                a = df["Adj Close"].shift(+t).to_frame()
                a.columns = ["t_{}".format(t)]
                print(type(a))
                newone = pd.concat([df,a],axis = 1)
            else:
                a = df["Adj Close"].shift(+t).to_frame()
                a.columns = ["t_{}".format(t)]
                newone = pd.concat([newone,a],axis = 1)
        #add ans
        a = df["Adj Close"].shift(-1).to_frame()
        a.columns = ["next day"]
        newone = pd.concat([newone,a],axis = 1)
        return newone


    def dataprocessing_(self):
        newone = self.shifting()
        self.today = newone.iloc[-1:,:].drop(["next day"],axis=1).values
        newone = newone.dropna()
        X = newone.drop(["next day"], axis=1)
        Y = newone[["next day"]]
        X = self.scalar_.fit_transform(X)
        self.today = self.scalar_.transform(self.today)
        tr_size = int(0.7*len(X))
        X_train = X[0:tr_size]
        X_test= X[tr_size:len(X)]
        Y_train = Y.values[0:tr_size]
        Y_test= Y.values[tr_size:len(X)]
        std_reg = LinearRegression()
        return X_train, X_test, Y_train, Y_test

    def learning(self):
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
        model = self.learning()
        result = (round(float(model.predict(self.today)),2))
        print(result)
        return result

if __name__ == "__main__":
    LR = LRshift10()
    result = LR.estimation_dataprocessing_tomorrow()
    #def estimation(self, x):
