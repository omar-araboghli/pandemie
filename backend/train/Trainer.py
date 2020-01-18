import sys
import os
import numpy as np

from datetime import date 

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    from train.PandemieEnv import PandemieEnv
    from google.colab import files
else:
    from PandemieEnv import PandemieEnv


FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'solvers'))
sys.path.insert(1, os.path.join(FILE, '..', 'models', 'converters'))
sys.path.insert(1, os.path.join(FILE, '..', 'util'))
from DQNAgent import DQNAgent
from ModelToNetworkAdapter import ModelToNetworkAdapter
from gameIO import loadJsonFile

from multiprocessing import Process

def main():
    args = loadJsonFile('./config.json')

    EPISODES = args["episodes"]
    MAX_ACTION = args["max_action"]
    DOWNLOAD_PERIOD = args["download_period"]
    NON_VALID_ACTION_REWARD = args["non_valid_action_reward"]

    env = PandemieEnv()
    sampleGame = env.reset()
    agent = DQNAgent(sampleGame, maxNumberOfRoundsInFuture=2)

    if args["mode"] == "load":
        print("loading previously saved model...") 
        agent.load(args["modelPath"])

    if args["mode"] == "pretrain":
        print("starting pre training phase")
        agent.preTrain(args["pretrainPath"])
        agent.save("./model_reducedInput_3500_1000_2500.h5")

    done = False
    batch_size = args["batch_size"]

    for e in range(EPISODES):
        currentGame = env.reset()
        agent.updateGame(currentGame)
        episodeReward = []
        modelToNetWorkAdapter = ModelToNetworkAdapter(currentGame)
        state = modelToNetWorkAdapter.convertInputReduced()
        #TODO: check if the model needs the input to be reshaped first
        state = np.reshape(state, [1, agent.stateSize])
        #TODO: might want to play game till the end
        for time in range(MAX_ACTION):
            # env.render()
            
            sarsBeforeEndRound = []
            stillInCombo = True

            while (stillInCombo):
                actionID = agent.act(state)
                action = agent.possibleActions[actionID]
                if(action.type == 'endRound'):
                    stillInCombo = False
                nextGame, reward, done, _ = env.step(action)
                agent.updateGame(nextGame)

                modelToNetWorkAdapter = ModelToNetworkAdapter(nextGame)
                nextState = modelToNetWorkAdapter.convertInputReduced()
                nextState = np.reshape(nextState, [1, agent.stateSize])

                sarsBeforeEndRound.append([state, action, reward, nextState, done])

                #print('Action number ', time, "sending action", type(action))
                #if action not allowed, train immidatiatly
                if reward == NON_VALID_ACTION_REWARD:
                    agent.remember(state, action, reward, nextState, done)
                    if len(agent.memory) > batch_size:
                        agent.replay(batch_size)

                state = nextState

            for sars in sarsBeforeEndRound:
                if sars[2] != NON_VALID_ACTION_REWARD:
                    sars[2] = sarsBeforeEndRound[-1][2] / len(sarsBeforeEndRound) 
                print(sars[1], sars[2])
                agent.remember(sars[0], sars[1], sars[2], sars[3], sars[4])

            sarsBeforeEndRound = []

            episodeReward.append(reward)

            if done:
                agent.update_target_model()
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, nextGame.outcome, agent.epsilon))

                print('episode reward {}'.format(episodeReward))
                print('output {} in {} rounds'.format(currentGame.outcome, currentGame.round))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

        #save after finishing each game
        modelName = date.today().strftime("%d-%m-%Y") + str(e)
        agent.save(modelName)
        
        #download from drive
        if IN_COLAB and e % DOWNLOAD_PERIOD == 0:
            print("starting download..")
            downloadThread = Process(target=files.download, args=(modelName, ))
            downloadThread.start()

    # kill last client and close connection
    env.killThread(env.clientThread)
    env.communicator.endConnection()

    #TODO: save the agent

if __name__ == "__main__":
    main()
