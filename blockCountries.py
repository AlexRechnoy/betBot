from pathlib import Path
filePath='data/blockCountries.txt'

def getBlockCountries():
    print('!!!!!!!!!')
    countryList=[]
    file =Path(filePath)
    if file.exists():
        f = open(filePath ,mode='r', encoding="utf-8")
        lines =f.read().split('\n')
        for line in lines:
            countryList.append(line.lower())
        f.close()
    return countryList


blockCountryList = getBlockCountries()