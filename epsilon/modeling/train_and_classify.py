import os, sys, pandas as pd, numpy as np, logging
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import cohen_kappa_score, confusion_matrix, make_scorer
from sklearn.base import BaseEstimator, TransformerMixin

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

# Should not use PCA before random forest. PCA changed the features
class PCAFeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.variance_cutoff = 0.99
        self.features = None
        self.pca = None

    def fit(self, X, y=None):
        """
        Use random forest to select features, and then use PCA to reduce dimension

        :param X: pandas feature DataFrame
        :param y: pandas label Series
        :return: self
        """
        clf = RandomForestClassifier(n_estimators=400, max_depth=20)
        clf.fit(X, y)
        idxs = np.nonzero(clf.feature_importances_)[0]
        self.features = X.columns[idxs]
        logger.info("Number of selected features based on importance: %d", len(idxs))

        X = X[self.features]
        self.pca = PCA()
        self.pca.fit(X)
        sums = np.cumsum(self.pca.explained_variance_ratio_)
        n_components = np.argmax(sums >= self.variance_cutoff) + 1  # keep 95% variances
        self.pca = PCA(n_components)
        self.pca.fit(X)
        return self

    def transform(self, X, y=None):
        """
        select features and reduce dimension by PCA

        :param X: pandas DataFrame of features
        :param y: Not used
        :return: numpy 2D array
        """
        X = X[self.features]
        return self.pca.transform(X)

class CorrelationFeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.correlation_cutoff = 0.9
        self.features = None

    def fit(self, X, y=None):
        """
        Use random forest and correlation to select features

        :param X: pandas feature DataFrame
        :param y: pandas label Series
        :return: self
        """
        clf = RandomForestClassifier(n_estimators=400, max_depth=35)
        clf.fit(X, y)
        idxs = np.nonzero(clf.feature_importances_)[0] # index of non-zeros
        aa = clf.feature_importances_[idxs]
        b = np.argsort(-1.0 * aa) # argsort only sort ascendingly
        idxs = idxs[b] # feature index sorted by importances, 1st is the most important
        self.features = X.columns[idxs]
        logger.info("Number of selected features based on importance: %d", len(idxs))
        logger.info("some important features: %s", self.features[0:20])

        X = X[self.features.values]
        corrs = np.abs(np.corrcoef(X.values.T))
        a = np.argwhere(corrs >= self.correlation_cutoff)
        a = a[a[:,0] < a[:,1]]
        a = np.unique(a[:, 1])
        logger.info("columns to be dropped due to high correlation: %s", a.shape)

        X = X.drop(X.columns[a], axis=1)
        self.features = X.columns
        logger.info("Number of non-correlated features: %s", self.features.shape)
        logger.info("some non-correlated features: %s", self.features[0:20])

        return self

    def transform(self, X, y=None):
        """
        select features

        :param X: pandas DataFrame of features
        :param y: Not used
        :return: numpy 2D array
        """
        return X[self.features]

def manualSplitEval(features, labels):
    # this can be used to evaluate possible overfitting
    clf = RandomForestClassifier(n_estimators=100)
    split = StratifiedShuffleSplit(n_splits=10, test_size=0.3, random_state=42)
    cnt = 0
    avg_train_kappa = 0.0
    avg_val_kappa = 0.0
    for train_idx, test_idx in split.split(features, labels):
        cnt += 1
        logger.debug('(%d) split index: %s, %s', cnt, train_idx[0:10], test_idx[0:10])
        model_data, val_data = trains.iloc[train_idx, :], trains.iloc[test_idx, :]
        model_labels, val_labels = labels.iloc[train_idx], labels.iloc[test_idx]

        clf.fit(model_data, model_labels)
        logger.debug('feature importances: \n%s', clf.feature_importances_)
        non_zero_feature_idx = np.flatnonzero(clf.feature_importances_)
        logger.debug('non-zero features: %s', len(non_zero_feature_idx))

        preds = clf.predict(model_data)
        logger.debug('confusion matrix: \n%s', confusion_matrix(model_labels, preds))
        train_kappa = cohen_kappa_score(model_labels, preds)
        avg_train_kappa += train_kappa

        preds = clf.predict(val_data)
        logger.debug('confusion matrix: \n%s', confusion_matrix(val_labels, preds))
        val_kappa = cohen_kappa_score(val_labels, preds)

        logger.info('\ttrain kappa = %f, validation kappa = %f', train_kappa, val_kappa)
        avg_val_kappa += val_kappa

    avg_train_kappa /= cnt
    avg_val_kappa /= cnt
    logger.info('avg train kappa = %f, avg validation kappa = %f', avg_train_kappa, avg_val_kappa)

def cvEval(X, y):
    logger.info('features: %s, labels: %s', X.shape, y.shape)

    # test out number of estimators of RF. Best is estimators = 250 and depth=15
    for num in range(200, 500, 50):
        for depth in range(10, 40, 5):
            clf = RandomForestClassifier(n_estimators=num, max_depth=depth)
            scores = cross_val_score(clf, X, y, cv=10,
                                     scoring=make_scorer(cohen_kappa_score, greater_is_better=True))
            logger.info('n_estimators = %d, max_depth = %d, mean kappa = %f', num, depth, np.mean(scores))

def build_model(features, labels):
    clf = RandomForestClassifier(n_estimators=200, max_depth=20)
    clf.fit(features, labels)
    return clf

def predict(clf, tests):
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logger.error('Usage: %s <running mode: evaluate or production>', sys.argv[0])
        exit(1)

    is_evaluation = (sys.argv[1].lower() == 'evaluate')
    logger.info("Running mode: %s", 'evaluation' if is_evaluation else 'production')

    data_dir = os.path.dirname(__file__) + "/interview"
    label_col = 'response'

    trains = pd.read_csv(data_dir + '/train.csv')
    trains = trains.reset_index(drop=True)
    logger.info('training data: %s', trains.shape)
    logger.info('training labels: \n%s', trains[label_col].value_counts(dropna=False))
    logger.info('training samples: \n%s', trains.head(4))

    scaler = StandardScaler()
    labels = trains[label_col]
    features = trains.drop(label_col, axis=1)
    scaler.fit(features)
    features = pd.DataFrame(scaler.transform(features), columns=features.columns)

    selector = CorrelationFeatureSelector()
    selector.fit(features, labels)
    X = selector.transform(features, labels)

    if is_evaluation:
        logger.info("start model evaluation ...")
        cvEval(X, labels)
    else:
        logger.info("start calculate probabilities ...")
        clf = build_model(X, labels)
        classes = clf.classes_
        positive_class_idx = np.where(classes == 1)[0][0]
        logger.info('classes: %s', classes)
        logger.info('positive class index: %s', positive_class_idx)

        tests = pd.read_csv(data_dir + '/test.csv')
        tests = tests.reset_index(drop=True)
        logger.info('testing data: %s', tests.shape)
        logger.info('testing samples: \n%s', tests.head(4))

        # missing featurs?
        cols = [x for x in features.columns if x not in tests.columns]
        logger.info("missing features: %s", cols)
        for col in cols:
            tests[col] = 0 # for any missing features, set to zero (assume zero is the default value)

        tests = tests[features.columns] # align test data with train data
        tests = pd.DataFrame(scaler.transform(tests), columns=features.columns) # first step is to scale, as we did to training data
        X_tests = selector.transform(tests) # second step is to select features and reduce dimension
        probs = clf.predict_proba(X_tests)[:, positive_class_idx]
        logger.info(probs[0:10])
        tests['predict_response'] = probs
        logger.info('tests with prediction probabilities: \n%s', tests.head(4))

        out_file = data_dir + '/test_with_prediction_probs.csv'
        tests.to_csv(out_file)
        logger.info('output to %s', out_file)
