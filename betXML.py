import xml.etree.ElementTree as xml
import xml.etree.cElementTree as ET
from bet import Bet

xml_file='data/T1M_BetDay.xml'

class BetXML:
    def __init__(self):
        tree = ET.ElementTree(file=xml_file)
        root = tree.getroot()
        self.betList =[]
        for betDay in root:
            if betDay.tag=='Дата':
                year =betDay.attrib.get('Год')
                month = betDay.attrib.get('Месяц')
                day = betDay.attrib.get('День')
                for betNode in betDay:
                    country = betNode.attrib.get('Страна')
                    tourney = betNode.attrib.get('Турнир')
                    res     = betNode.attrib.get('Результат')
                    self.betList.append(Bet(country ,tourney ,res ,year ,month ,day))
        print('Bet count (from XML) = ' ,len(self.betList))
