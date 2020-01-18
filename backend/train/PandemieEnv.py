import gym 
from gym import error, spaces, utils
from gym.utils import seeding


import subprocess
import sys
import os, signal
import platform
import numpy as np
from threading import Thread
from multiprocessing import Process

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'responses'))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'converters'))

IN_COLAB = 'google.colab' in sys.modules

from GameConverter import Converter

if IN_COLAB:
    from train.WebServer import WebServer
else:
    from WebServer import WebServer

from EndRoundResponse import EndRoundResponse

operatingSystemExtension = 'windows.exe' if os.name == 'nt' else 'linux' 
CLIENT_PATH = os.path.join(FILE, '..', 'ic20_' + operatingSystemExtension)

class PandemieEnv(gym.Env):
    metadata = {'render.modes': ['human']}   
    def __init__(self):
        self.converter = Converter()
        self.communicator = WebServer()
        self.clientThread = None
        
 
    def step(self, action):
        if not action.isValidInContextOf(self.game):
           reward = -1.0

        nextStateJson = self.communicator.sendMessage(action.respond())
        self.game = self.converter.convertGame(nextStateJson) 
        #evaluate the resulting model
        observation = self.game
        done = self.game.isOver()
        
        if 'reward' not in locals() :
            reward = self._getReward(self.game.outcome, action)

        if action.type == 'endRound':
            self.lastRoundOverallInfected = self.game.getOverallInfected()
            self.lastRoundPopulation = self.game.getOverallPopulation()
        #print("current reward is :", reward)
        info = {}
        #get the current population
        self.currentPopulation = self.game.getOverallPopulation()
        return observation, reward, done, info
 
    def reset(self):
        # flush client
        self.killThread(self.clientThread)
        # run a new client (game)
        self.clientThread = Process(target = subprocess.run, args=([CLIENT_PATH, "-t", "0", "-o", "delme"], ))
        self.clientThread.start()
        # flush socket 
        self.communicator.acceptConnection()
        #receive message, and convert it into game
        initState = self.communicator.recieveMessage()
        self.game = self.converter.convertGame(initState)
        #get the inital population
        self.startPopulation = self.game.getOverallPopulation()
        self.currentPopulation = self.startPopulation
        self.lastRoundOverallInfected = self.game.getOverallInfected()
        self.lastRoundPopulation = self.game.getOverallPopulation()
        return self.game
        
    def render(self, mode='human', close=False):
        pass

	
    def _getReward(self, outcome, action):
        if outcome == "win":
            return 300 - int(self.game.round)
        if outcome == "loss":
            return -150 + int(self.game.round)
        
        deltaPopulation = self.game.getOverallPopulation() - self.lastRoundPopulation
        deltaInfected = self.game.getOverallInfected() - self.lastRoundOverallInfected
        pn = self.game.getOverallPopulation()
        reward = (deltaPopulation - deltaInfected) / pn
        print("dP = {}, dIP={}, pn={} , reward={}".format(deltaPopulation, deltaInfected, pn , reward))
        #lateGameFactor = self.startPopulation / self.game.getOverallPopulation()
        #correctionFactor = -1 

        #if deltaPopulation == 0:
        #    deltaPopulation = 1

        #if deltaInfected > 0 and deltaPopulation < 0:
        #    correctionFactor = 1

        #return correctionFactor * (deltaInfected/deltaPopulation) * lateGameFactor

        #another function to be tries later
        #(x**3 + y **3 ) ** (1/3)
        #p3ip3 = (deltaInfected**3 + deltaPopulation**3)
        #return (-1) * np.sign(p3ip3) *(abs(p3ip3) ** (1. / 3))

        return reward

    def killThread(self, thread):
        if thread:
            if 'Windows' in platform.system():
                # force kill all child processes from the parent process (pid) and redirect output to stderr
                os.system('taskkill /F /t /pid >nul 2>&1 {}'.format(thread.pid))
            elif 'Linux' in platform.system():
                # send termination signal to the thread in order to be killed
                os.system('kill -9 {}'.format(thread.pid))



'''
if __name__ == '__main__':
    env = PandemieEnv()
    for i_episode in range(200):
        observation = env.reset()
        for t in range(100):
            endRound = EndRoundResponse()
            try:
                observation, reward, done, info = env.step(endRound)
            except:
                observation = env.reset()
                t = 0 
            #print(done)
            if done:
                print("episode {} finished in {} iterations".format(i_episode, t+1))
                break
    # kill last client and close connection
    env.killThread(env.clientThread)
    env.communicator.endConnection()

'''
