import sys 
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', 'util'))

class Game:
    def __init__(self, round, outcome, points, cities, events, error):
        self.round = str(round)
        self.outcome = outcome
        self.points = str(points) 
        self.cities = cities
        self.events = events
        self.error = error

    def getCityNamesAsList(self):
        cityNames = []
        for city in self.cities:
            cityNames.append(city.name)
        return cityNames

    def getCityByName(self, name):
        for city in self.cities:
            if name == city.name:
                return city
        return None

    def getAllPathogenNames(self):
        from gameIO import loadJsonFile
        pathogens = loadJsonFile(os.path.join(FILE, '..', '..', 'resources', 'pathogens.json'))
        return [v for v in pathogens.values()]

    def getGlobalEventByType(self, type):
        # returns an event that can be occur one time, e.g. economicCrisis
        for event in self.events:
            if event.type == type:
                return event
        return None

    def getGlobalEventsByType(self, type):
        # returns list of events that can be occur multiple times, e.g. medicationInDevelopment
        globalEvents = []
        for event in self.events:
            if event.type == type:
                globalEvents.append(event)
        return globalEvents

    def isOver(self):
        return self.outcome != "pending"
        
    def isPathogenEncounteredByName(self, pathogenName):
        return self.isGlobalAttributeAvailableForPathogenByPathogenName("pathogenEncountered", pathogenName)

    def isVaccineAvailableByPathogenName(self, pathogenName):
        return self.isGlobalAttributeAvailableForPathogenByPathogenName("vaccineAvailable", pathogenName)

    def isMedicationAvailableByPathogenName(self, pathogenName):
        return self.isGlobalAttributeAvailableForPathogenByPathogenName("medicationAvailable", pathogenName)
    
    def isGlobalAttributeAvailableForPathogenByPathogenName(self, globalAttribute, pathogenName):
        pathogenEncounteredEvents = self.getGlobalEventsByType(globalAttribute)
        for pathogenEncounteredEvent in pathogenEncounteredEvents:
            if pathogenEncounteredEvent.pathogen.name == pathogenName:
                return True        
        return False

    def getOverallPopulation(self):
        overallPopulation = 0
        for city in self.cities:
            overallPopulation = overallPopulation + int(city.population)
        return overallPopulation
        
    def getPopulationsAsListOfFloats(self):
        populations = []
        for city in self.cities:
            populations.append(float(city.population))
        return populations

    def normalizePopulationForCity(self, city):
        populations = self.getPopulationsAsListOfFloats()
        
        return round(((float(city.population) - min(populations)) / (max(populations) - min(populations))
                * (1000 - 1)) + 1)

    def getOverallInfected(self):
        overallInfected = 0
        for city in self.cities:
            population = int(city.population)
            cityPrevalence = 0 
            for event in city.events:
                if event.type == 'outbreak':
                    cityPrevalence = cityPrevalence + float(event.prevalence)
            overallInfected = overallInfected + cityPrevalence * population
        return overallInfected