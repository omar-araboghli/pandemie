from Response import Response 

class CallElectionsResponse(Response):
    requiredParameters = ['city']

    def __init__(self, city):
        Response.__init__(self, type='callElections', city=city)

    def getPointsRequired(self):
        return 3

    def respond(self):
        return {'type': self.type, 'city': self.city.name}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False
            
        # everything is ok!    
        return True