from bet import Bet
from betXML import BetXML

sumStat = {
    'Win'     : 0,
    'Loose'   : 0,
    'Cash'    : 0,
    'Place'   : 0,
    'BetList' : []
}

tourneyStats = {
    'Name'    : '',
    'Stats'   : sumStat
}

countryStats ={
    'Name'    : '',
    'Tourney' : [], #список из словарей tourneyStats
    'Stats'   : sumStat
}

class BetStats :
    def __init__(self):
        self.countryList=[] #список стран
        self.betXML=BetXML()
        for bet in self.betXML.betList:
            self.__addBet(bet)
        self.__sortListByName()
        self.__calcPlaces()
        self.print()
    def __tourneyIndex(self, country , tourneyName: str):
        tourneyIndex=-1
        index=0
        if len(country['Tourney'])>0:
            for tourney in country['Tourney'] :
                if tourney['Name']==tourneyName :
                    tourneyIndex=index
                index+=1
        return tourneyIndex

    def __addToCountryStats(self,bet: Bet):
        countryIndex = self._сountryIndex(bet.country)
        if countryIndex==-1:
            country=dict(Name=bet.country, Stats=dict(Win=0, Loose=0, Cash=0, Place=0, BetList=[]), Tourney=[])
            self.countryList.append(country)
        else:
            country=self.countryList[countryIndex]

        country['Stats']['Win']   +=int(float(bet.cash) > 0)
        country['Stats']['Loose'] +=int(float(bet.cash) <= 0)
        country['Stats']['Cash']  += float(bet.cash)
        country['Stats']['BetList'].append(bet.cash)
        tourneyIndex=self.__tourneyIndex(country,bet.tourney)
        if tourneyIndex==-1:
            newTourney=dict(Name=bet.tourney, Stats=dict(Win=int(float(bet.cash) > 0), Loose=int(float(bet.cash) <= 0), Cash=float(bet.cash), Place=0, BetList=[bet.cash]))
            country['Tourney'].append(newTourney)
        else:
            country['Tourney'][tourneyIndex]['Stats']['Win']+=int(float(bet.cash) > 0)
            country['Tourney'][tourneyIndex]['Stats']['Loose'] += int(float(bet.cash) <= 0)
            country['Tourney'][tourneyIndex]['Stats']['Cash'] += float(bet.cash)
            country['Tourney'][tourneyIndex]['Stats']['BetList'].append(bet.cash)

    def __sortListByName(self):
        self.countryList.sort(key=lambda countryList: countryList['Name'])  #
        for tekCountry in self.countryList:
            mytourneyList = tekCountry['Tourney']
            mytourneyList.sort(key=lambda mytourneyList: mytourneyList['Name'])
            #print(mytourneyList)

    def __addBet(self,bet : Bet):
        self.__addToCountryStats(bet)

    def __calcPlaces(self):
        def getTourneyFromName(countryName,tourneyName):
            for tekCountry in self.countryList:
                if tekCountry['Name'].lower()==countryName.lower():
                    for tekTourney in tekCountry['Tourney']:
                        if tekTourney['Name'].lower()==tourneyName.lower():
                            return tekTourney

        self.countryList.sort(key=lambda countryList: countryList['Stats']['Cash'])
        self.tourneyList=[]
        self.countryList.reverse()
        index = 1
        for tekCountry in self.countryList:
            for tekTourney in tekCountry['Tourney']:
                self.tourneyList.append(dict(Country=tekCountry['Name'], Name=tekTourney['Name'], Cash=tekTourney['Stats']['Cash']))
            tekCountry['Stats']['Place']=index
            index+=1
        print(self.tourneyList[0])
        #ttttouurney=getTourneyFromName(self.tourneyList[0]['Country'],self.tourneyList[0]['Name'])
        #ttttouurney['Stats']['Place']=self.tourneyList[0]['Place']
        self.tourneyList.sort(key=lambda tourneyList: tourneyList['Cash'])
        self.tourneyList.reverse()
        index=1
        for tekTourney in self.tourneyList:
            #print(tekTourney)
            findTourney=getTourneyFromName(tekTourney['Country'],tekTourney['Name'])
            findTourney['Stats']['Place']=index
            index+=1



    def _сountryIndex(self, countryName: str):
        countryIndex = -1
        index = 0
        for country in self.countryList:
            if countryName.lower() in country['Name'].lower():
                countryIndex = index
                return countryIndex
            index += 1
        return countryIndex

    def print(self):
        #self.__calcPlaces()
        print('*')
        print('tourney count = ',len(self.tourneyList))
        # tourney in self.tourneyList:
        #    print(tourney)
        for tekCountry in self.countryList:
            print('')
            for key,value in tekCountry.items():
                print('{} = {}'.format(key,value))

