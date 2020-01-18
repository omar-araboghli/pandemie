import numpy as np
import sys
import os

from PandemieEnv import PandemieEnv
#but on colab
#from train.PandemieEnv import PandemieEnv

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'solvers'))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'converters'))
from DQNAgent import DQNAgent
from ModelToNetworkAdapter import ModelToNetworkAdapter


class Evaluator():
    def __init__(self, seed, numberOfGames=10):
        self.randomState = np.random.RandomState(seed)
        self.seeds = self.randomState.randint(1, 10000, numberOfGames)
        self.env = PandemieEnv()

    #TODO: change evaluator to be able to evaluate solvers, not only DQNAgents
    #IDEA: use flask with an invoker instead of pandemieEnv, EvaluationServer and EvaluationInvoker
    def evluate(self, agent):
        gameResultsAndTurns = dict()
        gameResultsAndTurns['win'] = []
        gameResultsAndTurns['loss'] = []

        #TODO: play n games using the created seeds in te beginning
        for seed in self.seeds:
            result, turns = self.playGameWithSeedUsingAgent(seed, agent)
            print("game results in {} in {} turns".format(result, turns))
            gameResultsAndTurns[result].append(turns)
            return gameResultsAndTurns

    def playGameWithSeedUsingAgent(self, seed, agent):
            print("start a new game")
            currentGame = self.env.reset()

            agent.updateGame(currentGame)
            episodeReward = []
            modelToNetWorkAdapter = ModelToNetworkAdapter(currentGame)
            state = modelToNetWorkAdapter.convertInput()
            #TODO: check if the model needs the input to be reshaped first
            state = np.reshape(state, [1, agent.stateSize])
            done = False
            while not done:
                actionID = agent.act(state)
                action = agent.possibleActions[actionID]
                try:
                    nextGame, reward, done, _ = self.env.step(action)
                    #reward = reward if not done else -10

                    agent.updateGame(nextGame)

                    modelToNetWorkAdapter = ModelToNetworkAdapter(nextGame)
                    nextState = modelToNetWorkAdapter.convertInput()

                    nextState = np.reshape(nextState, [1, agent.stateSize])
                    state = nextState

                    episodeReward.append(reward)
                    result = nextGame.outcome
                    turns = nextGame.round
                except:
                    observation = self.env.reset()
                    turns = '0'
                    result = ''

                print('Round number ', turns, "sending action", type(action))
            return result, turns


if __name__ == '__main__':
    e = Evaluator(2020)
    agent = DQNAgent(e.env.reset(), maxNumberOfRoundsInFuture=2)
    print("loading previously saved model...")
    agent.load("./model.h5")
    e.evluate(agent)