from betStats import BetStats
from flashScoreParse import fsDataToStr

maxSymbolsInMessage = 4000

class BotData(BetStats):
    def __init__(self):
        super().__init__()
        self.onlineCountryList=[] #списко стран, в которых играются матчи в данный момент

    def __getStatStr(self,stats,lastCount=5):
        Place = stats['Place']
        Cash = stats['Cash']
        Win = stats['Win']
        Loose = stats['Loose']
        Last = stats['BetList'][-lastCount:]
        Last.reverse()
        Percent = Win / (Win + Loose) * 100
        return Cash, Win, Loose, Last, Percent, Place

    def __getFullStatStr(self,statDict : dict, elementName : str, index : int, countryName : str=''):
        def getTopStatStr(stats):
            Cash = stats['Cash']
            Win = stats['Win']
            Loose = stats['Loose']
            Percent = Win / (Win + Loose) * 100
            return Cash, Win, Loose, Percent
        Cash, Win, Loose, Percent = getTopStatStr(statDict)
        if countryName=='':
            strFormat = '{}) {}. Выигр ={:.2f} Всего={} В={} П={} %={:.2f}'
            str = '\n' + (strFormat.format(index, elementName, Cash, Win + Loose, Win, Loose, Percent))
        else:
            strFormat = '{}) {}.{} '+'\n'+' Выигр ={:.2f} Всего={} В={} П={} %={:.2f}'
            str = '\n' + (strFormat.format(index, countryName,elementName, Cash, Win + Loose, Win, Loose, Percent))

        return str

    def getCountryStats(self, countryName : str):
        """
        Функция, возвращающяя статистику страны и ее турниров
        :param countryName: название страны, для которой будет осуществлен поиск статистики
        :return:возвращает список строк, который содержит в себе статистику страны countryName и всех турниров, относящихся к ней
        """
        def valToIcons(valList : list):
            iconStr=''
            for val in valList :
                if float(val)>0:
                    iconStr+='\U00002705'
                else:
                    iconStr+='\U0000274C'
            return iconStr
        countryIndex=self._сountryIndex(countryName)
        strList = []
        if countryIndex==-1:
            return '*"{}" - такая страна не найдена !!!*'.format(countryName)
        #страна
        country=self.countryList[countryIndex]
        strList.append('*'+country['Name']+'*')
        Cash, Win, Loose, Last, Percent, Place=self.__getStatStr(country['Stats'],15)
        strList.append('_Выигр ={:.2f} Место={} из {}_'.format(Cash,Place,len(self.countryList)))
        strList.append('_В={} П={}  %={:.2f} {} _'.format(Win, Loose, Percent, valToIcons(Last)))
        #турниры
        tourneyList=country['Tourney']
        tourneyList.sort(key=lambda tourneyList: tourneyList['Stats']['Cash'])
        tourneyList.reverse()
        strList.append('*Турниры : *')
        for tourney in tourneyList:
            Cash, Win, Loose, Last, Percent, Place = self.__getStatStr(tourney['Stats'])
            strList.append('*{}* Выигр ={:.2f} Место={} из {}'.format(tourney['Name'],Cash, Place, len(self.tourneyList)))
            strList.append('В={} П={} %={:.2f} {}'.format(Win, Loose, Percent,valToIcons(Last)))
        str=''
        for tekstr in strList :
            if len(str+'\n'+tekstr)<maxSymbolsInMessage:
                str+='\n'+tekstr
        return str

    def getStats(self):
        strList,str=[],''
        dayCount = (self.betFullStats.lastDate - self.betFullStats.firstDate).days
        strList.append('*Выигрыш* : {:.2f} тыс. руб.'.format(self.betFullStats.cash))
        strList.append('*Выигрыш за месяц*: {:.0f} руб.'.format(self.betFullStats.cash*1000/dayCount*30))
        strList.append('*Выигрыш за 1 cтавку*  : {:.2f} руб.'.format(self.betFullStats.cash * 1000 / self.betFullStats.betCount))
        strList.append('*Выигрыши по годам* : ')
        for yearStat in self.betFullStats.yearList:
            strList.append(' *{}* {:.2f}тыс. р., {}, {:.2f}%'.format(yearStat['year'],yearStat['cash'],yearStat['win']+yearStat['loose'],
                                                             yearStat['win']/(yearStat['win']+yearStat['loose'])*100))
        strList.append('*Всего ставок* : {}'.format(self.betFullStats.betCount))
        strList.append('*Всего стран/турнир.* : {}/{}'.format(self.betFullStats.countryCount,self.betFullStats.tourneyCount))
        strList.append('*Выигрыши/поражения* : {}/{}'.format(self.betFullStats.win,self.betFullStats.loose))
        strList.append('*Процент побед* : {:.2f}%'.format(self.betFullStats.winpercent))
        strList.append('*Первая ставка* : {}'.format(self.betFullStats.firstDate))
        strList.append('*Последняя ставка* : {}'.format(self.betFullStats.lastDate))
        strList.append('*Кол-во дней* : {}'.format(dayCount))
        for tekstr in strList:
            str += '\n' + tekstr
        return str

    def getOnlineGames(self):
        commandTxt,self.onlineCountryList,onlineGameCount = fsDataToStr()
        return commandTxt,onlineGameCount

    def getOnlineStats(self):
        strList=[]
        #commandTxt, self.onlineCountryList, onlineGameCount = fsDataToStr()
        for country in self.onlineCountryList:
            strList.append(self.getCountryStats(country.lower()))
        return strList

    def getTopCountries(self, topCount):
        """
        Функция возвращает лучшие страны
        :param topCount: кол-во стран
        :return: строка, содержащяя статистику стран
        """
        toplist = self.countryList[0:topCount]
        index, str = 1, ''
        for country in toplist:
            str+=self.__getFullStatStr(country['Stats'],country['Name'],index)
            index += 1
        return str

    def getTopTourneys(self,topCount):
        toplist = self.tourneyList[0:topCount]
        index, str = 1, ''
        for tourney in toplist:
            s=self.__getFullStatStr(tourney['Tourney']['Stats'], tourney['Tourney']['Name'], index,tourney['Country'])
            str += s
            index += 1
        return str

botData=BotData()
