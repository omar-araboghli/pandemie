from Solver import Solver 
import random
import numpy as np 

class RandomWalker(Solver):

    def getRandomValidAction(self, game):
        validActionsSet, probVector = self.createValidActionsSetForGame(game)
        randomActionID = random.randint(0, len(validActionsSet) -1 )
        randomAction = validActionsSet[randomActionID]
        return randomAction

    def createValidActionsSetForGame(self, game):
        possibleActions = self.generateAllPossibleActions()
        validActions = []

        probabilityVector = np.zeros(len(possibleActions))

        i = 0
        for action in possibleActions:
            if action.isValidInContextOf(game):
                validActions.append(action)
                probabilityVector[i] = 1
            i = i + 1
        
        probabilityVector = probabilityVector / len(validActions)
        return validActions, probabilityVector


