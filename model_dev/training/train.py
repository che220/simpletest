import os, pickle, logging, tarfile, shutil, tensorflow as tf, datetime as dt
import training.train_env as train_env

logger = logging.getLogger(os.path.basename(__file__))

def train():
    # set logging level on tf to reduce logging
    debug=False
    if 'DEBUG' in os.environ:
        debug=True

    if debug:
        tf.logging.set_verbosity(logging.INFO)
        logger.info("set tensorflow verbosity to INFO")
    else:
        tf.logging.set_verbosity(logging.WARN)
        logger.info("set tensorflow verbosity to WARN")

    # clean up model output dir
    shutil.rmtree(train_env.model_dir, ignore_errors=True)
    os.makedirs(train_env.model_dir, exist_ok=True)
    logger.info('cleaned %s', train_env.model_dir)

    # data, model etc
    df = pd.DataFrame({'x' : 1,'y' : 2}, index=range(1))
    out_file = train_env.model_dir + '/data.pickle'
    pickle.dump(df, open(out_file, 'wb'))

    df = pd.DataFrame({'x' : 5, 'y' : 6}, index=range(1))
    out_file = train_env.model_dir + '/model.pickle'
    pickle.dump(df, open(out_file, 'wb'))

    # tarball trained model and data
    os.chdir(train_env.model_dir)
    model_tar = train_env.model_dir + '/../model.tar.gz'
    if os.path.isfile(model_tar):
        os.remove(model_tar)
        logger.info('removed old %s', model_tar)

    tar = tarfile.open(model_tar, "w:gz")
    for file in os.listdir(train_env.model_dir):
        tar.add(file)
    logging.info('models are tarballed in: %s', model_tar)

if __name__ == '__main__':
    train_env.define_dirs_for_local()
    train_env.model_dir += '/opt/ml/model'
    logger.info('model output dir (re-defined): %s', train_env.model_dir)
    train()
