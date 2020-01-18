import unittest
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'responses'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'models', 'game'))
sys.path.insert(1, os.path.join(FILE, '..', '..', '..', 'util'))
from EndRoundResponse import EndRoundResponse
from PutUnderQuarantineResponse import PutUnderQuarantineResponse
from ApplyHygienicMeasuresResponse import ApplyHygienicMeasuresResponse
from CallElectionsResponse import CallElectionsResponse
from CloseAirportResponse import CloseAirportResponse
from CloseConnectionResponse import CloseConnectionResponse
from DeployMedicationResponse import DeployMedicationResponse
from DeployVaccineResponse import DeployVaccineResponse
from DevelopMedicationResponse import DevelopMedicationResponse
from DevelopVaccineResponse import DevelopVaccineResponse
from ExertInfluenceResponse import ExertInfluenceResponse
from LaunchCampaignResponse import LaunchCampaignResponse
from Pathogen import Pathogen
from Event import Event
from gameIO import loadGameFromFile

class TestResponse(unittest.TestCase):
    path = os.path.join(FILE, '..', '..', '..', 'resources', 'sample.json')
    game = loadGameFromFile(path)
    city = game.cities[0]
    toCity = game.cities[1]

    def testIsValidInContextOf(self):
        endRoundResponse = EndRoundResponse()
        self.assertTrue(endRoundResponse.isValidInContextOf(self.game), msg="Should be True")
        
        putUnderQuarantineResponse = PutUnderQuarantineResponse(self.city, 1)
        self.assertTrue(putUnderQuarantineResponse.isValidInContextOf(self.game), msg="Should be True")
        putUnderQuarantineResponse = PutUnderQuarantineResponse(self.city, 4)
        self.assertFalse(putUnderQuarantineResponse.isValidInContextOf(self.game), msg="Should be False")
        putUnderQuarantineResponse = PutUnderQuarantineResponse(self.city, -1)
        self.assertFalse(putUnderQuarantineResponse.isValidInContextOf(self.game), msg="Should be False")

        applyHygienicMeasuresResponse = ApplyHygienicMeasuresResponse(self.city)
        self.assertTrue(applyHygienicMeasuresResponse.isValidInContextOf(self.game), msg="Should be True")
        self.game.points = 2
        self.assertFalse(applyHygienicMeasuresResponse.isValidInContextOf(self.game), msg="Should be False")

        callElectionsResponse = CallElectionsResponse('Brazzaville')
        self.assertFalse(callElectionsResponse.isValidInContextOf(self.game), msg="Should be False")
        self.game.points = 40
        self.assertTrue(callElectionsResponse.isValidInContextOf(self.game), msg="Should be True")

        closeAirportResponse = CloseAirportResponse(self.city, 1)
        self.assertTrue(closeAirportResponse.isValidInContextOf(self.game), msg="Should be True")
        closeAirportResponse = CloseAirportResponse(self.city, -1)
        self.assertFalse(closeAirportResponse.isValidInContextOf(self.game), msg="Should be False")
        closeAirportResponse = CloseAirportResponse(self.city, 10)
        self.assertFalse(closeAirportResponse.isValidInContextOf(self.game), msg="Should be False")

        closeConnectionResponse = CloseConnectionResponse(self.city, self.toCity, 1)
        self.assertFalse(closeConnectionResponse.isValidInContextOf(self.game), msg="Should be False")
        closeConnectionResponse = CloseConnectionResponse(self.city, self.toCity, 1)
        self.assertFalse(closeConnectionResponse.isValidInContextOf(self.game), msg="Should be False")
        closeConnectionResponse = CloseConnectionResponse(self.city, self.toCity, 50)
        self.assertFalse(closeConnectionResponse.isValidInContextOf(self.game), msg="Should be False")
        closeConnectionResponse = CloseConnectionResponse(self.city, self.toCity, -1)
        self.assertFalse(closeConnectionResponse.isValidInContextOf(self.game), msg="Should be False")

        deployMedicationResponse = DeployMedicationResponse('Brazzaville', 'Procrastinalgia')
        self.assertFalse(deployMedicationResponse.isValidInContextOf(self.game), msg="Should be False")

        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        pathogenEncounteredEvent = Event(type='medicationAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)
        self.game.events.append(pathogenEncounteredEvent)
        self.assertTrue(deployMedicationResponse.isValidInContextOf(self.game), msg="Should be True")

        deployVaccineResponse = DeployVaccineResponse('Brazzaville', 'Procrastinalgia')
        self.assertFalse(deployVaccineResponse.isValidInContextOf(self.game), msg="Should be False")
        
        pathogen = Pathogen(name='Procrastinalgia', infectivity='', mobility='', duration='', lethality='')
        pathogenEncounteredEvent = Event(type='vaccineAvailable', city='', round='', sinceRound='',
                                    untilRound='', participants='', prevalence='',
                                    pathogen=pathogen)
        self.game.events.append(pathogenEncounteredEvent)
        self.assertTrue(deployVaccineResponse.isValidInContextOf(self.game), msg="Should be True")

        developMedicationResponse = DevelopMedicationResponse('Procrastinalgia')
        self.assertTrue(developMedicationResponse.isValidInContextOf(self.game), msg="Should be True")
        self.game.points = 1
        self.assertFalse(developMedicationResponse.isValidInContextOf(self.game), msg="Should be False")

        developVaccineResponse = DevelopVaccineResponse('Procrastinalgia')
        self.assertFalse(developVaccineResponse.isValidInContextOf(self.game), msg="Should be False")
        self.game.points = 50
        self.assertTrue(developVaccineResponse.isValidInContextOf(self.game), msg="Should be True")

        exertInfluenceResponse = ExertInfluenceResponse('Brazzaville')
        self.assertTrue(exertInfluenceResponse.isValidInContextOf(self.game), msg="Should be True")
        self.game.points = 1
        self.assertFalse(exertInfluenceResponse.isValidInContextOf(self.game), msg="Should be False")

        launchCampaignResponse = LaunchCampaignResponse('Brazzaville')
        self.assertFalse(launchCampaignResponse.isValidInContextOf(self.game), msg="Should be False")
        self.game.points = 50
        self.assertTrue(launchCampaignResponse.isValidInContextOf(self.game), msg="Should be True")


if __name__ == '__main__':
    unittest.main()