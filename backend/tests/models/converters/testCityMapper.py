import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'converters'))
from CityMapper import CityMapper

class TestCityMapper(unittest.TestCase):

    cityMapper = CityMapper(["zero","one","two","three","four","five","six","seven","eight"])

    def testGetCityUsingId(self):
        self.assertEqual(self.cityMapper.getCityUsingId(3), "three", "Should be three")

    def testGetIdUsingCity(self):
        self.assertEqual(self.cityMapper.getIdUsingCity("three"), 3, "Should be 3")
    
if __name__ == '__main__':
    unittest.main()