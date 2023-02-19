import time

import requests
from _1xstavka_funcs import getTourneyGames,tourneyFilter
from datetime import datetime

def _1xstavkaParse():
    def proccessTourney(champID):
        params = {
            'sports': '1',
            'champs': champID,
            'count': '50',
            'antisports': '188',
            'mode': '4',
            'country': '1',
            'partner': '51',
            'getEmpty': 'true',
            'noFilterBlockEvent': 'true',
        }
        response = requests.get('https://1xstavka.ru/LiveFeed/Get1x2_VZip', params=params)
        result = response.json()
        return getTourneyGames(result)


    def getTourneys():
        '''Возвращает словарь {ID : название турнира} '''
        params = {
            'sport': '1',
            'country': '1',
            'partner': '51',
            'virtualSports': 'true',
            'groupChamps': 'true',
        }
        response = requests.get('https://1xstavka.ru/LiveFeed/GetChampsZip', params=params)
        result = response.json()

        champList={}
        for champ in result['Value']:
            if "SC" in champ.keys():
                for subchamp in champ["SC"]:
                    champList[int(subchamp["LI"])]=subchamp["L"]
            else:
                champList[int(champ["LI"])]=champ["L"]
        return champList
    ####################################################################################################################
    ####################################################################################################################
    ################################################  Основной код !!!!  ###############################################
    ####################################################################################################################
    ####################################################################################################################
    tourneyList = getTourneys()
    tourneyListFilter={key: val for key, val in tourneyList.items() if tourneyFilter(str(val).lower())}
    print(f'Всего турниров : {len(tourneyListFilter)}')

    index=0
    gamesData=[] #cписок ,cостоящий из списков словарей (которые описывают статистику турниров)
    start_time = time.time()
    for tourneyID in tourneyListFilter.keys():
        #print(f'{index}) champID = {tourneyID} name = "{tourneyListFilter[tourneyID]}"')
        gamesData.append(proccessTourney(tourneyID))
        #if index>10 :
        #    break
        index+=1
    print('Запросы (1xstavka) за : {:2.4f} c.'.format(time.time() - start_time))

    countryDict={} # ключ - название страны, значение - словарь из турниров и списков игр
    # {страна1 : {турнир1 : [cписок игр], турнир2 : [список игр] ...},
    #  страна2 : {турнир1 : [cписок игр], турнир2 : [список игр] ...}  }
    gameCount=0
    for gamesCountry in gamesData :
        for game in gamesCountry:
            countryName=game["country"]
            tourneyName=game["tourney"]
            gameCount+=1
            if countryName in countryDict:
                if tourneyName in  countryDict[countryName]:
                    countryDict[countryName][tourneyName] += [game]
                else:
                    countryDict[countryName][tourneyName] = [game]
            else:
                countryDict[countryName]={tourneyName:[game]}

    #распечатать
    #for county in countryDict :
    #    print(f'{county} : ')
    #    for tourney in countryDict[county]:
    #        print(f'  {tourney}')
    #        for game in countryDict[county][tourney]:
    #            print(f'    {game}')
    return countryDict,gameCount

def _1xstavkaDataToStr():
    def gameToStr(game : dict):
        koefStr='ТМ:'
        for key in game["koef"]:
            str=f'{key}={game["koef"][key]}, '
            #print(str)
            koefStr+=str
        koefStr=koefStr[:-2]
        if game["gamePeriod"]=='Перерыв':
            timeStr=''
        else:
            timeStr=f'{game["gameTime"]}мин . '
        return  f'  {game["gamePeriod"]}. {timeStr}{game["homeTeam"]} {game["homeGoals"]} - {game["awayGoals"]} {game["awayTeam"]}.\n *{koefStr}*'


    countryDict,gameCount=_1xstavkaParse()
    outstrlist=[f'*Всего матчей онлайн : {gameCount}*']
    countrylist=[]
    for county in countryDict :
        countrylist.append(county)
        outstrlist.append('')
        outstrlist.append(f'*{county.upper()}*')
        for tourney in countryDict[county]:
            outstrlist.append(f'*{tourney}*')
            for game in countryDict[county][tourney]:
                outstrlist.append(gameToStr(game))
    str=''
    for tekstr in outstrlist:
        str += '\n' + tekstr
    return str,countrylist,gameCount

#'country': country, 'tourney':tourney,'homeTeam':homeTeam,'homeGoals':homegoals,
#'awayTeam':awayTeam, 'awayGoals': awaygoals, 'gamePeriod':gamePeriod,'gameTime':gameTimeMin, 'koef':TMkoef}



