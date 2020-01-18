import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'converters'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'game'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))
from GameConverter import Converter
from Pathogen import Pathogen
from Event import Event
from City import City
from Game import Game
from gameIO import loadJsonFile

class TestGameConverter(unittest.TestCase):

    converter = Converter()
    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game_dict = loadJsonFile(path)
    city_dict = game_dict['cities']['Abuja']
    event_dict = game_dict['events'][0]
    pathogen_dict = event_dict['pathogen']

    def testConvertPathogen(self):
        self.assertEqual(type(self.converter.convertPathogen(self.pathogen_dict)), Pathogen, "Should be a Pathogen")
        self.assertEqual(self.converter.convertPathogen(self.pathogen_dict).name, 'Procrastinalgia', "Should be Procrastinalgia")

    def testConvertEvent(self):
        self.assertEqual(type(self.converter.convertEvent(self.event_dict)), Event, 'Should be an Event')
        self.assertEqual(self.converter.convertEvent(self.event_dict).type, 'pathogenEncountered', 'Should be pathogenEncountered')

    def testConvertCity(self):
        self.assertEqual(type(self.converter.convertCity(self.city_dict)), City, 'Should be an City')
        self.assertEqual(self.converter.convertCity(self.city_dict).name, 'Abuja', 'Should be Abuja')
        self.assertEqual(type(self.converter.convertCity(self.city_dict).connections), list, 'Should be a list')
        self.assertEqual(len(self.converter.convertCity(self.city_dict).connections), 5, 'Should be 5')

    def testConvertGame(self):
        self.assertEqual(type(self.converter.convertGame(self.game_dict)), Game, 'Should be a Game')
        self.assertEqual(type(self.converter.convertGame(self.game_dict).cities), list, 'Should be a list')
        self.assertEqual(type(self.converter.convertGame(self.game_dict).cities[0]), City, 'Should be a City')
        self.assertEqual(type(self.converter.convertGame(self.game_dict).events), list, 'Should be a list')
        self.assertEqual(type(self.converter.convertGame(self.game_dict).events[0]), Event, 'Should be an Event')
    
    def testConvertToNumber(self):
        self.assertEqual(type(self.converter.convertToNumber('--')), float, 'Should be float')
        self.assertEqual(self.converter.convertToNumber('--'), 4.0, 'Should be 4.0')
        with self.assertRaises(ValueError): self.converter.convertToNumber('hello')

if __name__ == '__main__':
    unittest.main()