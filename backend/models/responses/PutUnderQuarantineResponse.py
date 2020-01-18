from Response import Response 

class PutUnderQuarantineResponse(Response):
    requiredParameters = ['city', 'rounds']

    def __init__(self, city, rounds):
        Response.__init__(self, type='putUnderQuarantine', city=city, rounds=rounds)

    def getPointsRequired(self):
        return (10 * self.rounds) + 20

    def respond(self):
        return {'type': self.type, 'city': self.city.name, 'rounds': self.rounds}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False

        # check values of parameters
        if self.rounds < 1:
            return False

        # check if there is already a quarantine
        if game.getCityByName(self.city.name).getLocalEventByType("quarantine") != None:
            return False
            
        # everything is ok!    
        return True