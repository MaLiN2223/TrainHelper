import keras
import logging
from src.callbacks import Repeater


def get_early_stopping(config):
    if config.EarlyStopping is not False and config.EarlyStopping is not None:
        early_stop = config.EarlyStopping.EarlyStopping
        early_stop = early_stop if early_stop is not None else 10
        monitor = config.EarlyStopping.Monitor
        monitor = monitor if monitor is not None else 'val_acc'
        logging.info('Model will early stop after {}'.format(early_stop))
        early = keras.callbacks.EarlyStopping(monitor=monitor, patience=early_stop, mode='auto')
        return early
    else:
        return None


def get_model_checkpoint(base_name, monitor, save_best_only):
    comment = "for best epoch" if save_best_only else "every epoch"
    logging.info('Model will save checkpoint {}'.format(comment))
    keras.callbacks.ModelCheckpoint(base_name + '_best.h5', monitor=monitor, save_best_only=save_best_only,
                                    save_weights_only=True, mode='auto', period=None if save_best_only else 1)


def get_tensor_board(base_name, batch_size):
    return keras.callbacks.TensorBoard(log_dir=base_name, histogram_freq=0, batch_size=batch_size, write_graph=True)


def get_keras_callbacks(config):
    callbacks = []
    base_name = config.General.ResultsDir + '/' + config.General.Name

    if config.ModelCheckpoint.Best:
        callbacks.append(get_model_checkpoint(base_name, config.ModelCheckpoint.Monitor, True))
    if config.ModelCheckpoint.EachEpoch:
        callbacks.append(get_model_checkpoint(base_name, config.ModelCheckpoint.Monitor, False))
    if config.EarlyStopping:
        callbacks.append(get_early_stopping(config))
    if config.TensorBoard:
        callbacks.append(get_tensor_board(base_name, config.Training.BatchSize))
    if config.CSV:
        callbacks.append(keras.callbacks.CSVLogger(base_name + '.log'))
    if config.Repeater:
        callbacks.append(Repeater(config, config.queuer))
    return callbacks
