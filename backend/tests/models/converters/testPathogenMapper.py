import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'converters'))
from PathogenMapper import PathogenMapper

class TestPathogenMapper(unittest.TestCase):

    pathogenMapper = PathogenMapper()

    def testInit(self):
        self.assertEqual(type(self.pathogenMapper.pathogensMap), dict, 'Should be a dict')
        self.assertEqual(len(self.pathogenMapper.pathogensMap), 19, 'Should be 19')

    def testGetPathogenUsingId(self):
        self.assertEqual(self.pathogenMapper.getPathogenUsingId(3), "Moricillus \u2620", "Should be Moricillus \u2620")

    def testGetIdUsingPathogen(self):
        self.assertEqual(self.pathogenMapper.getIdUsingPathogen("Rhinonitis"), 12, "Should be 12")
    
if __name__ == '__main__':
    unittest.main()