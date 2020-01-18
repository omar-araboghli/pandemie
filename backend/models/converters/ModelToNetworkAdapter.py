import numpy as np
import os 
import sys 

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'solvers'))

from PathogenMapper import PathogenMapper
from CityMapper import CityMapper
from Solver import Solver



class ModelToNetworkAdapter:
    def __init__(self, game):
        self.game = game
        self.pathogenMapper = PathogenMapper()
        self.cityMapper = CityMapper(game.getCityNamesAsList())

    def convertInputReduced(self):
        # 95940 features
        features = self.extractLocalFeaturesReduced()
        # 137 features
        features = np.append(features, self.extractGlobalFeatures())
        return features

    def extractLocalFeaturesReduced(self):
        localFeatures = np.array([], dtype=np.float32)

        for city in self.game.cities:
            # city0_has_connection_to_city1 ... city_0_has_connection_to_city259
            localFeatures = np.append(localFeatures, self.getCityConnectionsFeaturesReduced(city))

            # lat_city0, lng_city0, population_city0, economy_city0, government_city0, hygiene_city0, awareness_city0
            normalizedPopulation = self.game.normalizePopulationForCity(city)
            localFeatures = np.append(localFeatures, [float(city.latitude), float(city.longitude), normalizedPopulation,
                                                     float(city.economy), float(city.government), float(city.hygiene),
                                                     float(city.awareness)])

            # airportClosed_since_city0
            airportClosedEvent = city.getLocalEventByType('airportClosed')
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(airportClosedEvent, 'sinceRound'))

            # airportClose_until_city0
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(airportClosedEvent, 'untilRound'))

            # quarantine_since_city0
            quarantineEvent = city.getLocalEventByType('quarantine')
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(quarantineEvent, 'sinceRound'))

            # quarantine_until_city0
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(quarantineEvent, 'untilRound'))
        
            # vaccine_deployment_round_for_p0_in_city0 ... vaccine_deployment_round_for_p18_in_city0
            vaccineDeployedEvents = city.getLocalEventsByType('vaccineDeployed')
            localFeatures = np.append(localFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(vaccineDeployedEvents, 'round'))

            # medication_deployment_round_for_p0_in_city0 ... medication_deployment_round_for_p18_in_city0
            medicationDeployedEvents = city.getLocalEventsByType('medicationDeployed')
            localFeatures = np.append(localFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(medicationDeployedEvents, 'round'))

            # uprising_since_city0
            uprisingEvent = city.getLocalEventByType('uprising')
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(uprisingEvent, 'sinceRound'))

            # uprising_participants_city0
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(uprisingEvent, 'participants'))

            # p0_outbreak_since_in_city0 ... p18_outbreak_since_in_city0
            outbreakEvents = city.getLocalEventsByType('outbreak')
            localFeatures = np.append(localFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(outbreakEvents, 'sinceRound'))

            # p0_outbreak_prevalence_in_city0 ... p18_prevalence_since_in_city0
            localFeatures = np.append(localFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(outbreakEvents, 'prevalence'))

            # p0_bioTerrorism_round_in_city0 ... p18_bioTerrorism_round_in_city0
            bioTerrorismEvents = city.getLocalEventsByType('bioTerrorism')
            localFeatures = np.append(localFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(bioTerrorismEvents, 'round'))

            # antivaccinationism_since_city0
            antiVaccinationismEvent = city.getLocalEventByType('antiVaccinationism')
            localFeatures = np.append(localFeatures, self.getFeatureOfEventByAttribute(antiVaccinationismEvent, 'sinceRound'))

        return localFeatures

    def extractGlobalFeatures(self):
        # 137 features
        globalFeatures = np.array([self.game.round, self.game.points], dtype=np.float32)

        # vaccineInDevelopment_for_p0_since  ... vaccineInDevelopment_for_p18_since
        vaccineInDevelopmentEvents = self.game.getGlobalEventsByType('vaccineInDevelopment')
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(vaccineInDevelopmentEvents, 'sinceRound'))

        # vaccineInDevelopment_for_p0_until  ... vaccineInDevelopment_for_p18_until
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(vaccineInDevelopmentEvents, 'untilRound'))
        
        # vaccineAvailable_for_p0_since ... vaccineAvailable_for_p18_since
        vaccineAvailableEvents = self.game.getGlobalEventsByType('vaccineAvailable')
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(vaccineAvailableEvents, 'sinceRound'))
        
        # medicationInDevelopment_for_p0_since  ... medicationInDevelopment_for_p18_since
        medicationInDevelopmentEvents = self.game.getGlobalEventsByType('medicationInDevelopment')
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(medicationInDevelopmentEvents, 'sinceRound'))
        
        # medicationInDevelopment_for_p0_until  ... medicationInDevelopment_for_p18_until
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(medicationInDevelopmentEvents, 'untilRound'))
        
        # medicationAvailable_for_p0_since ... medicationAvailable_for_p18_since
        medicationAvailableEvents = self.game.getGlobalEventsByType('medicationAvailable')
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(medicationAvailableEvents, 'sinceRound'))

        # p0_encountered_round ... p18_encountered_round
        pathogenEncounteredEvents = self.game.getGlobalEventsByType('pathogenEncountered')
        globalFeatures = np.append(globalFeatures, self.getFeaturesOfEventsRegardingPathogenIdByAttribute(pathogenEncounteredEvents, 'round'))
        
        # economicCrisis_sinceRound
        economicCrisisEvent = self.game.getGlobalEventByType('economicCrisis')
        globalFeatures = np.append(globalFeatures, self.getFeatureOfEventByAttribute(economicCrisisEvent, 'sinceRound'))

        # largeScalePanic_sinceRound
        largeScalePanicEvent = self.game.getGlobalEventByType('largeScalePanic')
        globalFeatures = np.append(globalFeatures, self.getFeatureOfEventByAttribute(largeScalePanicEvent, 'sinceRound'))

        return globalFeatures
    
    def getCityConnectionsFeatures(self, city):
        cityConnectionsFeatures = np.zeros(260)
        for connection in city.connections:
            index = self.cityMapper.getIdUsingCity(connection)
            cityConnectionsFeatures[index] = 1.0 
        return cityConnectionsFeatures

    def getCityConnectionsFeaturesReduced(self, city):
        cityConnectionsFeatures = np.zeros(260)
        for connection in city.connections:
            index = self.cityMapper.getIdUsingCity(connection)
            cityConnectionsFeatures[index] = 1.0 

        # close closed connections
        connectionClosedEvents = city.getLocalEventsByType('connectionClosed')
        for event in connectionClosedEvents:
            index = self.cityMapper.getIdUsingCity(event.city)
            cityConnectionsFeatures[index] = 0.0

        return cityConnectionsFeatures

    def getFeaturesOfEventsRegardingPathogenIdByAttribute(self, events, attributeName=None):
        featuresOfAttribute = np.zeros(19)
        for event in events:
            index = self.pathogenMapper.getIdUsingPathogen(event.pathogen.name)
            featuresOfAttribute[index] = self.getAttributeFromEvent(event, attributeName)
        return featuresOfAttribute

    def getFeaturesOfEventsRegardingCityIdByAttribute(self, events, attributeName=None):
        featuresOfAttribute = np.zeros(260)
        for event in events:
            index = self.cityMapper.getIdUsingCity(event.city)
            featuresOfAttribute[index] = self.getAttributeFromEvent(event, attributeName)
        return featuresOfAttribute
    
    def getFeatureOfEventByAttribute(self, event, attributeName=None):
        feature = np.zeros(1)
        if not event:
            return feature

        feature[0] = self.getAttributeFromEvent(event, attributeName)
        return feature

    def getAttributeFromEvent(self, event, attributeName):
        attribute = None

        if attributeName == 'sinceRound':
            attribute = event.sinceRound
        elif attributeName == 'untilRound':
            attribute = event.untilRound
        elif attributeName == 'round':
            attribute = event.round
        elif attributeName == 'participants':
            attribute = event.participants
        elif attributeName == 'prevalence':
            attribute = event.prevalence

        return float(attribute)