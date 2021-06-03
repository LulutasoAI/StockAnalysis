from MA import MA
from Baseutils import Baseutils

def main():
    Ma = MA()
    BaseU = Baseutils()
    start = BaseU.start
    end = BaseU.end
    stocknames = BaseU.usefulStocks
    prices = BaseU.stksearch2p("PLUG",start,end)
    print(prices)
    pass









if __name__ == '__main__':
    main()
