import sys
import os
import random

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'responses'))
from Response import Response
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

class Solver():

    #toDo: move action generation to class Action generator

    def __init__(self, game, maxNumberOfRoundsInFuture):
        self.game = game
        self.maxNumberOfRoundsInFuture = maxNumberOfRoundsInFuture

    def generateAllPossibleActions(self):
        actionsList = []
        actionClasses = Response.__subclasses__()
        #toDo: create list connecting needed parameters and the needed function to call
        for actionClass in actionClasses:
            if actionClass.requiredParameters == []:
                actionsList.append(actionClass())
            if actionClass.requiredParameters == ["city"]:
                actionRepeatedForAllCities = self.generateActionForAllCities(actionClass)
                actionsList.extend(actionRepeatedForAllCities)
            if actionClass.requiredParameters == ["city", "rounds"]:
                actionRepeatedForAllCitiesForNRounds = self.generateActionForAllCitiesAndNumberOfRounds(actionClass)
                actionsList.extend(actionRepeatedForAllCitiesForNRounds)
            if actionClass.requiredParameters == ["pathogen"]:
                actionRepeatedForAllPathogens = self.generateActionForAllPathogens(actionClass)
                actionsList.extend(actionRepeatedForAllPathogens)
            if actionClass.requiredParameters == ["city", "pathogen"]:
                actionRepeatedForAllPathogensInAllCities = self.generateActionForAllPathogensAndAllCities(actionClass)
                actionsList.extend(actionRepeatedForAllPathogensInAllCities)
            if actionClass.requiredParameters == ["fromCity", "toCity", "rounds"]:
                actionCloseAllConnections = self.generateAllCloseConnections()
                actionsList.extend(actionCloseAllConnections)

        return actionsList

    def createValidActionsSetForGame(self, game):
        possibleActions = self.generateAllPossibleActions()
        validActions = []
        for action in possibleActions:
            if action.isValidInContextOf(game):
                validActions.append(action)
        return validActions

    def getRandomValidAction(self, game):
        validActionsSet = self.createValidActionsSetForGame(game)
        randomActionID = random.randint(0, len(validActionsSet) -1 )
        randomAction = validActionsSet[randomActionID]
        return randomAction

    def generateActionForAllCities(self,action):
        resList = []
        for city in self.game.cities:
            createdAction = action(city=city)
            resList.append(createdAction)
        return resList

    def generateActionForAllCitiesAndNumberOfRounds(self,action):
        resList = []
        for roundNumber in range(1, self.maxNumberOfRoundsInFuture):
            for city in self.game.cities:
                createdAction = action(city=city, rounds=roundNumber)
                resList.append(createdAction)
        return resList

    def generateActionForAllPathogensInCity(self,action, city):
        resList = []
        for pathogen in self.game.getAllPathogenNames():
            if(city == None):
                createdAction = action(pathogen=pathogen)
            else:
                createdAction = action(pathogen=pathogen, city=city)
            resList.append(createdAction)
        return resList


    def generateActionForAllPathogens(self,action):
        return self.generateActionForAllPathogensInCity(action, None)

    def generateActionForAllPathogensAndAllCities(self,action):
        resList = []
        for city in self.game.cities:
            cityResList = self.generateActionForAllPathogensInCity(action, city)
            resList.extend(cityResList)
        return resList
    
    def generateAllCloseConnections(self):
        resList = []
        for roundNumber in range(1, self.maxNumberOfRoundsInFuture):
            for city in self.game.cities:
                for connection in city.connections:
                    toCity = self.game.getCityByName(connection)
                    createdAction = CloseConnectionResponse(fromCity=city, toCity=toCity ,rounds=roundNumber)
                    resList.append(createdAction)
        return resList