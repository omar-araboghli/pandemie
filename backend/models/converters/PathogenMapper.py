import json
import sys
import os

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', 'util'))

class PathogenMapper:
    
    pathogensMap = dict()

    def __init__(self):
        self.pathogensMap = self.getPathogensFromResource()

    def getPathogenUsingId(self, id):
        return self.pathogensMap[id]

    def getIdUsingPathogen(self, pathogen):
        listResult = [i for i in self.pathogensMap.keys() if self.pathogensMap[i] == pathogen]
        return listResult[0]

    def getPathogensFromResource(self):
        from gameIO import loadJsonFile
        jsonData = loadJsonFile(os.path.join(FILE, '..', '..' ,'resources', 'pathogens.json'))
        return {int(k): v for k, v in jsonData.items()}