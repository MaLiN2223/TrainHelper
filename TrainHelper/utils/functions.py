from sklearn.model_selection import train_test_split
import logging
import numpy as np
import argparse
from ..configuration.reader import Reader
from .utils import ensure_dir_exists


def __save_and_log(data, name):
    logging.info('Saving {}'.format(name))
    np.save(name, data)


def download_splitted_dataset(downloader, test_size=0.1, name_prefix="", random_state=1):
    if test_size is None:
        test_size = 0
    logging.info('Downloading dataset.')
    (x_train, y_train), (x_valid, y_valid) = downloader()

    __save_and_log(x_train, '{}x_train'.format(name_prefix))
    __save_and_log(y_train, '{}y_train'.format(name_prefix))

    if test_size > 0:
        logging.info('Splitting validation to two sets.')
        x_valid, x_test, y_valid, y_test = train_test_split(x_valid, y_valid, test_size=test_size,
                                                            random_state=random_state)
        __save_and_log(x_test, '{}x_test'.format(name_prefix))
        __save_and_log(y_test, '{}y_test'.format(name_prefix))

    __save_and_log(x_valid, '{}x_valid'.format(name_prefix))
    __save_and_log(y_valid, '{}y_valid'.format(name_prefix))

    if test_size > 0:
        return (x_train, y_train), (x_valid, y_valid), (x_test, y_test)
    return (x_train, y_train), (x_valid, y_valid)


def __load_and_log(name, extension='npy'):
    logging.info('Loading {}'.format(name))
    return np.load('{}.{}'.format(name, extension))


def load_data(has_test=True, name_prefix=""):
    x_train = __load_and_log('{}x_train'.format(name_prefix))
    y_train = __load_and_log('{}y_train'.format(name_prefix))
    x_valid = __load_and_log('{}x_valid'.format(name_prefix))
    y_valid = __load_and_log('{}y_valid'.format(name_prefix))

    if has_test:
        x_test = __load_and_log('{}x_test'.format(name_prefix))
        y_test = __load_and_log('{}y_test'.format(name_prefix))
        return (x_train, y_train), (x_valid, y_valid), (x_test, y_test)
    return (x_train, y_train), (x_valid, y_valid)


def setup_logging(config):
    ensure_dir_exists('logs')
    log_file = 'logs/{}.log'.format(config.General.Name)
    print('Setting up logging in ', log_file)
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.info(config.config)


def load_config():
    print('---PARSING ARGUMENTS---')
    parser = argparse.ArgumentParser(description='Inputs')
    parser.add_argument('--config', help='config')
    args, leftovers = parser.parse_known_args()
    config_name = args.config
    config = Reader.read(config_name)
    return config, config_name
