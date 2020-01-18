# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
import glob
import sys
import os
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

import tensorflow as tf

FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', '..', 'util'))

from gameIO import loadGameFromFile
from ModelToNetworkAdapter import ModelToNetworkAdapter
from Solver import Solver

EPISODES = 5000

class DQNAgent(Solver):
    def __init__(self, game, maxNumberOfRoundsInFuture, stateSize=96077):
        super().__init__(game, maxNumberOfRoundsInFuture)
        self.stateSize = stateSize
        self.possibleActions = self.generateAllPossibleActions()
        self.action_size = len(self.possibleActions)
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def root_mean_squared_error(self, y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred - y_true))) 

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        #TODO: try sigmoid, tanh
        model = Sequential()
        model.add(Dense(3500, input_dim=self.stateSize, activation='tanh'))
        model.add(Dense(1000, activation='tanh'))
        model.add(Dense(2500, activation='tanh'))
        #model.add(Dense(200000, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self.root_mean_squared_error,
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    #TODO: move pretrain to another class, or make a suitable pre train data set
    def preTrain(self, dirPath):
        #get the dataset
        preTrainFilesPath = glob.glob(dirPath + '/*-inputVector')
        inputVectors = []
        labels = []
        for i in range(4500):
            preTrainFilePath = preTrainFilesPath[i]
            #input vector
            inputVector = np.load(preTrainFilePath)
            inputVectors.append(inputVector)
            #its label
            labelFileName = preTrainFilePath[:-12] + '-probVector'
            label = np.load(labelFileName)
            #only testing
            label[label ==0] = -1.0
            label[label !=-1.0] = 0.0
            labels.append(label)

        inputVectorsNP = np.array(inputVectors)
        labelsNP = np.array(labels)
        #train on the pretrain dataset
        self.model.fit(inputVectorsNP, labelsNP, epochs=3,validation_split=0.3)
        self.update_target_model()

    def act(self, state):
        #check if points allow to do at least one action, 0 is endRound id
        if int(self.game.points) < 3:
            return 0

        if np.random.rand() <= self.epsilon:
            randomValidAction = self.getRandomValidAction(self.game)
            randomValidActionId = self.possibleActions.index(randomValidAction)
            #randomAction = random.randrange(self.action_size)
            return randomValidActionId

        return self.predict(state)  # returns action

    def updateGame(self, newGame):
        self.game = newGame

    def predict(self, state):
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            actionID = self.possibleActions.index(action)
            if done:
                target[0][actionID] = reward
            else:
                # a = self.model.predict(next_state)[0]
                t = self.target_model.predict(next_state)[0]
                target[0][actionID] = reward + self.gamma * np.amax(t)
                # target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def clearModel(self, agent):
        K.clear_session()
        del agent