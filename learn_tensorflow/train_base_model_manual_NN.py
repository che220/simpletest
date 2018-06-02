#!/usr/lib/anaconda3/bin/python3 -u

import os, sys, pickle, pandas as pd, logging
import myacct_env
import rec_train.training_data as training_data
import rec_train.customer_profile as customer
import tensorflow as tf
from sklearn.model_selection import StratifiedShuffleSplit

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
    df = get_user_training(ty, use_cached_data=__DEBUG)

    df = df[(df.PRODUCT_FAMILY == 'LACERTE') & (df.CUST_REN_CD == 'New')]
    df = df[['userid', 'KEY', 'categoryid', 'category', 'startedon_order', 'PRODUCT_GROUP', 'PRODUCT_SEGMENT', 'TOTAL_BILL']].drop_duplicates()
    if myacct_env.hasNan(df):
        exit(1)

    feature_cols = ['PRODUCT_GROUP', 'PRODUCT_SEGMENT']
    label_col = 'categoryid'
    one_hot_df = pd.get_dummies(df[feature_cols], prefix=feature_cols, columns=feature_cols)

    # transform labels into sequence numbers
    classes = df[label_col].unique()
    labels = df[label_col].replace(dict(zip(classes, [i for i, j in enumerate(classes)])))

    logger.debug("perform stratified split on PRODUCT_GROUP ...")
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=myacct_env.secondsSinceMidnight())
    for train_idx, test_idx in split.split(df, df.PRODUCT_GROUP):
        trains = one_hot_df.iloc[train_idx]
        tests = one_hot_df.iloc[test_idx]
        train_labels = labels.iloc[train_idx]
        test_labels = labels.iloc[test_idx]

    logger.debug("training: %s, testing: %s", trains.shape, tests.shape)

    X = tf.placeholder(tf.float32, shape=(None, trains.shape[1]), name="X")
    y = tf.placeholder(tf.int32, shape=(None), name="y")

    with tf.name_scope('dnn'):
        hidden1 = tf.layers.dense(X, units=10, activation=tf.nn.relu, name='hidden1')
        hidden2 = tf.layers.dense(hidden1, units=10, activation=tf.nn.relu, name='hidden2')
        logits = tf.layers.dense(hidden2, units=len(classes), activation=tf.nn.relu, name='outputs')
        y_proba = tf.nn.softmax(logits)

    with tf.name_scope('loss'):
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
        loss = tf.reduce_mean(xentropy, name="loss")

    learning_rate = 0.01
    with tf.name_scope("train"):
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        training_op = optimizer.minimize(loss)

    with tf.name_scope('eval'):
        # logits is a 2D numpy array, like this:
        #
        # <class 'numpy.ndarray'> (1160, 10)
        # [[0.23936488 0.         0.         0.27902588 0.         0. 0.05300933 0.24646123 0.2787308  0.26884508]
        # [0.45942634 0.06383048 0.0357738  0.21491887 0.5715122  0. 0.24600069 0.         0.         0.1714494 ]
        # [0.23936488 0.         0.         0.27902588 0.         0. 0.05300933 0.24646123 0.2787308  0.26884508]
        # [0.45942634 0.06383048 0.0357738  0.21491887 0.5715122  0. 0.24600069 0.         0.         0.1714494 ]
        # [0.45942634 0.06383048 0.0357738  0.21491887 0.5715122  0. 0.24600069 0.         0.         0.1714494 ] ...]
        #
        # y_proba is also a 2D array, like this:
        #
        # <class 'numpy.ndarray'> (1160, 10)
        #[[0.10993675 0.08653425 0.08653425 0.11438458 0.08653425 0.08653425 0.09124514 0.11071968 0.11435083 0.11322596]
        # [0.13017175 0.08764187 0.0852171  0.10193621 0.14561127 0.08222244 0.10515432 0.08222244 0.08222244 0.09760003]
        # [0.10993675 0.08653425 0.08653425 0.11438458 0.08653425 0.08653425 0.09124514 0.11071968 0.11435083 0.11322596]
        # [0.13017175 0.08764187 0.0852171  0.10193621 0.14561127 0.08222244 0.10515432 0.08222244 0.08222244 0.09760003]
        # [0.13017175 0.08764187 0.0852171  0.10193621 0.14561127 0.08222244 0.10515432 0.08222244 0.08222244 0.09760003]] ...]
        #
        # y is 1D numpy array (because of feed_dict={X: trains.values, y: train_labels.values})
        #
        # <class 'numpy.ndarray'> (1160,)
        # [3 3 1 0 3 ...]
        #

        # k = 1: pick the top 1 indices of each row in logits. Based on above data, that would be:
        #
        # [3 0 4 4 4 ...]
        #
        # compare this with y array, we get the following (k can be any integer. y only needs to be in top-K to get True):
        #
        # correct is a list of True/False, 1D numpy array
        #
        # <class 'numpy.ndarray'> (1160,)
        # [ True False False False False ...]
        #
        # tf.cast: True -> 1.0, False -> 0.0
        # tf.reduce_mean: take the mean of the 1.0/0.0 1D array, which is just the fraction of 1.0s
        correct = tf.nn.in_top_k(logits, y, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

    with tf.Session() as sess:
        sess.run((tf.global_variables_initializer(), tf.tables_initializer()))

        last_acc = -1.0
        tolerance = 0.0001
        max_acc_cnt = 0
        for i in range(1000):
            x_val, logits_val, loss_val, _ = sess.run([X, logits, loss, training_op], feed_dict={X: trains.values, y: train_labels.values})
            acc_train = accuracy.eval(feed_dict={X: trains.values, y: train_labels.values})
            acc_test = accuracy.eval(feed_dict={X: tests.values, y: test_labels.values})
            logger.debug("Epoch = %d: loss: %s, training sample accuracy: %s, testing sample accuracy: %s", i, loss_val, acc_train, acc_test)

            if acc_test < last_acc:
                max_acc_cnt += 1
                if max_acc_cnt >= 3:
                    break
            else:
                max_acc_cnt = 0
                last_acc = acc_test
