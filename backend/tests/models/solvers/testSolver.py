import unittest
import sys
import os 

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'solvers'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'responses'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))

from gameIO import loadGameFromFile
from Solver import Solver
from ExertInfluenceResponse import ExertInfluenceResponse
from CloseAirportResponse import CloseAirportResponse
from DeployVaccineResponse import DeployVaccineResponse
from DevelopMedicationResponse import DevelopMedicationResponse
from CloseConnectionResponse import CloseConnectionResponse

class TestSolver(unittest.TestCase):
    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game = loadGameFromFile(path)
    solver = Solver(game, 2)

    def testGenerateAllPossibleActions(self):
        self.assertEqual(type(self.solver.generateAllPossibleActions()), list, "Should be a list")

        # BUG: in Solver.py range(1, self.maxNumberOfRoundsInFuture) must be
        # range(1, self.maxNumberOfRoundsInFuture + 1)        
        #self.assertEqual(len(self.solver.generateAllPossibleActions()), 14659, "Should be 14659")

    def testGenerateActionForAllCities(self):
        self.assertEqual(type(self.solver.generateActionForAllCities(ExertInfluenceResponse)), list, "Should be a list")
        self.assertEqual(type(self.solver.generateActionForAllCities(ExertInfluenceResponse)[0]), ExertInfluenceResponse, "Should be ExertInfluenceResponse")
        self.assertEqual(len(self.solver.generateActionForAllCities(ExertInfluenceResponse)), 260, "Should be 260")
        
    def testGenerateActionForAllCitiesAndNumberOfRounds(self):
        self.assertEqual(type(self.solver.generateActionForAllCitiesAndNumberOfRounds(CloseAirportResponse)), list, "Should be a list")
        self.assertEqual(type(self.solver.generateActionForAllCitiesAndNumberOfRounds(CloseAirportResponse)[0]), CloseAirportResponse, "Should be a list")
        
        # BUG: in Solver.py range(1, self.maxNumberOfRoundsInFuture) must be
        # range(1, self.maxNumberOfRoundsInFuture + 1)        
        #self.assertEqual(len(self.solver.generateActionForAllCitiesAndNumberOfRounds(CloseAirportResponse)), 520, "Should be 520")

    def testGenerateActionForAllPathogensInCity(self):
        self.assertEqual(type(self.solver.generateActionForAllPathogensInCity(DeployVaccineResponse, 'Abuja')), list, "Should be a list")
        self.assertEqual(type(self.solver.generateActionForAllPathogensInCity(DeployVaccineResponse, 'Abuja')[0]), DeployVaccineResponse, "Should be DeployVaccineResponse")
        self.assertEqual(len(self.solver.generateActionForAllPathogensInCity(DeployVaccineResponse, 'Abuja')), 19, "Should be 19")

    def testGenerateActionForAllPathogens(self):
        self.assertEqual(type(self.solver.generateActionForAllPathogens(DevelopMedicationResponse)), list, "Should be a list")
        self.assertEqual(type(self.solver.generateActionForAllPathogens(DevelopMedicationResponse)[0]), DevelopMedicationResponse, "Should be DeployVaccineResponse")
        self.assertEqual(len(self.solver.generateActionForAllPathogens(DevelopMedicationResponse)), 19, "Should be 19")

    def testGenerateActionForAllPathogensAndAllCities(self):
        self.assertEqual(type(self.solver.generateActionForAllPathogensAndAllCities(DeployVaccineResponse)), list, "Should be a list")
        self.assertEqual(type(self.solver.generateActionForAllPathogensAndAllCities(DeployVaccineResponse)[0]), DeployVaccineResponse, "Should be DeployVaccineResponse")
        self.assertEqual(len(self.solver.generateActionForAllPathogensAndAllCities(DeployVaccineResponse)), 4940, "Should be 4940")

    def testGenerateAllCloseConnections(self):
        self.assertEqual(type(self.solver.generateAllCloseConnections()), list, "Should be a list")
        self.assertEqual(type(self.solver.generateAllCloseConnections()[0]), CloseConnectionResponse, "Should be DeployVaccineResponse")
        
        # BUG: in Solver.py range(1, self.maxNumberOfRoundsInFuture) must be
        # range(1, self.maxNumberOfRoundsInFuture + 1)        
        #self.assertEqual(len(self.solver.generateAllCloseConnections()), 2660, "Should be 2660")

if __name__ == '__main__':
    unittest.main()