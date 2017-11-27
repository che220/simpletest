import time, pandas as pd, numpy as np, random
import multiprocessing
import model.model_evaluation as model_eval
from sklearn.ensemble import RandomForestClassifier

# class to train models to compare performances and to build the final model
class RFTrainer(model_eval.ModelWrapper):
    # numTress, leafSize, criterion are random forest parameters
    # positiveClass string. Used to compute precision, recall, and f1
    def __init__(self, numTrees, leafSize, criterion, originalFeatureColumns, featureColumns, labelColumn, positiveClass):
        super(RFTrainer, self).__init__(originalFeatureColumns, featureColumns, labelColumn, positiveClass)
        self.numTrees = numTrees
        self.leafSize = leafSize
        self.criterion = criterion

    # modelData: training data
    def buildFinalModel(self, modelData):
        rf = RandomForestClassifier(n_estimators=self.numTrees, criterion=self.criterion,
                                    min_samples_leaf=self.leafSize, n_jobs=multiprocessing.cpu_count())
        self.model = rf.fit(modelData[self.featureColumns], modelData[self.labelColumn])
        return self.model
        
    # modelData: training data. Will be split into "folds" folds for cross validation
    # folds: number of folds in CV
    def evalModel(self, modelData, folds):
        rf = RandomForestClassifier(n_estimators=self.numTrees, criterion=self.criterion,
                                    min_samples_leaf=self.leafSize, n_jobs=multiprocessing.cpu_count())
        # label each row with a fold index randomly
        modelData['fold'] = [random.randint(0, folds - 1) for i in range(modelData.shape[0])]

        t1 = int(round(time.time() * 1000))
        evals = None
        classes = None
        for fold in range(folds):
            trains = modelData[modelData.fold != fold] # training data is (folds-1) folds
            tests = modelData[modelData.fold == fold] # testing is one fold
            print('Fold = {}: {} training samples, {} testing samples'.format(fold, trains.shape[0], tests.shape[0]))

            m = rf.fit(trains[self.featureColumns], trains[self.labelColumn])
            preds = m.predict_proba(tests[self.featureColumns]) # get probability in case we can optimize prob cutoff
            preds = pd.DataFrame(preds, columns=np.char.lower(m.classes_.astype('str')))
            if classes is None:
                classes = preds.columns
            preds = preds[classes]  # make sure the order of class labels are always right

            x = tests.reset_index()
            preds['truth'] = x[self.labelColumn] # add truth into the eval matrix
            if evals is None:
                evals = preds
            else:
                evals = pd.concat([evals, preds], axis=0)

        # use milliseconds to measure performances
        t2 = int(round(time.time() * 1000))
        print('n_estimators = {}, min_samples_leaf = {}, {} milliseconds'.format(self.numTrees, self.leafSize, t2 - t1))

        x = evals.truth.unique()
        evals['pred'] = x[x != self.positiveClass][0]  # assume binary class
        evals.loc[evals[str(self.positiveClass).lower()] >= 0.5, 'pred'] = self.positiveClass # prob cutoff is 0.5

        self.evaluator = model_eval.ModelEvaluator(positiveClass=self.positiveClass,
                                        params={'n_estimators': self.numTrees,
                                                'min_samples_leaf': self.leafSize,
                                                'criterion': self.criterion})
        self.evaluator.evaluate(evals.truth, evals.pred)
        return self.evaluator
