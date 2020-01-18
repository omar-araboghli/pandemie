import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'game'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))

from Game import Game
from City import City
from Event import Event
from Pathogen import Pathogen
from gameIO import loadGameFromFile

class TestEvent(unittest.TestCase):

    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game = loadGameFromFile(path)
    city = game.getCityByName('Atlanta')

    def testInit(self):
        self.assertEqual(type(self.city), City, 'Should be a City')
        self.assertEqual(self.city.name, 'Atlanta', 'Should be Atlanta')

    def testGetLocalEventByType(self):
        self.assertEqual(type(self.city.getLocalEventByType('outbreak')), Event, 'Should be an Event')
        self.assertEqual(self.city.getLocalEventByType('outbreak').type, 'outbreak', 'Should be outbreak')
        self.assertEqual(type(self.city.getLocalEventByType('outbreak').pathogen), Pathogen, 'Should be Pathogen')
        self.assertEqual(self.city.getLocalEventByType('outbreak').pathogen.name, 'Procrastinalgia', 'Should be Procrastinalgia')

        self.city = self.game.getCityByName('Banjul')
        self.assertEqual(self.city.getLocalEventByType('outbreak'), None, 'Should be None')
        
if __name__ == '__main__':
    unittest.main()