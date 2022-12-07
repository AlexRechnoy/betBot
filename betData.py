from ipaddress import _count_righthand_zero_bits

from betStats import BetStats

class BetData (BetStats):

    def getCountryStats(self, countryName : str):
        def getStatStr(stats):
            Cash = stats['Cash']
            Win = stats['Win']
            Loose = stats['Loose']
            Last = stats['BetList'][-5:]
            Last.reverse()
            Percent = Win / (Win + Loose) * 100
            return Cash,Win,Loose,Last,Percent
        countryIndex=self._сountryIndex(countryName)
        strList = []
        print('countryIndex = ',countryIndex)
        if countryIndex==-1:
            return '*Такая страна не найдена !!!*'
        country=self.countryList[countryIndex]
        strList.append('*'+country['Name']+'*')
        Cash,Win,Loose,Last,Percent=getStatStr(country['Stats'])
        strList.append('_Выигр ={:.2f} В={} П={} %={:.2f} Послед.={}_'.format(Cash,Win,Loose,Percent,Last))
        #
        tourneyList=country['Tourney']
        tourneyList.sort(key=lambda tourneyList: tourneyList['Stats']['Cash'])
        tourneyList.reverse()
        strList.append('*Турниры : *')
        for tourney in tourneyList:
            Cash, Win, Loose, Last, Percent = getStatStr(tourney['Stats'])
            strList.append('*{}* Выигр ={:.2f} В={} П={} %={:.2f} Послед.={}'.format(tourney['Name'],Cash, Win, Loose, Percent, Last))

        str=''
        for tekstr in strList :
            str+='\n'+tekstr
        return str