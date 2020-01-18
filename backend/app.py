import sys
import os, signal
import subprocess
import json 
import platform

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, 'util'))
sys.path.insert(1, os.path.join(FILE, 'models', 'solvers'))
sys.path.insert(1, os.path.join(FILE, 'models', 'converters'))

import numpy as np
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from gameIO import loadGameFromData, loadGameFromFile
from DQNAgent import DQNAgent
from ModelToNetworkAdapter import ModelToNetworkAdapter

app = Flask(__name__)
cors = CORS(app)
frontendInfo = {"round": 0, "outcome": 'pending', "points": '40', "action": ''}
pid = None

path = os.path.join(FILE, 'resources', 'sample.json')
gameObject = loadGameFromFile(path)

# create one agent with dummy game
agent = DQNAgent(game=gameObject, maxNumberOfRoundsInFuture=2)

@app.route('/play', methods=['POST'])
def play():
    # get game as request body and convert it to game object
    gameJson = request.json
    gameObject = loadGameFromData(gameJson)

    # update the agent and its IO adapter
    agent.updateGame(gameObject)
    adapter = ModelToNetworkAdapter(game=gameObject)

    # load last trained model
    agent.load('model.h5')

    # convert the game to input vector
    state = adapter.convertInputReduced()
    state = np.reshape(state, [1, agent.stateSize])

    # predict the action and respond
    actionID = agent.act(state)
    action = agent.possibleActions[actionID]
    print('round: {}, action: {}, outcome: {}'.format(gameObject.round, type(action), gameObject.outcome))
    
    # set information for the frontend
    global frontendInfo
    frontendInfo = gameJson
    frontendInfo['action'] = action.respond()['type']

    return action.respond()

@app.route('/start', methods=['GET'])
@cross_origin()
def start_game():

    if 'Windows' in platform.system():
        command = ['ic20_windows.exe', '-t', '0', '-u', 'http://localhost:443/play']
    elif 'Linux' in platform.system():
        command = ['./ic20_linux', '-t', '0', '-u', 'http://localhost:443/play']

    # start a client
    global pid
    p = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    pid = p.pid

    return 'Game Started!'

@app.route('/frontend', methods=['GET'])
@cross_origin()
def get_frontend():
    return frontendInfo

@app.route('/stop', methods=['GET'])
@cross_origin()
def stop_game():
    if not pid:
        return {'Game': 'could not be stopped, please try again'}
    
    if 'Windows' in platform.system():
        os.system('taskkill /F /t /pid >nul 2>&1 {}'.format(pid))
    elif 'Linux' in platform.system():
        os.system('kill -9 {}'.format(pid))

    return {'Game': 'Stopped'}


@app.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port='443', threaded=False)