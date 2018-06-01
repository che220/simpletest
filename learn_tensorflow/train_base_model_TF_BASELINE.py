#!/usr/lib/anaconda3/bin/python3 -u

import os, sys, pickle, pandas as pd, logging, tensorflow as tf, shutil, datetime as dt
import myacct_env
import rec_train.training_data as training_data
import rec_train.customer_profile as customer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split

logger = logging.getLogger(os.path.basename(__file__))
__DEBUG = False

"""
TODO:

4. use NN to see if scores are the same
5. use the baysian models to score users with trainings
    a. to-be-continued to be put in the front
    b. completed to be put in the back

"""

def get_user_training(ty, use_cached_data=False):
    """
    return user training data with userid, modules, categories, CAN, YOY etc.

    :param ty:
    :return:
    """
    cache_file = myacct_env.DATA_CACHE_DIR + '/training_baysian_model_data_all.pickle'
    if ty is not None:
        cache_file = myacct_env.DATA_CACHE_DIR + '/training_baysian_model_data_TY{}.pickle'.format(ty)

    if use_cached_data and os.path.isfile(cache_file):
        logger.info('load baysian model data from %s', cache_file)
        df = pickle.load(open(cache_file, 'rb'))
        return df

    """
    yoy schema:
    
    CAN                                 int64
    PRODUCT_FAMILY                     object
    PRODUCT_GROUP                      object
    PRODUCT_SEGMENT                    object
    TOTAL_BILL                        float64
    IS_PM                                bool
    CUST_REN_CD                        object
    ACCEPTED_AK-CORP-FILING           float64
    ACCEPTED_AK-SCORP-AMENDED         float64
    ACCEPTED_AK-SCORP-FILING          float64
    """
    yoy = customer.getCANFeatures(ty, alwaysUseCache=__DEBUG)

    """
    training schema:

    userid              int64
    moduleid           object
    vendorid           object
    startedon          object
    categoryid         object
    category           object
    PRODUCT_FAMILY     object
    startedon_order     int64
    """
    training = training_data.getUserTrainingSeries(ty, alwaysUseCache=__DEBUG)
    mapping = training_data.getUserIdCANMapping(alwaysUseCache=__DEBUG)

    """
    modules schema:

    moduleid             object
    vendorid              int64
    name                 object
    description          object
    benefittag           object
    duration            float64
    aggregatedrating    float64
    recommendations      object
    ratingid             object
    ratedon              object
    rating              float64
    """
    modules = training_data.getAllModules(alwaysUseCache=__DEBUG)
    modules = modules.rename(index=str, columns={'id': 'moduleid'})

    # add names to each module user has used
    training = training.merge(modules[['moduleid', 'name']].drop_duplicates(), on='moduleid')

    # add CAN to each user in training data
    df = training.merge(mapping, on='userid')
    df = df.rename(index=str, columns={'PRODUCT_FAMILY': 'PRODUCT_FAMILY_TRAINING'})  # to avoid conflict

    def gen_key(row):
        return str(row.TY) + '-' + str(row.CAN)
    df['KEY'] = df.apply(gen_key, axis=1)
    df = df.drop(['TY', 'CAN'], axis=1)
    df = df.merge(yoy, on='KEY')

    # if two product families don't match, the data should not exist
    df = df[df.PRODUCT_FAMILY_TRAINING == df.PRODUCT_FAMILY]
    pickle.dump(df, open(cache_file, 'wb'))
    logger.info('Cached baysian model data in %s', cache_file)
    return df

def buildDNNModel(df, model_dir, forCategory=False):
    if os.path.isdir(model_dir):
        shutil.rmtree(model_dir)
        logger.info("remove %s", model_dir)

    if forCategory:
        df = df[['userid', 'KEY', 'categoryid', 'startedon_order', 'PRODUCT_GROUP', 'PRODUCT_SEGMENT', 'CUST_REN_CD', 'TOTAL_BILL']].drop_duplicates()
        label_col = 'categoryid'
    else:
        df = df[['userid', 'KEY', 'moduleid', 'startedon_order', 'PRODUCT_GROUP', 'PRODUCT_SEGMENT', 'CUST_REN_CD', 'TOTAL_BILL']].drop_duplicates()
        label_col = 'moduleid'

    if myacct_env.hasNan(df):
        exit(1)

    feature_cols = ['PRODUCT_GROUP', 'PRODUCT_SEGMENT', 'CUST_REN_CD']
    one_hot_df = pd.get_dummies(df[feature_cols], prefix=feature_cols, columns=feature_cols)
    one_hot_df['TOTAL_BILL'] = StandardScaler().fit_transform(df[['TOTAL_BILL']])

    # transform labels into sequence numbers
    classes = df[label_col].unique()
    labels = df[label_col].replace(dict(zip(classes, [i for i, j in enumerate(classes)])))
    logger.info("samples: %s", one_hot_df.shape)

    logger.debug("perform stratified split on PRODUCT_GROUP ...")
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=myacct_env.secondsSinceMidnight())
    for train_idx, test_idx in split.split(df, df.PRODUCT_GROUP):
        trains = one_hot_df.iloc[train_idx]
        tests = one_hot_df.iloc[test_idx]
        train_labels = labels.iloc[train_idx]
        test_labels = labels.iloc[test_idx]
    logger.debug("training: %s, testing: %s", trains.shape, tests.shape)

    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": trains.values}, y=train_labels.values,
                                                      num_epochs=None, shuffle=True, num_threads=myacct_env.CORES)
    feature_columns = [tf.feature_column.numeric_column('x', shape=[trains.shape[1]])]
    dnn = tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10, 10], n_classes=len(classes),
                                     activation_fn=tf.nn.elu, model_dir=model_dir)
    dnn.train(input_fn=train_input_fn, steps=5000)

    test_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": tests.values}, num_epochs=1, shuffle=False)
    ps = dnn.predict(input_fn=test_input_fn)
    for i in ps:
        logger.debug(i)
    # TODO

def buildBaselineModel(df, model_dir, forCategory=False):
    if os.path.isdir(model_dir):
        shutil.rmtree(model_dir)
        logger.info("remove %s", model_dir)

    if forCategory:
        df = df[['userid', 'KEY', 'categoryid', 'startedon_order', 'PRODUCT_GROUP']].drop_duplicates()
        label_col = 'categoryid'
    else:
        df = df[['userid', 'KEY', 'moduleid', 'startedon_order', 'PRODUCT_GROUP']].drop_duplicates()
        label_col = 'moduleid'
    if myacct_env.hasNan(df):
        exit(1)

    feature_cols = ['PRODUCT_GROUP']  # keep one trivial feature. BaselineClassifier does not use features.
    one_hot_df = pd.get_dummies(df[feature_cols], prefix=feature_cols, columns=feature_cols)

    # transform labels into sequence numbers
    classes = df[label_col].unique()
    labels = df[label_col].replace(dict(zip(classes, [i for i, j in enumerate(classes)])))
    logger.info("samples: %s", one_hot_df.shape)

    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": one_hot_df.values}, y=labels.values,
                                                        num_epochs=None, shuffle=True, num_threads=myacct_env.CORES)
    classifier = tf.estimator.BaselineClassifier(n_classes=len(classes), model_dir=model_dir)
    classifier.train(input_fn=train_input_fn, max_steps=50)
    preds = classifier.predict(train_input_fn)
    probs = None
    for pred in preds:
        probs = pred['probabilities']
        break
    rs = pd.DataFrame(list(zip(classes, probs)), columns=[label_col, 'score']).sort_values('score', ascending=False)
    return rs

def usage():
    logger.info('Usage: '+sys.argv[0]+' [-d] [-h] <ty>')
    logger.info('    -d: run in debug mode for development purpose')
    logger.info('    -h: show this help menu')

if __name__ == '__main__':
    args = sys.argv[1:]
    if '-h' in args:
        usage()
        exit(0)

    __DEBUG = ('-d' in args)
    if __DEBUG:
        args.remove('-d')
        logger.setLevel(logging.DEBUG)

    ty = None
    if len(args) == 1:
        ty = int(args[0])

    logger.info('TY: %s', ty)
    logger.info('Debug mode: %s', __DEBUG)
    origData = get_user_training(ty, use_cached_data=__DEBUG)

    cats = []
    mods = []
    for family in training_data.PRODUCT_FAMILIES:
        famDF = origData[origData.PRODUCT_FAMILY == family]
        getStartedCatId = famDF[famDF.category == 'Getting Started'].categoryid.unique()[0]
        getStartedModIds = famDF[famDF.category == 'Getting Started'].moduleid.unique()
        logger.info('category id of Getting Started: %s', getStartedCatId)
        logger.info('module ids of Getting Started: %s', getStartedModIds)

        for code in ('New', 'Existing'):
            userid = myacct_env.getDefaultUserId(code == 'New')
            if code == 'New':
                df = famDF[famDF.CUST_REN_CD == 'New']
            else:
                df = famDF[famDF.CUST_REN_CD != 'New']

            model_dir = training_data.WORK_DIR + '/Baseline_module_{}_{}'.format(family, code)
            rs = buildBaselineModel(df, model_dir, forCategory=False)
            if code == 'New':
                logger.info('move Getting Started modules to the front ...')
                maxNonGetStartedScore = rs[~rs.moduleid.isin(getStartedModIds)].score.max()
                rs.loc[rs.moduleid.isin(getStartedModIds), 'score'] = rs[rs.moduleid.isin(getStartedModIds)].score + maxNonGetStartedScore + 0.01
                rs = rs.sort_values('score', ascending=False)
                maxScore = rs.score.max()
                rs.score = rs.score / maxScore
                logger.info('\n%s', rs)
            else:
                logger.info('\n%s', rs)

            outFile = training_data.WORK_DIR + '/TF_{}_{}_module_scores.csv'.format(family, code)
            myacct_env.to_csv(outFile, rs)
            mods.append([userid, family, rs.moduleid.tolist()])

            model_dir = training_data.WORK_DIR + '/Baseline_category_{}_{}'.format(family, code)
            rs = buildBaselineModel(df, model_dir=model_dir, forCategory=True)
            if code =='New':
                logger.info('move Getting Started category to the front ...')
                maxNonGetStartedScore = rs[rs.categoryid != getStartedCatId].score.max()
                rs.loc[rs.categoryid == getStartedCatId, 'score'] = rs[rs.categoryid == getStartedCatId].score + maxNonGetStartedScore + 0.01
                rs = rs.sort_values('score', ascending=False)
                maxScore = rs.score.max()
                rs.score = rs.score / maxScore
                logger.info('\n%s', rs)
            else:
                logger.info('\n%s', rs)

            outFile = training_data.WORK_DIR + '/TF_{}_{}_category_scores.csv'.format(family, code)
            myacct_env.to_csv(outFile, rs)
            cats.append([userid, family, rs.categoryid.tolist()])

    catDF = pd.DataFrame(cats, columns=['userid', 'family', 'categoryids'])
    modDF = pd.DataFrame(mods, columns=['userid', 'family', 'moduleids'])
    catDF['last_updated'] = dt.datetime.now()
    modDF['last_updated'] = dt.datetime.now()

    myacct_env.to_csv(training_data.WORK_DIR + '/base_categories.csv', catDF)
    myacct_env.to_csv(training_data.WORK_DIR + '/base_modules.csv', modDF)

