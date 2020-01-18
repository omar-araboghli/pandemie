class Event:
    def __init__(self, type, city, round, sinceRound, untilRound, participants, prevalence, pathogen):
        self.type = type
        self.city = city
        self.round = str(round)
        self.sinceRound = str(sinceRound)
        self.untilRound = str(untilRound)
        self.participants = str(participants) 
        self.prevalence = str(prevalence)
        self.pathogen = pathogen
