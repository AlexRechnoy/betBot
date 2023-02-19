import requests
import json
from datetime import datetime
from flashScoreFuncs import addNewCountry, addNewTourney, addGame, isCorrectGame

def fsParse():
    '''
    Возввращает список матчей, данные которых упакованы в словари.
    Ключи словаря :
        country - страна
        tourney - турнир
        startdate  - дата и время начала матча
        startperid - время начала тайма
        team1  - команда 1
        team2  - команда 2
        score1 - кол-во голов, забитых командой 1
        score2 - кол-во голов, забитых командой 2
    '''
    feed='f_1_0_3_ru-kz_1'
    url=f'https://d.flashscorekz.com/x/feed/{feed}'
    r = requests.get(url=url, headers={"x-fsign":"SW9D1eZo"})
    data=r.text.split('¬')

    data_list=[{}]
    for item in data:
        key   = item.split('÷')[0]
        value = item.split('÷')[-1]
        if '~' in key :
            data_list.append({key:value})
        else:
            data_list[-1].update({key:value})

    match_list=[]
    for element in data_list:
        if "ZA" in list(element.keys())[0]: #страны
            country=element["~ZA"].split(':')[0]
            tourney = element["~ZA"].split(':')[-1]
        if "AA" in list(element.keys())[0]: #матчи
            startDate =datetime.fromtimestamp(int(element["AD"]))
            team1 =element["AE"]
            team2 =element["AF"]
            score1=element.get("AG")
            score2=element.get("AH")
            isPlaying = (element.get("AI")!=None)
            isBreak   = (isPlaying and element.get("BX")=='-1')
            #dtime= datetime.now()-startDate
            #if (dtime.total_seconds()>0) and (dtime.total_seconds()<3500):
                #min=int(dtime.total_seconds()//60)
                #sec=int(dtime.total_seconds()%60)
                #print(country, tourney, startDate, min,sec , team1, score1, score2,  team2)
                #print(json.dumps(element, ensure_ascii=False, indent=2))
            #print(json.dumps(element, ensure_ascii=False, indent=2))
            startperiod=datetime(2000,1,1,1,1,1)
            if "AO" in element:
                startperiod=datetime.fromtimestamp(int(element["AO"]))
                #print(startperiod)
            match_list.append({'country': country, 'tourney': tourney, 'startdate': startDate, 'startperiod': startperiod,
                               'team1': team1, 'score1': score1,'team2': team2,'score2': score2, 'isbreak': isBreak, 'isplaying': isPlaying})
    return match_list

def getFsData():
    '''
    :return: Список матчей, которые удовлетворяют условиям отбора
    '''
    fsRawData = fsParse() #cписок всех матчей
    gamesDayCount=len(fsRawData)
    filter_data = []
    for game in fsRawData:
        if isCorrectGame(game):
            filter_data.append(game)
    return filter_data,gamesDayCount

def fsDataToStr():
    '''
    :return: Приводим данные к текстовому сообщению
    '''
    gamesData,gamesDayCount = getFsData()
    myoutlist = ['*Всего матчей за сегодня : {} *'.format(gamesDayCount)]
    myoutlist.append('*Матчей онлайн : {}*'.format(len(gamesData)))
    countryList=[]
    for index in range(len(gamesData)):
        if index == 0:
            dataList = addNewCountry(gamesData[index])
            countryList.append(gamesData[index]['country'])
        else:
            if gamesData[index - 1]['country'] != gamesData[index]['country']:  # изменилась страна
                dataList = addNewCountry(gamesData[index])
                countryList.append(gamesData[index]['country'])
            elif gamesData[index - 1]['tourney'] != gamesData[index]['tourney']:
                dataList = addNewTourney(gamesData[index])
            else:
                dataList = addGame(gamesData[index])
        for str in dataList:
            myoutlist.append(str)
    str = ''
    for tekstr in myoutlist:
        print(tekstr)
        str += '\n' + tekstr
    return str,countryList, len(gamesData)