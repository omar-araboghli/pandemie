from Response import Response 

class DevelopMedicationResponse(Response):
    requiredParameters = ['pathogen']

    def __init__(self, pathogen):
        Response.__init__(self, type='developMedication', pathogen=pathogen)

    def getPointsRequired(self):
        return 20

    def respond(self):
        return {'type': self.type, 'pathogen': self.pathogen}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False
        
        # check if pathogen encountered
        if not game.isPathogenEncounteredByName(self.pathogen):
            return False

        # everything is ok!    
        return True