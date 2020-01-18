import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'game'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))

from Event import Event
from Pathogen import Pathogen
from gameIO import loadGameFromFile

class TestEvent(unittest.TestCase):

    def testInit(self):
        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        event = Event(type='vaccineAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)
        
        self.assertEqual(type(event), Event, 'Should be an Event')
        self.assertEqual(event.type, 'vaccineAvailable', "Should be vaccineAvailable")
        self.assertEqual(event.pathogen.name, 'Procrastinalgia', "Should be Procrastinalgia")

if __name__ == '__main__':
    unittest.main()