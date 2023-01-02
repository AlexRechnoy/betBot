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
        self.yearList=[]

    def setTourneyCount(self,tourneyCount):
        self.tourneyCount=tourneyCount

    def setCountryCount(self, countryCount):
        self.countryCount = countryCount

    def processBet (self,bet:Bet):
        if self.__firstBet:
            self.firstDate=bet.date
            self.__firstBet=False
        self.betCount+=1
        self.win   += int(float(bet.cash) > 0)
        self.loose += int(float(bet.cash) <= 0)
        self.cash  += float(bet.cash)
        self.winpercent=self.win/self.betCount*100
        self.lastDate=bet.date
        newYearDict = {'year': bet.date.year, 'win': int(float(bet.cash) > 0), 'loose': int(float(bet.cash) <= 0),
                       'cash': float(bet.cash)}
        if len(self.yearList)==0:

            self.yearList.append(newYearDict)
        else:
            addDict=True
            index=0
            for tekyear in self.yearList:
                if tekyear['year']==bet.date.year:
                    addDict=False
                    break
                index+=1
            if addDict:
                self.yearList.append(newYearDict)
            else:
                self.yearList[index]['win'] += int(float(bet.cash) > 0)
                self.yearList[index]['loose'] += int(float(bet.cash) <= 0)
                self.yearList[index]['cash'] += float(bet.cash)
