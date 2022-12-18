from betStats import BetStats

class BetData (BetStats):
    def __getStatStr(self,stats):
        Place = stats['Place']
        Cash = stats['Cash']
        Win = stats['Win']
        Loose = stats['Loose']
        Last = stats['BetList'][-5:]
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
        countryIndex=self._сountryIndex(countryName)
        strList = []
        print('countryIndex = ',countryIndex)
        if countryIndex==-1:
            return '*Такая страна не найдена !!!*'
        country=self.countryList[countryIndex]
        print('country = ', country)
        strList.append('*'+country['Name']+'*')
        Cash,Win,Loose,Last,Percent, Place=self.__getStatStr(country['Stats'])
        strList.append('_Выигр ={:.2f} Место={} из {}_'.format(Cash,Place,len(self.countryList)))
        strList.append('_В={} П={} %={:.2f} Послед.={}_'.format(Win, Loose, Percent, Last))
        #
        tourneyList=country['Tourney']
        tourneyList.sort(key=lambda tourneyList: tourneyList['Stats']['Cash'])
        tourneyList.reverse()
        strList.append('*Турниры : *')
        for tourney in tourneyList:
            Cash, Win, Loose, Last, Percent, Place = self.__getStatStr(tourney['Stats'])
            strList.append('*{}* Выигр ={:.2f} Место={} из {}'.format(tourney['Name'],Cash, Place, len(self.tourneyList)))
            strList.append('В={} П={} %={:.2f} Послед.={}'.format(Win, Loose, Percent,Last))

        str=''
        for tekstr in strList :
            str+='\n'+tekstr
        return str

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
