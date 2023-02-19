from datetime import datetime
from blockCountries import blockCountryList

def minOfGame(isPlaying,isBreak : bool,  startPeriod :datetime, startGame :datetime):
    '''
    :param startPeriod: время начала периода
    :param startGame: время начала игры
    :return: minOfGame - минута игры, isBreak - перерыв
    '''
    minGame = -999999
    dPeriodGameTime = startPeriod - startGame  #разница между началом тайма(перерыва) и началом игры
    minPeriod  = int((datetime.now() - startPeriod).total_seconds() // 60) #минута тайма
    if not isPlaying: # игра окончена
        minGame=-1
    elif isBreak:
        minGame =45
    elif dPeriodGameTime.total_seconds() < 1800: #в первом тайме
        minGame=minPeriod
    elif (dPeriodGameTime.total_seconds() > 3300): #во втором тайме
        minGame=(45+minPeriod)
    #if isPlaying:
    #    print(isPlaying, isBreak, startGame, startPeriod , dPeriodGameTime.total_seconds())
    #if minGame==-999999:
    #    print(isPlaying, isBreak, startPeriod, startGame,  dPeriodGameTime.total_seconds())
    #    print(minGame,isBreak)
    return minGame


def isCorrectGame(game: dict) -> bool:
    '''
    :param game: словарь, заполненный данными матча
    :return: True, если матч удовлетворяет фильтрам по времени, голам
    '''
    def getGoalFilter(game:dict) ->bool:
        if (type(game['score1']) == str) and (type(game['score2']) == str):
            return  (game['score1'] == '0') and (game['score2'] == '0')
        else:
            return  False
    def getTimeFilter(game:dict) ->bool:
        minGame = minOfGame(game['isplaying'], game['isbreak'], game['startperiod'], game['startdate'])
        return  (minGame > 30) and (minGame < 60)


    countryFilter = not (game['country'].lower() in blockCountryList)
    gameIsPlaying = game['isplaying']
    timeFilter    = getTimeFilter(game)
    goalFilter    = getGoalFilter(game)
    #
    if gameIsPlaying and timeFilter and goalFilter and countryFilter:
        return True
    else:
        return False


def gameToStr(game : dict) -> str:
    def minOrBreak(isPlaying,isBreak : bool, startPeriod:datetime, startGame : datetime) -> str:
        minGame = minOfGame(isPlaying,isBreak,startPeriod, startGame)
        if isBreak:
            minStr='Перерыв'
        else:
            minStr = '{}\' мин'.format(minGame)
        return minStr
    return '{} {}. {}. {} {} - {} {}'.format(game['startdate'].strftime('%H:%M'),game['startperiod'].strftime('%H:%M'),
                                                  minOrBreak(game['isplaying'],game['isbreak'], game['startperiod'],game['startdate']),
                                                  game['team1'],game['score1'], game['score2'], game['team2'])


def addNewCountry(game : dict):
    outlist=[]
    outlist.append('*{}*'.format(game['country']))
    outlist.append('*{}*'.format(game['tourney']))
    outlist.append(gameToStr(game))
    return  outlist

def addNewTourney(game : dict):
    outlist=[]
    outlist.append('*{}*'.format(game['tourney']))
    outlist.append(gameToStr(game))
    return  outlist

def addGame(game : dict):
    outlist=[]
    outlist.append(gameToStr(game))
    return  outlist