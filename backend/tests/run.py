import unittest

testmodules = [
    'models.game.testGame',
    'models.game.testCity',
    'models.game.testEvent',
    'models.game.testPathogen',
    'models.converters.testCityMapper',
    'models.converters.testPathogenMapper',
    'models.converters.testGameConverter',
    'models.converters.testModelToNetworkAdapter',
    'models.responses.testResponse',
    'models.solvers.testSolver',
    'models.solvers.testRandomWalker'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite)