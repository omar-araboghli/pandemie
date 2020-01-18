from Response import Response 

class DeployVaccineResponse(Response):
    requiredParameters = ['city', 'pathogen']

    def __init__(self, city, pathogen):
        Response.__init__(self, type='deployVaccine', city=city, pathogen=pathogen)

    def getPointsRequired(self):
        return 5

    def respond(self):
        return {'type': self.type, 'city': self.city.name, 'pathogen': self.pathogen}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False
        
        # check if vaccine deployed for this pathogen
        if not game.isVaccineAvailableByPathogenName(self.pathogen):
            return False

        # everything is ok!    
        return True