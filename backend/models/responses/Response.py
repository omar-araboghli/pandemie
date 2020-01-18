class Response:
    def __init__(self, type, city=None, rounds=None, fromCity=None, toCity=None, pathogen=None):
        self.type = type
        self.city = city 
        self.rounds = rounds
        self.fromCity = fromCity
        self.toCity = toCity
        self.pathogen = pathogen

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Response):
            return self.type  == other.type and\
            self.city == other.city and\
            self.rounds == other.rounds and\
            self.fromCity == other.fromCity and\
            self.toCity == other.toCity and\
            self.pathogen == other.pathogen
        return False

    def __hash__(self):
        return hash((self.type, self.city, self.rounds, self.fromCity, self.toCity, self.pathogen))