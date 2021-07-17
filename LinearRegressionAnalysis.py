#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np
import xlrd
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn import datasets
import calendar
import json
import datetime
from pandas_datareader import data

class LRANALYSIS():
    def __init__(self,start_date,symbols):
        self.start_date = start_date
        self.symbols = symbols
        self.axx = len(symbols)
        self.axy = len(start_date)
        self.fig, self.axs = plt.subplots(self.axx,self.axy)
        #self.fig.show()

    def graphgen(self,start_date, symbol,m,n):

        today = datetime.date.today()
        end_date = "{}".format(today)
        df = data.DataReader(symbol, "yahoo", start_date, end_date)
        print(df.reset_index(level=0, inplace=True)) #it worked!
        df["Date"]
        date = df["Date"]
        price = df["Adj Close"]
        X = date
        y = price
        X = X.rename_axis("Date")
        print(X,"before adjustment")
        Xaxis = X
        y = y.rename_axis("Price")
        X = X.values.astype("datetime64[D]").astype(int)
        print(X,"after the adjustment")
        X = pd.Series(X)
        type(y)
        type(X)
        X = X.values.reshape(-1,1)
        Y = y.values.reshape(-1,1)
        lm = linear_model.LinearRegression()
        model = lm.fit(X,y)
        predictions = lm.predict(X)
        print(predictions)
        lm.score(X,y)
        lm.coef_
        lm.intercept_
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, y)
        Y_pred = linear_regressor.predict(X)
        Y_pred
        """"plt.plot(X, Y_pred, y, color="red", )
        plt.show()"""
        #plt.plot(Xaxis,y)
        #plt.plot(Xaxis, Y_pred, color="red")
    #    plt.title(symbol)

        self.axs[m,n].plot(Xaxis,y)
        self.axs[m,n].plot(Xaxis,Y_pred,color="red")
        self.axs[m,n].set_title(symbol)

    def main(self):
        #self.fig, self.axss = plt.subplots(self.axx,self.axy)
        for m, sdate in enumerate(self.start_date):
            for n, sname in enumerate(self.symbols):
                self.graphgen(sdate,sname,n-1,m-1)
        plt.show()



if __name__ == "__main__":

    start_date = ["1980-01-01","2001-01-01","2010-01-01"]
    symbols = ["NEE","ENPH","SEDG","FSLR","TSLA"]
    LR = LRANALYSIS(start_date, symbols)
    LR.main()
    LR.fig.show()
