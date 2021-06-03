import pandas as pd
import numpy as np
import pandas_datareader as dt
import datetime
from matplotlib import pyplot as plt

class Baseutils():
    """
    bunch of utills how apparent.
    """
    def __init__(self):
        self.start = datetime.datetime(2001,1,1)
        self.end = datetime.datetime.today()
        self.usefulStocks = ["TSLA","NEE", "GM", "SEDG","ENPH", "FSLR","NIO"]

    def stksearch2p(self,stk_name,start, end):
        df = dt.DataReader(stk_name,"yahoo", start, end)
        prices = df["Close"]
        return np.array(prices)
