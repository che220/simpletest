"""
This file is used to evaluate models with different parameters
"""
import sys
from physician_data import *
from physician_modeling import *

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)

def usage():
    print('usage: python {} <data directory> <physician type>'.format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

dataDir = sys.argv[1]
docType = sys.argv[2]

dataProcessor = DocDataProcessor(dataDir, docType)
dataProcessor.processData()

specs = dataProcessor.getSpecialtyCodes()
features = dataProcessor.getModelFeatures()
modelData = dataProcessor.getModelData()
physicians = modelData.physician_id

# grid search n_estimators, min_samples_leaf, and gini vs entropy
# one 10-fold CV run takes about 5 mins on my laptop. 2.5 mins on 8-core Linux
yCol = 'spec_code'
positiveClass = docType.upper()

numTrees = 100 # 100 is sufficient for this project. Tested
leafSize = 2 # 2 is optimal. Tested
criterion = 'entropy' # entropy is slightly better than gini. Tested

print("=======================================")
rf = RandomForestTrainer(numTrees=numTrees, leafSize=leafSize, criterion=criterion, positiveClass=positiveClass)
rf.trainModel(modelData, features.feature, yCol, folds=10)
"""
Model Parameters: 
{'n_estimators': 100, 'min_samples_leaf': 2, 'criterion': 'entropy'}

Confusion Matrix:

Prediction  Cardiology    Not
Reality                      
Cardiology        7738    536
Not                185  16474

Precision = 0.977, Recall = 0.935, F1 = 0.955, Kappa = 0.934
"""
