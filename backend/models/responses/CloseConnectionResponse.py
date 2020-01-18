from Response import Response 

class CloseConnectionResponse(Response):
    requiredParameters = ['fromCity', 'toCity', 'rounds']

    def __init__(self, fromCity, toCity, rounds):
        Response.__init__(self, type='closeConnection', fromCity=fromCity, toCity=toCity, rounds=rounds)
        
    def getPointsRequired(self):
        return (3 * self.rounds) + 3

    def respond(self):
        return {'type': self.type, 'fromCity': self.fromCity.name, 'toCity': self.toCity.name, 'rounds': self.rounds}

    def isValidInContextOf(self, game):
        # check the required points
        if int(game.points) < self.getPointsRequired():
            return False

        # check values of parameters
        if self.rounds < 1:
            return False

        # check if there is a connection from A to B
        if self.toCity.name not in game.getCityByName(self.fromCity.name).connections:
            return False

        # check if the connection is already closed
        connectionClosedEvents = game.getCityByName(self.fromCity.name).getLocalEventsByType("connectionClosed")     
        for connectionClosedEvent in connectionClosedEvents:
            if connectionClosedEvent.city == self.toCity.name:
                return False

        # check if the airport in B
        airportClosedEvent = game.getCityByName(self.toCity.name).getLocalEventByType("airportClosed")     
        if airportClosedEvent != None:
            return False
            
        # everything is ok!    
        return True