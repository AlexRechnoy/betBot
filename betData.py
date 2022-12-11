from betStats import BetStats

class BetData (BetStats):

    def getCountryStats(self, countryName : str):
        def getStatStr(stats):
            Place = stats['Place']
            Cash = stats['Cash']
            Win = stats['Win']
            Loose = stats['Loose']
            Last = stats['BetList'][-5:]
            Last.reverse()
            Percent = Win / (Win + Loose) * 100
            return Cash,Win,Loose,Last,Percent,Place
        countryIndex=self._сountryIndex(countryName)
        strList = []
        print('countryIndex = ',countryIndex)
        if countryIndex==-1:
            return '*Такая страна не найдена !!!*'
        country=self.countryList[countryIndex]
        print('country = ', country)
        strList.append('*'+country['Name']+'*')
        Cash,Win,Loose,Last,Percent, Place=getStatStr(country['Stats'])
        strList.append('_Выигр ={:.2f} Место={} из {}_'.format(Cash,Place,len(self.countryList)))
        strList.append('_В={} П={} %={:.2f} Послед.={}_'.format(Win, Loose, Percent, Last))
        #
        tourneyList=country['Tourney']
        tourneyList.sort(key=lambda tourneyList: tourneyList['Stats']['Cash'])
        tourneyList.reverse()
        strList.append('*Турниры : *')
        for tourney in tourneyList:
            Cash, Win, Loose, Last, Percent, Place = getStatStr(tourney['Stats'])
            strList.append('*{}* Выигр ={:.2f} Место={} из {}'.format(tourney['Name'],Cash, Place, len(self.tourneyList)))
            strList.append('В={} П={} %={:.2f} Послед.={}'.format(Win, Loose, Percent,Last))

        str=''
        for tekstr in strList :
            str+='\n'+tekstr
        return str