from bet import Bet

class BetFullStats:
    def __init__(self):
        self.win=0
        self.firstDate=''
        self.lastDate=''
        self.loose=0
        self.cash=0
        self.countryCount=0
        self.tourneyCount=0
        self.betCount=0
        self.__firstBet=True

    def setTourneyCount(self,tourneyCount):
        self.tourneyCount=tourneyCount

    def setCountryCount(self, countryCount):
        self.tourneyCount = countryCount

    def processBet (self,bet:Bet):
        if self.__firstBet:
            self.firstDate=bet.date
            self.__firstBet=False
        self.betCount+=1
        self.win   += int(float(bet.cash) > 0)
        self.loose += int(float(bet.cash) <= 0)
        self.cash  += float(bet.cash)
        self.lastDate=bet.date