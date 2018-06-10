import os, sys, pandas as pd, numpy as np, logging
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import cohen_kappa_score, confusion_matrix, make_scorer

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

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

def cvEval(features, labels):
    # test out number of estimators of RF. Best is estimators = 250 and depth=15
    for num in range(50, 500, 50):
        for depth in range(5, 40, 5):
            clf = RandomForestClassifier(n_estimators=num, max_depth=depth)
            scores = cross_val_score(clf, features, labels, cv=10,
                                     scoring=make_scorer(cohen_kappa_score, greater_is_better=True))
            logger.info('n_estimators = %d, max_depth = %d, mean kappa = %f', num, depth, np.mean(scores))

def build_model(features, labels):
    clf = RandomForestClassifier(n_estimators=250, max_depth=15)
    clf.fit(features, labels)
    return clf

def predict(clf, tests):
    pass

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
#mode = 'Evaluation'
mode = 'Production'

if mode == 'Evaluation':
    cvEval(features, labels)
else:
    clf = build_model(features, labels)
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
    probs = clf.predict_proba(scaler.transform(tests))[:, positive_class_idx]
    logger.info(probs[0:10])
    tests['predict_response'] = probs
    logger.info('tests with prediction probabilities: \n%s', tests.head(4))

    out_file = data_dir + '/test_with_prediction_probs.csv'
    tests.to_csv(out_file)
    logger.info('output to %s', out_file)
