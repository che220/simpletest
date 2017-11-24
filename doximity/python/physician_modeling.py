"""
model training and evaluation classes
"""
import time, pandas as pd, numpy as np, random
import multiprocessing
from sklearn.ensemble import *
import sklearn.metrics as metrics


class ModelEvaluator:
    # params is a dictionary to record whatever parameters you want to record
    # positiveClass: for precison, recall, f1 calculation
    def __init__(self, positiveClass, params={}):
        self.positiveClass = positiveClass
        self.params = params

        self.kappa = self.precision = self.recall = self.f1 = 0.0
        self.confusionMatrix = None
        return

    # self-explanatory
    def getConfusionMatrix(self, truths, predictions):
        conf = metrics.confusion_matrix(truths, predictions)
        conf = pd.DataFrame(conf)

        # name rows and columns properly
        x = np.sort(truths.unique())
        conf.columns = x
        conf.index = x
        conf.columns.names = ['Prediction']
        conf.index.names = ['Reality']
        return conf

    # calc kappa, precision, recall, f1, confusion matrix and print them out
    def evaluate(self, truths, predictions):
        self.kappa = metrics.cohen_kappa_score(truths, predictions)

        prf = metrics.precision_recall_fscore_support(truths, predictions,
                                                      pos_label=self.positiveClass, average='binary')
        self.precision = prf[0]
        self.recall = prf[1]
        self.f1 = prf[2]

        self.confusionMatrix = self.getConfusionMatrix(truths, predictions)
        print("")
        print('Model Parameters: ')
        print(self.params)
        print("")
        print("Confusion Matrix:")
        print("")
        print(self.confusionMatrix)
        print("")
        print("Precision = %.3f, Recall = %.3f, F1 = %.3f, Kappa = %.3f" % (self.precision, self.recall, self.f1, self.kappa))


# class to train models to compare performances and to build the final model
class RandomForestTrainer:
    # numTress, leafSize, criterion are random forest parameters
    # positiveClass string. Used to compute precision, recall, and f1
    def __init__(self, numTrees, leafSize, criterion, positiveClass):
        self.numTrees = numTrees
        self.leafSize = leafSize
        self.criterion = criterion
        self.positiveClass = positiveClass
        self.model = None
        self.evaluator = None

    # modelData: training data
    # featureColumns: feature columns
    # labelColumn: target column name
    def buildFinalModel(self, modelData, featureColumns, labelColumn):
        rf = RandomForestClassifier(n_estimators=self.numTrees, criterion=self.criterion,
                                    min_samples_leaf=self.leafSize, n_jobs=multiprocessing.cpu_count())
        self.model = rf.fit(modelData[featureColumns], modelData[labelColumn])

    # modelData: training data. Will be split into "folds" folds for cross validation
    # featureColumns: feature columns
    # labelColumn: target column name
    # folds: number of folds in CV
    def trainModel(self, modelData, featureColumns, labelColumn, folds):
        rf = RandomForestClassifier(n_estimators=self.numTrees, criterion=self.criterion,
                                    min_samples_leaf=self.leafSize, n_jobs=multiprocessing.cpu_count())
        # label each row with a fold index randomly
        modelData['fold'] = [random.randint(0, folds - 1) for i in range(modelData.shape[0])]

        t1 = int(round(time.time() * 1000))
        evals = None
        for fold in range(folds):
            trains = modelData[modelData.fold != fold] # training data is (folds-1) folds
            tests = modelData[modelData.fold == fold] # testing is one fold
            print('Fold = {}: {} training samples, {} testing samples'.format(fold, trains.shape[0], tests.shape[0]))

            m = rf.fit(trains[featureColumns], trains[labelColumn])
            preds = m.predict_proba(tests[featureColumns]) # get probability in case we can optimize prob cutoff
            preds = pd.DataFrame(preds, columns=m.classes_)
            preds = preds[np.sort(m.classes_)]  # make sure the order of class labels are always right

            x = tests.reset_index()
            preds['truth'] = x[labelColumn] # add truth into the eval matrix
            if evals is None:
                evals = preds
            else:
                evals = pd.concat([evals, preds], axis=0)

        # use milliseconds to measure performances
        t2 = int(round(time.time() * 1000))
        print('n_estimators = {}, min_samples_leaf = {}, {} milliseconds'.format(self.numTrees, self.leafSize, t2 - t1))

        x = evals.truth.unique()
        evals['pred'] = x[x != self.positiveClass][0]  # assume binary class
        evals.loc[evals[self.positiveClass] >= 0.5, 'pred'] = self.positiveClass # prob cutoff is 0.5

        self.evaluator = ModelEvaluator(positiveClass=self.positiveClass,
                                        params={'n_estimators': self.numTrees,
                                                'min_samples_leaf': self.leafSize,
                                                'criterion': self.criterion})
        self.evaluator.evaluate(evals.truth, evals.pred)


class DocModel:
    def __init__(self):
        self.model = None
        self.procedureCodes = None
