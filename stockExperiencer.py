import numpy as np
import pandas as pd
import pandas_datareader.data as web
import random

n225 = web.DataReader("NIKKEI225", "fred")

"""
1128 I have to make it simple because I still suck in thinking about complicated
algorithm or so on. You can hold only one stock or something at a certain price that
what I can do most at the moment
"""
class Reinforcement_AI():
    def __init__(self,data):
        self.data = data #data, it might be the big dataset or something
        self.hold = 0  #the price when you bought something
        self.current_price #the current_price of the moment the AI is training or something
        self.position = False #whether or not The Ai is holding the position
        self.holding_positions = []  """this function is currently disabled since this makes the
        whole system overly complicated. I can implement this later for sure can't I"""
        self.profit = 0
        self.project_path = r"C:\Users\hinet\Documents\MarketAI project"
        return
    def Act_buy(self,c_price):
        if self.position == True:
            pass
        self.hold = c_price - 7""" #spread is always there init, and this prevents AI to
        overly trade things which is pretty stupid in real life anyway"""
        self.position = True
        return
    def Act_sell(self, c_price):
        if self.position == False:
            pass
        benefit = self.hold - self.current_price
        self.profit += benefit
        return benefit
    def create_agent(self):
        AnAgent = AgentX()
        return AnAgent
    def record(self):
        """those three probabilities do not add up to more than 100, rather, it has to
        add up to sharp 100 because maths is OP you  know"""
        Agent_sight = []
        sightATT = [] #sight At That Time apparently
        C_prices = []
        Actions = []
        Benefits = []
        AnAgent = self.create_agent()
        BT= AnAgent.buying_tendency
        ST= AnAgent.selling_tendency
        HT = 100 - BT - ST #holding_tendency
        for i, cp in enumerate(self.data):
            self.current_price = cp
            C_prices.append(self.current_price)
            if i < 40: #AI observes 40 sequences of price moving
                Agent_sight.append(cp)
            else:
                rd = random.randint(0,100)
                if 0 <= rd < BT:
                    self.Act_buy()
                    Benefits.append(0)
                    Actions.append("Buy")
                    del Agent_sight[0]
                    Agent_sight.append(self.current_price)
                    sightATT.append(Agent_sight)
                elif BT <= rd < ST:
                    benefit = self.Act_sell()
                    Benefits.append(benefit)
                    Actions.append("Sell")
                    del Agent_sight[0]
                    Agent_sight.append(self.current_price)
                    sightATT.append(Agent_sight)
                else:
                    Actions.append("Hold")
                    Benefits.append(0)
                    del Agent_sight[0]
                    Agent_sight.append(self.current_price)
                    sightATT.append(Agent_sight)
                    pass
        self.output_result(sightATT,C_prices, Actions, Benefits, BT,ST,HT)





    def output_result(self,sightATT, C_prices, Actions, Benefits,BT,ST,HT):
        pre_df = []
        pre_df.append(sightATT)
        pre_df.append(C_prices)
        pre_df.append(Actions)
        pre_df.append(Benefits)
        df = pd.DataFrame(pre_df).T
        df.columns = columns
        columns = ["SightATT", "C_prices", "Actions", "Benefits"]
        df.to_csv(self.project_path,"results.csv")

        #something out put csv or something thank you
        pass

class AgentX():
    """this fucntion creates an agent randomly for the exploring behaviour and
     the result record for future trading for everyone"""
    def __init__(self):
        self.buying_tendency = random.randint(1,30)
        self.selling_tendency = random.randint(1,30)
        self.holding_tendency = 100 - buying_tendency - selling_tendency
        return
        #AgentX.buying_tendency outputs the tendency which can be used for sure
