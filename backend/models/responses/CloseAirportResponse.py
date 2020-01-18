from Response import Response 

class CloseAirportResponse(Response):
    requiredParameters = ['city', 'rounds']

    def __init__(self, city, rounds):
        Response.__init__(self, type='closeAirport', city=city, rounds=rounds)

    def getPointsRequired(self):
        return (5 * self.rounds) + 15

    def respond(self):
        return {'type': self.type, 'city': self.city.name, 'rounds': self.rounds}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False

        # check values of parameters
        if self.rounds < 1:
            return False

        if game.getCityByName(self.city.name).getLocalEventByType("airportClosed") != None:
            return False
            
        # everything is ok!    
        return True