import datetime

month_str_to_int = {
    'Янв': 1,
    'Фев': 2,
    'Март': 3,
    'Апр': 4,
    'Май':5,
    'Июнь': 6,
    'Июль': 7,
    'Авг': 8,
    'Сент': 9,
    'Окт': 10,
    'Нояб': 11,
    'Дек': 12,
}

class Bet:
    def __init__(self,country,tourney,cash : float,year,month,day):
        self.country = country
        self.tourney = tourney
        self.cash = cash
        try:
            month_int = month_str_to_int[month]
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))
        self.date = datetime.date(int(year), month_int, int(day))

