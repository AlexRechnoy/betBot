from bet import Bet
from betXML import BetXML
from betFullStats import BetFullStats
from blockCountries import blockCountryList

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
        self.betXML=BetXML() #список ставок из XML
        #self.blockCountries=blockCountryList # список стран, игры которых не будут отображаться а онлайн
        #print(self.blockCountries)
        self.betFullStats=BetFullStats() #статистика по ставкам
        for bet in self.betXML.betList:
            self.__addBet(bet)
            self.betFullStats.processBet(bet)
        self.__sortListByName()
        self.__calcPlaces()
        #self.print()
        self.betFullStats.setTourneyCount(len(self.tourneyList))
        self.betFullStats.setCountryCount(len(self.countryList))
        #print('Всего={} В={} П={} %={:.2f}'.format(self.betFullStats.betCount,self.betFullStats.win,self.betFullStats.loose,self.betFullStats.winpercent))
        #print(self.betFullStats.firstDate)
        #print(self.betFullStats.lastDate)

    def __tourneyIndex(self, country , tourneyName: str):
        tourneyIndex=-1
        index=0
        if len(country['Tourney'])>0:
            for tourney in country['Tourney'] :
                if tourney['Name']==tourneyName :
                    tourneyIndex=index
                index+=1
        return tourneyIndex

    def __addToStats(self,bet: Bet):
        countryIndex = self.__getСountryIndexMatch(bet.country)
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
        """
        Функция добавления ставки к статистике
        :param bet:
        :return:
        """
        self.__addToStats(bet)

    def __calcPlaces(self):
        """
        -упорядочивание списка countryList по выигрышу
        -создание списка tourneyList (отдельный список турниров) и упорядочивание его по выигрышу
        :return:
        """
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
                self.tourneyList.append(dict(Country=tekCountry['Name'], Tourney=tekTourney))
            tekCountry['Stats']['Place']=index
            index+=1
        self.tourneyList.sort(key=lambda tourneyList: tourneyList['Tourney']['Stats']['Cash'])
        self.tourneyList.reverse()
        index=1
        for tekTourney in self.tourneyList:
            findTourney=getTourneyFromName(tekTourney['Country'],tekTourney['Tourney']['Name'])
            findTourney['Stats']['Place']=index
            index+=1


    def __getСountryIndexMatch(self, countryName: str):
        '''Поиск по полному названию, если такую страну нашли, то возвращаем ее индекс в списке self.countryList'''
        countryIndex,index = -1,0
        for country in self.countryList:
            if countryName.lower() == country['Name'].lower():
                countryIndex = index
                break
            index+=1
        return countryIndex


    def _getCountryIndex(self, countryName: str):
        '''Сначала ищем полное совпадение, потом частичное'''
        if countryName.lower()=='южная африка':
            countryName='юар'
        countryIndex=self.__getСountryIndexMatch(countryName)
        if countryIndex!=-1:
            return countryIndex
        index = 0
        for country in self.countryList:
            if countryName.lower() in country['Name'].lower():
                countryIndex = index
                return countryIndex
            index += 1
        return countryIndex

    def print(self):
        #self.__calcPlaces()
        pass
        #print('tourney count = ',len(self.tourneyList))
        # tourney in self.tourneyList:
        #    print(tourney)
        #for tekCountry in self.countryList:
        #    print('')
        #    for key,value in tekCountry.items():
        #        print('{} = {}'.format(key,value))

