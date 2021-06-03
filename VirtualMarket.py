class VirtualMarket(Baseutils):
    def __init__(self):
        super().__init__()
        pass

    def experiencereplay(self, stkname):
        #Integrate here.
        data = self.stksearch(stk_name,start, end)
        prices = df2price(data)
        prediction, index = self.datathrower(prices)
        pass
    def experiencereplay2(self, stkname, model):
        #Integrate here.
        data = self.stksearch(stk_name,start, end)
        prices = df2price(data)
        predictioin, index = model(prices)
        return prediction,index, prices


    def datathrower(self, prices,model):
        """
        It takes the past data not necessarily the longer the better but the data should be long enough.
        Then for loop begins with the input data, and add the each data to the 'situation' list until the size
        of the list hits 400.
        After the process, the situation is now 400 successive price data. The process makes it a input for
        the prediction making model. Model is freely selected as you please as an argument as long as the model
        is made in accordance with the specific rules we have to follow. This function finally outputs the prediction and
        corresponding Index. Index can be used to validate answeres(predictions). The process will use Price, Index and predictions.

        """
        situation = []
        predictions = []
        index = []

        for i, a in enumerate(prices):
            if i <= 401:
                situation.append(a)
            else:
                situation.append(a)
                del situation[-1]
                predictions.append(model(situation))
                index.append(i)
        return predictions, index


    def validationdatamakerpattern1(self, data):
        """Answers will come one month later. """
        temporaldata = []
        inputdata = []
        answers = []
        for i, a in enumerate(data):
            temporaldata.append(a)
            if len(temporaldata) == 400:
                try:
                    answers.append(data[i+30])
                    inputdata.append(temporaldata)
                    temporaldata = []
                except:
                    temporaldata = []
        return inputdata, answers
    def validationAdatamaker(self, data, model,pattern):
        """
        Answers will come one month later.
        After the process of making predictions this will check the prediction accuracy.

        """
        profit = 0
        inputdata, answers = pattern(data)
        for i, a in enumerate(inputdata):
            pred = model(a)
            current_price = a[-1]
            if pred == 0:
                temp_prof = answers[i] - current_price
                print("I thought this Stock would go up and this resulted in {} as profit ".format(temp_prof))

            elif pred == 1:
                temp_prof = 0
                print("I am neutral about this.")
            elif pred == 2:
                temp_prof = current_price - answers[i]
                print("I thought this Stock would go down and this resulted in {} as profit ".format(temp_prof))
            else:
                print("something is wrong with prediction sectore but I think it is unlikely for this message to show up")
            profit += temp_prof
            print("the current profit = {}".format(profit))

        return profit
