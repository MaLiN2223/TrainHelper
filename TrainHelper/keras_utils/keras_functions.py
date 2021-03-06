import keras
import logging


def __get_early_stopping(config):
    early_stop = config.EarlyStopping.EarlyStopping
    early_stop = early_stop if early_stop is not None else 10
    monitor = config.EarlyStopping.Monitor
    monitor = monitor if monitor is not None else 'val_acc'
    logging.info('Model will early stop after {}'.format(early_stop))
    early = keras.callbacks.EarlyStopping(monitor=monitor, patience=early_stop, mode='auto')
    return early


def __get_model_checkpoint(base_name, monitor, save_best_only):
    comment = "for best epoch" if save_best_only else "every epoch"
    logging.info('Model will save checkpoint {}'.format(comment))
    return keras.callbacks.ModelCheckpoint(base_name + '_best.h5', monitor=monitor, save_best_only=save_best_only,
                                           save_weights_only=True, mode='auto', period=1)


def __get_tensor_board(base_name, batch_size):
    return keras.callbacks.TensorBoard(log_dir=base_name, histogram_freq=0, batch_size=batch_size, write_graph=True)


def get_keras_callbacks(config):
    callbacks = []
    base_name = config.General.ResultsDir + '/' + config.General.Name

    if config.ModelCheckpoint.Best:
        callbacks.append(__get_model_checkpoint(base_name, config.ModelCheckpoint.Monitor, True))
    if config.ModelCheckpoint.EachEpoch:
        callbacks.append(__get_model_checkpoint(base_name, config.ModelCheckpoint.Monitor, False))
    if config.EarlyStopping:
        callbacks.append(__get_early_stopping(config))
    if config.TensorBoard:
        callbacks.append(__get_tensor_board(base_name, config.Training.BatchSize))
    if config.CSV:
        callbacks.append(keras.callbacks.CSVLogger(base_name + '.log'))
    if config.Repeater:
        from TrainHelper.callbacks import Repeater  # because we don't want to import TensorFlow directly
        callbacks.append(Repeater(config, config.queuer))
    return callbacks
