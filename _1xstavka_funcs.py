import requests

def getTM(homeTeam ,awayTeam ,gameData):
    '''Возвращает словарь из параметров игры, если игра удовлетворяет условия по времени и голам,
       иначе возвращает пустой словарь
    '''
    game = gameData["Value"]["GE"]
    homegoals ,awaygoals ,gamePeriod ,gameTimeMin =0 ,0 ,'?????' ,0
    country = gameData["Value"]["CN"]
    tourney = gameData["Value"]["L"]
    if "S1" in gameData["Value"]["SC"]["FS"]:
        homegoals= gameData["Value"]["SC"]["FS"]["S1"]
    if "S2" in gameData["Value"]["SC"]["FS"]:
        awaygoals= gameData["Value"]["SC"]["FS"]["S2"]
    if "CPS" in gameData["Value"]["SC"]:
        gamePeriod =gameData["Value"]["SC"]["CPS"]
    if "TS" in gameData["Value"]["SC"]:
        gameTimeMin =gameData["Value"]["SC"]["TS"]//60
    TMkoef ={ }
    for stats in game:
        if stats["G"]==4 :
            for stat in (stats["E"][1]):
                if stat["P"]< 2.5:
                    TMkoef[stat["P"]]= stat["C"]
                    # print(f'    ТМ{stat["P"]} = {stat["C"]}')
    if (homegoals==0 ) and (awaygoals==0 ) and (gameTimeMin>30) and (gameTimeMin<60):
    #if homegoals<10:
        gameDict= { 'country': country, 'tourney':tourney,'homeTeam':homeTeam,'homeGoals':homegoals,
                    'awayTeam':awayTeam, 'awayGoals': awaygoals, 'gamePeriod':gamePeriod,'gameTime':gameTimeMin, 'koef':TMkoef}
    else:
        gameDict={}
    return gameDict

def getTourneyGames(tourneyData):
    '''Возвращает список словарей из параметров игр, относящихся к данному турниру'''
    gamesData=[]
    gameIndex=0
    for game in tourneyData['Value']:
        gameIndex+=1
        ok=all(map(game.__contains__,('O1','O2')))    # ('O1' in game.keys()) and ('O2' in game.keys())
        if not ok :
            print(f'  {gameIndex}) Некорректная игра !!!')
            continue
        homeTeam=game['O1']
        if 'голы' in homeTeam:
            print(f'  {gameIndex}) Некорректное название команды!!!')
            continue
        awayTeam = game['O2']
        gameID   = game['I']
        params = {
            'id': gameID,
            'lng': 'ru',
            'cfview': '0',
            'isSubGames': 'true',
            'GroupEvents': 'true',
            'allEventsGroupSubGames': 'true',
            'countevents': '250',
            'partner': '51',
            'grMode': '2',
            'marketType': '1',
            'isNewBuilder': 'true',
        }
        response = requests.get('https://1xstavka.ru/LiveFeed/GetGameZip', params=params)
        gameDict=getTM(homeTeam,awayTeam,response.json())
        if len(gameDict)>0 :
            if 'альтернатив' not in gameDict['tourney'].lower():
                print(gameDict)
                gamesData.append(gameDict)
    return gamesData

def tourneyFilter(name : str):
    filerlist=['женщ','2x2','3x3','4x4','5x5','7x7','indoor','short','испан','австр','итал','швейцар','уругв','азер',
               'швец','косово','португа','исланд', 'дани','англ','франц','бельг','нидерл','израил','португал',
               'гватемал','росси',
               'товарищеские','шотл','финлян','турци','казах','герман','дуэль','уефа','альтер','league']
    for filterElem in filerlist :
        if filterElem.lower() in name.lower():
            return False
    return True