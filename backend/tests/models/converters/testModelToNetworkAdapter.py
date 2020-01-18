import unittest
import sys
import os
import numpy as np

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'converters'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))
from ModelToNetworkAdapter import ModelToNetworkAdapter
from gameIO import loadGameFromFile

class TestModelToNetworkAdapter(unittest.TestCase):

    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game = loadGameFromFile(path)
    adapter = ModelToNetworkAdapter(game)

    def testconvertInputReduced(self):
        self.assertEqual(type(self.adapter.convertInputReduced()), np.ndarray, 'Should be a numpy array')
        self.assertEqual(len(self.adapter.convertInputReduced()), 96077, 'Should be 96077')
        # interpreting the number of points
        self.assertEqual(self.adapter.convertInputReduced()[-136], 40, 'Should be 40')

    def testGetCityConnectionsFeatures(self):
        city = self.game.cities[0]
        self.assertEqual(type(self.adapter.getCityConnectionsFeatures(city)), np.ndarray, 'Should be a numpy array')
        self.assertEqual(len(self.adapter.getCityConnectionsFeatures(city)), 260, 'Should be 260')
        # Abuja has connection to Boston
        self.assertEqual(self.adapter.getCityConnectionsFeatures(city)[25], 1.0, 'Should be 1.0')
        # Abuja has no connection to Bloemfontein
        self.assertEqual(self.adapter.getCityConnectionsFeatures(city)[24], 0.0, 'Should be 0.0')

if __name__ == '__main__':
    unittest.main()