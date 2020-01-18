import matplotlib.pyplot as plt
import seaborn as sns
import glob 
import numpy as np
import pandas as pd
import sys
import os
FILE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(FILE, '..', 'util'))
from gameIO import loadGameFromFile

preTrainFilesPath = glob.glob('./jsons/validatedRandomWalkerReduced/*.json')
populations = []
infected = []
for i in range(len(preTrainFilesPath)):
    preTrainFilePath = preTrainFilesPath[i]
    inputGame = loadGameFromFile(preTrainFilePath)
    gameNumber = int(preTrainFilePath.split('\\')[1].split('-')[0][1:])
    populations.append((gameNumber, int(inputGame.round), inputGame.getOverallPopulation()))
    infected.append((gameNumber, int(inputGame.round), inputGame.getOverallInfected()))

#train on the pretrain dataset
sns.set(style="darkgrid")
populationDf = pd.DataFrame(populations, columns=['gameNumber', 'round', 'population'])
infectedDf = pd.DataFrame(infected, columns=['gameNumber', 'round', 'population'])

populationDf.to_csv('populationDf.csv')
infectedDf.to_csv('infectedDf.csv')

'''
sns.lineplot(x="round", y="population", hue='gameNumber', data=populationDf)
plt.xlabel('round')
plt.ylabel('population')
#plt.savefig('roundVsPopulationOneGameless.png', bbox_inches='tight')
plt.clf()
sns.lineplot(x="round", y="population", hue='gameNumber', data=infectedDf)
plt.xlabel('round')
plt.ylabel('infected population')
#plt.savefig('roundVsInfectedOneGameLess.png', bbox_inches='tight')
'''