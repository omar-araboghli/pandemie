from Response import Response 

class DeployMedicationResponse(Response):
    requiredParameters = ['city', 'pathogen']

    def __init__(self, city, pathogen):
        Response.__init__(self, type='deployMedication', city=city, pathogen=pathogen)

    def getPointsRequired(self):
        return 10

    def respond(self):
        return {'type': self.type, 'city': self.city.name, 'pathogen': self.pathogen}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False
        
        # check if medication developed for this pathogen
        if not game.isMedicationAvailableByPathogenName(self.pathogen):
            return False

        # everything is ok!    
        return True