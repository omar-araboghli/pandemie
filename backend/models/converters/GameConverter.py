import sys 
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'game'))

class Converter:
    def convertPathogen(self, pathogen_object):
        from Pathogen import Pathogen
        name = pathogen_object['name'] if 'name' in pathogen_object else ''
        infectivity = pathogen_object['infectivity'] if 'infectivity' in pathogen_object else ''
        mobility = pathogen_object['mobility'] if 'mobility' in pathogen_object else ''
        duration = pathogen_object['duration'] if 'duration' in pathogen_object else ''
        lethality = pathogen_object['lethality'] if 'lethality' in pathogen_object else ''
        
        return Pathogen(name, infectivity, mobility, duration, lethality)
    
    def convertEvent(self, event_object):
        from Event import Event
        type = event_object['type'] if 'type' in event_object else ''
        city = event_object['city'] if 'city' in event_object else ''
        round = event_object['round'] if 'round' in event_object else ''
        sinceRound = event_object['sinceRound'] if 'sinceRound' in event_object else ''
        untilRound = event_object['untilRound'] if 'untilRound' in event_object else ''
        participants = event_object['participants'] if 'participants' in event_object else ''
        prevalence = event_object['prevalence'] if 'prevalence' in event_object else ''
        pathogen = event_object['pathogen'] if 'pathogen' in event_object else ''
        pathogen = self.convertPathogen(pathogen)

        return Event(type, city, round, sinceRound, untilRound, participants, prevalence, pathogen)

    def convertCity(self, city_object):
        from City import City
        name = city_object['name'] if 'name' in city_object else ''
        latitude = city_object['latitude'] if 'latitude' in city_object else ''
        longitude = city_object['longitude'] if 'longitude' in city_object else ''
        population = city_object['population'] if 'population' in city_object else ''
        connections = city_object['connections'] if 'connections' in city_object else ''
        economy = self.convertToNumber(city_object['economy']) if 'economy' in city_object else ''
        government = self.convertToNumber(city_object['government']) if 'government' in city_object else ''
        hygiene = self.convertToNumber(city_object['hygiene']) if 'hygiene' in city_object else ''
        awareness = self.convertToNumber(city_object['awareness']) if 'awareness' in city_object else ''
        events = []
        if 'events' in city_object:
            for event in city_object['events']:
                events.append(self.convertEvent(event))

        return City(name, latitude, longitude, population, connections, economy,
                    government, hygiene, awareness, events)
        
    def convertGame(self, game_object):
        from Game import Game
        round = game_object['round'] if 'round' in game_object else ''
        outcome = game_object['outcome'] if 'outcome' in game_object else ''
        points = game_object['points'] if 'points' in game_object else ''
        error = game_object['error'] if 'error' in game_object else ''
        cities = []
        events = []

        if 'cities' in game_object:
            for city in game_object['cities']:
                cities.append(self.convertCity(game_object['cities'][city]))
        
        if 'events' in game_object:
            for event in game_object['events']:
                events.append(self.convertEvent(event))

        return Game(round, outcome, points, cities, events, error) 

    def convertToNumber(self, string):
        number = 0
        if string == '++':
            number = 0.0
        elif string == '+':
            number = 1.0
        elif string == 'o':
            number = 2.0
        elif string == '-':
            number = 3.0
        elif string == '--':
            number = 4.0
        else:
            raise ValueError('Only these values are allowed ["--", "-", "o", "+", "++"]')
        return number