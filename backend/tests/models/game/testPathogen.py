import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'game'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))

from Pathogen import Pathogen
from gameIO import loadGameFromFile

class TestPathogen(unittest.TestCase):

    def testInit(self):
        pathogen = Pathogen(name='Procrastinalgia', infectivity='+',
                            mobility='-', duration='--', lethality='++')
                            
        self.assertEqual(pathogen.name, 'Procrastinalgia', "Should be Procrastinalgia")
        self.assertEqual(pathogen.infectivity, '+', "Should be +")
        self.assertEqual(pathogen.mobility, '-', "Should be -")
        self.assertEqual(pathogen.duration, '--', "Should be --")
        self.assertEqual(pathogen.lethality, '++', "Should be ++")

if __name__ == '__main__':
    unittest.main()