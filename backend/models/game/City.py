class City:
    def __init__(self, name, latitude, longitude, population, connections,
                     economy, government, hygiene, awareness, events):
        self.name = name
        self.latitude = str(latitude)
        self.longitude = str(longitude)
        self.population = str(population) 
        self.connections = connections
        self.economy = str(economy)
        self.government = str(government)
        self.hygiene = str(hygiene)
        self.awareness = str(awareness) 
        self.events = events

    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name

    def getLocalEventByType(self, type):
        # returns an event that can be occur one time, e.g. quarantine
        for event in self.events:
            if event.type == type:
                return event
        return None
        
    def getLocalEventsByType(self, type):
        # returns list of events that can be occur multiple times, e.g. medicationDeployed
        localEvents = []
        for event in self.events:
            if event.type == type:
                localEvents.append(event)
        return localEvents 