class CityMapper:

    cityMap = dict()

    def __init__(self, cities):
        self.cityMap = self.mapCities(cities)

    def getCityUsingId(self, id):
        return self.cityMap[id]

    def getIdUsingCity(self, city):
        listResult = [i for i in self.cityMap.keys() if self.cityMap[i] == city]
        return listResult[0]

    def mapCities(self, cities):
        map = dict(zip(range(len(cities)), cities))
        return map

