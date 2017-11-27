import pandas as pd, numpy as np, random
import sklearn.metrics as metrics

class ModelWrapper:
    # originalFeatureColumns: feature columns before one-hot encoding with get_dummies()
    # featureColumns: feature columns after one-hot encoding with get_dummies()
    # labelColumn: target column
    # positiveClass: positive class for label
    def __init__(self, originalFeatureColumns, featureColumns, labelColumn, positiveClass):
        self.positiveClass = positiveClass
        self.originalFeatureColumns = originalFeatureColumns
        self.featureColumns = featureColumns
        self.labelColumn = labelColumn
        
        self.model = None
        self.evaluator = None
        
    def buildFinalModel(self, modelData):
        return self.model
    
    def evalModel(self, modelData, folds):
        return self.evaluator

def getPredictions(model, samples, featureColumns):
    preds = model.predict_proba(samples[featureColumns]) # get probability in case we can optimize prob cutoff
    
    # if the column headers are True/False (bool), it is better to transform them to lowercase strings
    preds = pd.DataFrame(preds, columns=np.char.lower(model.classes_.astype('str')))
    return preds

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
        