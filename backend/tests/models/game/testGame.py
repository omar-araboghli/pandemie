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

class TestGame(unittest.TestCase):

    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game = loadGameFromFile(path)

    def testInit(self):
        self.assertEqual(type(self.game), Game, 'Should be a Game')
        self.assertEqual(self.game.outcome, 'pending', 'Should be pending')                   

    def testGetCityNamesAsList(self):
        self.assertEqual(type(self.game.getCityNamesAsList()), list, 'Should be a list')
        self.assertEqual(len(self.game.getCityNamesAsList()), 260, 'Should be 260')
        self.assertEqual(self.game.getCityNamesAsList()[0], 'Abuja', 'Should be Abuja')

    def testGetCityByName(self):
        self.assertEqual(type(self.game.getCityByName('Abuja')), City, 'Should be a City')
        self.assertEqual(self.game.getCityByName('Abuja').name, 'Abuja', 'Should be a Abuja')
        self.assertEqual(self.game.getCityByName('Hello'), None, 'Should be None')

    def testGetAllPathogenNames(self):
        self.assertEqual(type(self.game.getAllPathogenNames()), list, 'Should be a list')
        self.assertEqual(len(self.game.getAllPathogenNames()), 19, 'Should be 19')
        self.assertEqual(self.game.getAllPathogenNames()[0], 'Procrastinalgia', 'Should be Procrastinalgia')

    def testGetGlobalEventByType(self):
        self.assertEqual(type(self.game.getGlobalEventByType('pathogenEncountered')), Event, 'Should be an Event')
        self.assertEqual(self.game.getGlobalEventByType('pathogenEncountered').type, 'pathogenEncountered', 'Should be a pathogenEncountered')
        self.assertEqual(self.game.getGlobalEventByType('hello'), None, 'Should be None')

    def testIsOver(self):
        self.assertFalse(self.game.isOver(), 'Should be False')
        self.game.outcome = 'win'
        self.assertTrue(self.game.isOver(), 'Should be True')
        self.game.outcome = 'pending'

    def testIsPathogenEncounteredByName(self):
        self.assertFalse(self.game.isPathogenEncounteredByName('Plorps'), 'Should be False')
        self.assertTrue(self.game.isPathogenEncounteredByName('Procrastinalgia'), 'Should be True')

    def testIsVaccineAvailableByPathogenName(self):
        self.assertFalse(self.game.isVaccineAvailableByPathogenName('Plorps'), 'Should be False')

        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        vaccineAvailableEvent = Event(type='vaccineAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)

        self.game.events.append(vaccineAvailableEvent)        
        self.assertTrue(self.game.isVaccineAvailableByPathogenName('Procrastinalgia'), 'Should be True')

    def testIsMedicationAvailableByPathogenName(self):
        self.assertFalse(self.game.isMedicationAvailableByPathogenName('Plorps'), 'Should be False')

        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        medicationAvailableEvent = Event(type='medicationAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)

        self.game.events.append(medicationAvailableEvent)        
        self.assertTrue(self.game.isMedicationAvailableByPathogenName('Procrastinalgia'), 'Should be True')

    def testIsGlobalAttributeAvailableForPathogenByPathogenName(self):
        self.assertFalse(self.game.isGlobalAttributeAvailableForPathogenByPathogenName('medicationAvailable', 'Procrastinalgia'), 'Should be False')

        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        medicationAvailableEvent = Event(type='medicationAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)

        self.game.events.append(medicationAvailableEvent)        
        self.assertTrue(self.game.isGlobalAttributeAvailableForPathogenByPathogenName('medicationAvailable', 'Procrastinalgia'), 'Should be True')

    def testGetPopulationsAsListOfFloats(self):
        self.assertEqual(type(self.game.getPopulationsAsListOfFloats()), list, 'Should be a list')
        self.assertEqual(len(self.game.getPopulationsAsListOfFloats()), 260, 'Should be 260')
        self.assertEqual(type(self.game.getPopulationsAsListOfFloats()[0]), float, 'Should be float')

    def testNormalizePopulationForCity(self):
        self.assertEqual(type(self.game.normalizePopulationForCity(self.game.cities[0])), int, 'Should be float')
        self.assertEqual(self.game.normalizePopulationForCity(self.game.cities[0]), 74, 'Should be 74')

if __name__ == '__main__':
    unittest.main()