from Response import Response 

class EndRoundResponse(Response):
    requiredParameters = []

    def __init__(self):
        Response.__init__(self, type='endRound')

    def getPointsRequired(self):
        return 0

    def respond(self):
        return {'type': self.type}

    def isValidInContextOf(self, game):
        # everything is ok!
        return True