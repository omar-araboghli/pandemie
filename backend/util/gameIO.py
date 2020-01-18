import sys
import os
import json

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'converters'))

def loadGameFromGamesPathWithNrAndRound(gamesPath, number, gameRound):
    gamePath = gamesPath + '\\g' + str(number) + '-r' + str(gameRound) + '.json'
    with open(gamePath) as jsonFile:
        data = json.load(jsonFile)
        return data

def getRoundsForGameInPath(game, path):
    prefix = 'g' + str(game) + '-r'
    files = [i for i in os.listdir(path) if i.startswith(prefix)]
    return files

def getJsonFilesInDirectory(dir_path):
    files = []

    for file in os.listdir(dir_path):
        if os.path.splitext(file)[1] == '.json' and 'summary' not in os.path.splitext(file)[0]:
            files.append(os.path.join(dir_path, file))

    return files

def getGameNumber(json_file):
    basename = os.path.basename(json_file)
    return basename

def loadJsonFile(json_file):
    with open(json_file, encoding='utf-8') as json_object:
        json_data = json.load(json_object)
    return json_data

def loadGameFromFile(json_file):
    json_data = loadJsonFile(json_file)
    return loadGameFromData(json_data)

def loadGameFromData(json_data):
    from GameConverter import Converter
    converter = Converter()
    return converter.convertGame(json_data)