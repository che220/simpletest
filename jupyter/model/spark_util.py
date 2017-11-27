import pandas as pd
from sklearn.metrics import confusion_matrix, cohen_kappa_score

class SparkEvaluator:
    def __init__(self):
        self.indexMapper = None
        self.evalData = None
        self.labelCol = ''
        self.indexedLabelCol = ''
        self.predictionCol = ''
        self.positiveClass = 'true'
        
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.kappa = 0
        self.confMat = None
        return
    
    def prettyPrint(self):
        print('')
        print("Indexer Mapping:")
        print(self.indexMapper)
        
        print('')
        print('{} value counts:'.format(self.labelCol))
        print(self.evalData[self.labelCol].value_counts())

        print('')
        print('{} value counts:'.format(self.predictionCol))
        print(self.evalData[self.predictionCol].value_counts())
        
        print('')
        print("Confusion Matrix:")
        print(self.confMat)
        
        print('')
        print('Precision: {}, Recall: {}, F1: {}'.format(self.precision, self.recall, self.f1))
        
        print('')
        print('Kappa = {}'.format(self.kappa))
        return
            
    # labels and preds are pandas.Series
    def evaluate(self, predictions, labelCol='label', indexedLabelCol='label_indexed',
                 predictionCol='prediction', positiveClass='true'):
        """
        predictions: pyspark DataFrame, usually out of testing samples after model prediction
        labelCol: these are the original labels of samples
        indexedLabelCol: these are indexed labels, for the sake of training models
        predictionCol: these are produced by model running on testing samples
        positiveClass: the label indicating a positive sample
        """

        self.labelCol = labelCol
        self.indexedLabelCol = indexedLabelCol
        self.predictionCol = predictionCol
        self.positiveClass = positiveClass
        
        # get the mappings between labels and their indexes
        b = predictions.select([labelCol, indexedLabelCol]).dropDuplicates().toPandas()
        self.indexMapper = b.set_index(b[indexedLabelCol])

        a = predictions.select([indexedLabelCol, predictionCol]).toPandas()
        a.columns = [labelCol, predictionCol]
        a[labelCol] = a[labelCol].map(b[labelCol])
        a[predictionCol] = a[predictionCol].map(b[labelCol])
        self.evalData = a

        self.confMat = confusion_matrix(a[labelCol], a[predictionCol], labels=b[labelCol])
        self.confMat = pd.DataFrame(self.confMat, columns=b[labelCol], index=b[labelCol])
        self.confMat.index.names = ['Reality']
        self.confMat.columns.names = ['Prediction']

        confMat = self.confMat
        self.recall = confMat[positiveClass][positiveClass]/confMat.sum(axis=1)[positiveClass]
        self.precision = confMat[positiveClass][positiveClass]/confMat.sum(axis=0)[positiveClass]
        self.f1 = 2*self.precision*self.recall/(self.precision+self.recall)

        self.kappa = cohen_kappa_score(a[labelCol], a[predictionCol])
        return
    