#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest
import json
import os
import sys
FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models'))
sys.path.insert(1, os.path.join(FILE, '..', 'util'))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'responses'))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'solvers'))

import numpy as np

from RandomWalker import RandomWalker
from gameIO import loadGameFromData
from EndRoundResponse import EndRoundResponse

gameNumber = 0
lastAction = EndRoundResponse()
actionNumber = 0

@post("/")
def index():
    global actionNumber
    global lastAction
    game = request.json
    isNew(game)

    print(f'round: {game["round"]}, outcome: {game["outcome"]}')

    gameJsonFileName = 'g' + str(gameNumber) + '-r' + str(game["round"]) + '-' + str(actionNumber) 

    with open(os.path.join(FILE, '..', '..', 'jsons', 'validatedRandomWalkerReduced',  gameJsonFileName + '.json'), 'w') as outfile:
        game['lastAction'] = lastAction.respond()
        json.dump(game, outfile, indent=4)

    gameModel = loadGameFromData(game)

    randomWalker = RandomWalker(gameModel, 2) 
    validActions , possibilityVector = randomWalker.createValidActionsSetForGame(gameModel)
    
    with open(os.path.join(FILE, '..', '..', 'jsons', 'validatedRandomWalkerReduced',  gameJsonFileName + '-probVector'), 'wb') as outfile:
        np.save(outfile, possibilityVector)

    lastAction = randomWalker.getRandomValidAction(gameModel)
    actionNumber += 1
    
    respond = lastAction.respond()
    if respond['type'] == 'endRound':
        actionNumber = 0

    return respond


def isNew(game):
    global gameNumber
    if game["outcome"] != 'pending':
        gameNumber = gameNumber + 1


BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host="0.0.0.0", port=50123, quiet=True)
